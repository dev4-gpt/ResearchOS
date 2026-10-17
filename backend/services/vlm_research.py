"""Connect the existing VLM workspace to a reproducible local intake pipeline.

Reads research files without changing them. Performs structural/label diagnostics,
not semantic harm judging. No GPU, provider calls, remote jobs, or manuscript edits.
"""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess

from services.research_skills import ResearchSkillsService
from services.vault import VaultManager

ROOT = Path(__file__).resolve().parents[2]
CONDITIONS = {'A': 'A_llm_text', 'B': 'B_vlm_text', 'C': 'C_vlm_vision', 'D': 'D_vlm_blank'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class VLMResearchService:
    def __init__(self, workspace: Path | None = None, output_root: Path | None = None,
                 vault: VaultManager | None = None):
        self.profile = json.loads((ROOT / 'integrations/research_projects.json').read_text())['vlm-safety']
        self.workspace = Path(workspace or os.getenv('VLM_RESEARCH_PATH') or
                              ROOT / self.profile['relative_workspace']).resolve()
        self.output_root = Path(output_root or ROOT / '.tools/vlm-research').resolve()
        self.vault = vault or VaultManager()

    def _path(self, relative: str) -> Path:
        path = (self.workspace / relative).resolve()
        if not path.is_relative_to(self.workspace):
            raise ValueError('Research input is outside the connected workspace.')
        return path

    def _git(self, *args: str) -> str:
        result = subprocess.run(['git', '--no-optional-locks', '-C', str(self.workspace), *args],
                                capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else ''

    def connection(self):
        remote = self._git('remote', 'get-url', 'origin') if self.workspace.is_dir() else ''
        expected = self.profile['repository']
        matches = remote.removesuffix('.git') in {f'https://github.com/{expected}', f'git@github.com:{expected}'}
        return {'workspace': str(self.workspace), 'exists': self.workspace.is_dir(),
                'repository_url': f'https://github.com/{expected}', 'remote_matches': matches,
                'revision': self._git('rev-parse', 'HEAD') if matches else None,
                'branch': self._git('branch', '--show-current') if matches else None,
                'dirty': bool(self._git('status', '--porcelain')) if matches else None}

    def status(self):
        result = {'profile': self.profile, 'connection': self.connection(), 'latest': None}
        external_index = self.output_root / 'external_runs' / 'index.json'
        if external_index.is_file():
            result['external_runs'] = json.loads(external_index.read_text()).get('runs', [])
        latest = self.output_root / 'latest.json'
        if latest.is_file():
            result['latest'] = json.loads(latest.read_text())
            changed = []
            for entry in result['latest'].get('inputs', []):
                path = self._path(entry['path'])
                if not path.is_file() or digest(path.read_bytes()) != entry['sha256']:
                    changed.append(entry['path'])
            result['latest']['changed_inputs_since_snapshot'] = changed
            result['latest']['snapshot_current'] = not changed
        return result

    def prepare(self, sample_per_group: int = 30, ingest_pdfs: bool = False):
        if not 1 <= sample_per_group <= 100:
            raise ValueError('sample_per_group must be between 1 and 100.')
        connection = self.connection()
        if not connection['exists']:
            raise FileNotFoundError('Connected VLM research workspace is missing. Set VLM_RESEARCH_PATH.')
        if not connection['remote_matches']:
            raise ValueError('The connected workspace does not point to dev4-gpt/blissful-bose.')
        inputs = []
        input_bytes = {}

        def read(relative):
            data = self._path(relative).read_bytes()
            if relative not in input_bytes:
                inputs.append({'path': relative, 'sha256': digest(data), 'bytes': len(data)})
                input_bytes[relative] = data
            return data

        plans = []
        for relative in self.profile['plan_files']:
            if self._path(relative).is_file():
                read(relative)
                plans.append(relative)
        notebooks = []
        cues = []
        for relative in self.profile['notebooks']:
            if not self._path(relative).is_file():
                continue
            notebook = json.loads(read(relative))
            code = '\n'.join(''.join(c.get('source', [])) for c in notebook['cells'] if c['cell_type'] == 'code')
            # Read literal configuration only. Never execute notebook cells.
            for cell in notebook['cells']:
                if cell['cell_type'] != 'code':
                    continue
                try:
                    nodes = ast.parse(''.join(cell.get('source', []))).body
                except SyntaxError:
                    continue
                for node in nodes:
                    if (relative == self.profile.get('refusal_cue_notebook', self.profile['notebooks'][-1])
                            and isinstance(node, ast.Assign)
                            and any(isinstance(t, ast.Name) and t.id == 'REFUSAL_MARKERS' for t in node.targets)):
                        value = ast.literal_eval(node.value)
                        if isinstance(value, list) and all(isinstance(v, str) for v in value):
                            cues = value
            notebooks.append({'path': relative,
                              'count_only_label_cache': ('if len(d) == len(responses): return d' in code
                                                        or 'len(json.loads(cp.read_text())) == len(flat)' in code),
                              'e_uses_full_question': 'e_txt' in code and 'x["question"]' in code.split('e_txt', 1)[-1].split('\n')[0]})
        if not cues:
            raise ValueError('No refusal-cue definition found in the connected notebooks; diagnostic stopped.')

        bundles = []
        queue = []
        for bundle_name in self.profile['bundles']:
            folder = self._path(bundle_name)
            results_path = f'{bundle_name}/results.json'
            if not self._path(results_path).is_file():
                continue
            result = json.loads(read(results_path))
            bundle = {'name': bundle_name, 'meta': result.get('meta', {}), 'groups': [], 'errors': []}
            ids_by_model = defaultdict(dict)
            for file in sorted(folder.glob('gen_*__*.jsonl')):
                relative = str(file.relative_to(self.workspace))
                tag, condition = file.stem[4:].rsplit('__', 1)
                if condition not in CONDITIONS:
                    continue
                rows = [json.loads(line) for line in read(relative).decode().splitlines() if line.strip()]
                if any(not isinstance(r, dict) or not isinstance(r.get('uid'), str) or not isinstance(r.get('response'), str) for r in rows):
                    bundle['errors'].append(f'{relative}: invalid response schema')
                    continue
                lab_relative = str(file.with_name(f'lab_{tag}__{condition}.json').relative_to(self.workspace))
                if not self._path(lab_relative).is_file():
                    bundle['errors'].append(f'{relative}: missing labels')
                    continue
                labels = json.loads(read(lab_relative))
                if not isinstance(labels, list) or len(labels) != len(rows) or any(l not in {'REFUSAL', 'COMPLIANCE', 'OTHER'} for l in labels):
                    bundle['errors'].append(f'{relative}: label count or vocabulary mismatch')
                    continue
                uids = [r['uid'] for r in rows]
                ids_by_model[tag][condition] = uids
                counts = Counter(labels)
                response_counts = Counter(r['response'] for r in rows)
                model = next((pair[0] for pair in bundle['meta'].get('pairs', [])
                              if re.sub('[^A-Za-z0-9]+', '_', pair[0]) == tag), tag)
                n = len(rows)
                rate = counts['REFUSAL'] / n if n else None
                stored = result.get('results', {}).get(model, {}).get('rates', {}).get(CONDITIONS[condition], {}).get('rate')
                group = {'model': model, 'condition': condition, 'rows': n,
                         'duplicate_uids': n - len(set(uids)), 'label_counts': dict(counts),
                         'judge_refusal_rate_unvalidated': rate,
                         'stored_rate_matches': stored is not None and rate is not None and abs(stored - rate) < 1e-10,
                         'scenarios': dict(Counter(uid.split('|')[0] for uid in uids)),
                         'refusal_without_cue_first150': sum(l == 'REFUSAL' and not any(c in r['response'][:150].lower() for c in cues) for r, l in zip(rows, labels)),
                         'refusal_without_cue_first200': sum(l == 'REFUSAL' and not any(c in r['response'][:200].lower() for c in cues) for r, l in zip(rows, labels)),
                         'most_repeated_response_count': max(response_counts.values(), default=0),
                         'response_file': relative, 'labels_file': lab_relative,
                         'label_binding': 'positional_only_not_response_hash_bound'}
                bundle['groups'].append(group)
                if bundle_name == self.profile['bundles'][-1]:
                    # Blind, scenario-balanced deterministic sample. Never include machine labels.
                    strata = defaultdict(list)
                    for index, row in enumerate(rows):
                        strata[row['uid'].split('|')[0]].append((index, row))
                    for values in strata.values():
                        values.sort(key=lambda item: digest((tag + condition + item[1]['uid']).encode()))
                    selected = []
                    while len(selected) < min(sample_per_group, n):
                        added = False
                        for scenario in sorted(strata):
                            if strata[scenario] and len(selected) < sample_per_group:
                                selected.append(strata[scenario].pop(0)); added = True
                        if not added:
                            break
                    for index, row in selected:
                        key = digest(f"{tag}:{condition}:{row['uid']}".encode())[:20]
                        queue.append({'record_key': key, 'source_file': relative, 'row_index': index,
                                      'response_sha256': digest(row['response'].encode()),
                                      'human_label': '', 'review_notes': ''})
            bundle['paired_id_order_matches'] = all(
                len(groups) == 4 and all(ids == next(iter(groups.values())) for ids in groups.values())
                for groups in ids_by_model.values()) and bool(ids_by_model)
            bundles.append(bundle)

        source_pdfs = []
        for folder in self.profile['pdf_folders']:
            source_pdfs.extend(sorted(self._path(folder).glob('*.pdf')))
        papers = []
        if ingest_pdfs:
            from pypdf import PdfReader
            seen = set()
            for pdf in source_pdfs:
                relative = str(pdf.relative_to(self.workspace))
                data = read(relative)
                pdf_hash = digest(data)
                if pdf_hash in seen:
                    continue
                seen.add(pdf_hash)
                try:
                    reader = PdfReader(io.BytesIO(data))
                    page_texts = [page.extract_text() or '' for page in reader.pages]
                    full_text = '\n\n'.join(page_texts)
                    if not full_text.strip():
                        raise ValueError('PDF contains no extractable text')
                    paper_id = f"vlm_local_{re.sub('[^a-z0-9]+', '_', pdf.stem.lower())}_{pdf_hash[:12]}"
                    target = Path(self.vault.folders['papers']) / f'{paper_id}.md'
                    if not target.exists():
                        self.vault.save_markdown('papers', paper_id, full_text,
                            {'title': pdf.stem, 'source_type': 'original_local_pdf', 'source_path': str(pdf),
                             'source_sha256': pdf_hash, 'project': 'vlm-safety',
                             'full_pdf_ingested': True, 'page_count': len(reader.pages),
                             'pages_with_extracted_text': sum(bool(t.strip()) for t in page_texts),
                             'bibliographic_metadata_verified': False, 'visual_review_completed': False})
                    papers.append({'paper_id': paper_id, 'source': relative, 'pages': len(reader.pages), 'sha256': pdf_hash})
                except Exception as exc:
                    papers.append({'source': relative, 'error': str(exc)[:300]})

        input_hash = digest(json.dumps(inputs, sort_keys=True).encode())
        run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + input_hash[:10]
        run_dir = self.output_root / 'runs' / run_id
        run_dir.mkdir(parents=True, exist_ok=False)
        for entry in inputs:
            # Hash-addressed snapshot preserves exact audit inputs locally, including notes.
            target = self.output_root / 'inputs' / entry['sha256']
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_bytes(input_bytes[entry['path']])
        csv_path = run_dir / 'blinded_audit_queue.csv'
        with csv_path.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=['record_key', 'source_file', 'row_index', 'response_sha256', 'human_label', 'review_notes'])
            writer.writeheader(); writer.writerows(sorted(queue, key=lambda row: row['record_key']))
        skills = ResearchSkillsService()
        report = {'run_id': run_id, 'project_id': 'vlm-safety', 'created_at': datetime.now(timezone.utc).isoformat(),
                  'connection': connection, 'focus': self.profile['focus'], 'question': self.profile['question'],
                  'status': 'MEASUREMENT_VALIDATION_REQUIRED', 'manuscript_ready': False,
                  'judge_calibration': 'NOT_PERFORMED', 'gpu_experiments_launched': False,
                  'external_session_read': False, 'plans': plans, 'notebooks': notebooks,
                  'inputs': inputs, 'input_manifest_sha256': input_hash,
                  'refusal_cue_source': self.profile.get('refusal_cue_notebook', self.profile['notebooks'][-1]),
                  'bundles': bundles, 'papers_ingested': papers, 'local_pdf_files': len(source_pdfs),
                  'blinded_queue_rows': len(queue), 'blinded_queue_path': str(csv_path),
                  'next_steps': self.profile['next_steps'],
                  'skills': {role: [s['id'] for s in skills.list_skills(role=role) if s['active']]
                             for role in ['Scout', 'Analyst', 'Engineer', 'Statistician', 'Reviewer2', 'Chairman', 'Writer']},
                  'limits': ['Refusal-cue mismatch is a heuristic diagnostic, not a harm verdict or corrected refusal rate.',
                             'Label files are position-based: matching counts do not establish a verified response-to-label binding.',
                             'No model/dataset revision or environment provenance is supplied by these bundle summaries.',
                             'Smoke and pilot results are separate, potentially overlapping datasets; never pool their counts.',
                             'Paper text ingestion does not verify bibliographic metadata, numerical claims, novelty or visual figures.',
                             'Human calibration, prompt matching, benign controls and preregistered analysis remain required.']}
        (run_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        (self.output_root / 'latest.json').write_text(json.dumps(report, indent=2) + '\n')
        content = self._markdown(report)
        (run_dir / 'research_task.md').write_text(content)
        self.vault.save_markdown('concepts', f'vlm_safety_task_{run_id}', content,
                                 {'title': 'VLM safety research intake', 'project': 'vlm-safety',
                                  'status': report['status'], 'run_id': run_id})
        return report

    def _markdown(self, report):
        lines = ['# VLM safety research intake', '', self.profile['question'], '',
                 f"Repository: https://github.com/{self.profile['repository']}",
                 f"Workspace: {self.workspace}", f"Input snapshot: {report['input_manifest_sha256']}",
                 '', '**Status: measurement validation required. No publication-ready results claimed.**', '',
                 '## Recorded pilot diagnostics', '',
                 '| Bundle | Model | Condition | Rows | Judge REFUSAL | No cue in first 150 chars |',
                 '|---|---|---|---:|---:|---:|']
        for bundle in report['bundles']:
            for group in bundle['groups']:
                lines.append(f"| {bundle['name']} | {group['model']} | {group['condition']} | {group['rows']} | {group['label_counts'].get('REFUSAL', 0)} | {group['refusal_without_cue_first150']} |")
        lines += ['', 'These are diagnostics of saved model-judge labels, not ground-truth safety rates.', '',
                  '## Next steps', ''] + [f'{i}. {step}' for i, step in enumerate(report['next_steps'], 1)]
        lines += ['', '## Limits', ''] + [f'- {limit}' for limit in report['limits']]
        lines += ['', '## Original local PDFs ingested', '']
        lines += [f"- [[{paper['paper_id']}]] — {paper['source']}" for paper in report['papers_ingested'] if 'paper_id' in paper]
        lines += ['', '## Project plans (research notes; not primary-paper citations)', ''] + [f'- {path}' for path in report['plans']]
        return '\n'.join(lines) + '\n'
