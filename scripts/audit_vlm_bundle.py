"""Create a local, hash-addressed audit summary for a completed VLM results ZIP."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / '.tools/vlm-research/external_runs'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_member(name: str) -> None:
    member = PurePosixPath(name)
    if member.is_absolute() or '..' in member.parts:
        raise ValueError(f'Unsafe ZIP member path: {name!r}')


def audit(archive: Path, notebook: Path | None = None, output_root: Path = DEFAULT_OUTPUT) -> dict:
    raw = archive.read_bytes()
    archive_hash = sha256(raw)
    with zipfile.ZipFile(archive) as zf:
        for item in zf.infolist():
            safe_member(item.filename)
            if item.file_size > 100_000_000:
                raise ValueError(f'ZIP member exceeds 100 MB: {item.filename}')
        if 'results.json' not in zf.namelist():
            raise ValueError('ZIP has no results.json')
        data = json.loads(zf.read('results.json'))
        meta = data.get('meta', {})
        if meta.get('version') != 'v2':
            raise ValueError('This audit entry point expects a v2 results bundle.')
        cues = []
        notebook_hash = None
        if notebook:
            source = json.loads(notebook.read_text())
            notebook_hash = sha256(notebook.read_bytes())
            for cell in source.get('cells', []):
                if cell.get('cell_type') != 'code':
                    continue
                code = ''.join(cell.get('source', []))
                try:
                    nodes = __import__('ast').parse(code).body
                except SyntaxError:
                    continue
                for node in nodes:
                    if isinstance(node, __import__('ast').Assign) and any(
                        isinstance(target, __import__('ast').Name) and target.id == 'REFUSAL_MARKERS'
                        for target in node.targets
                    ):
                        value = __import__('ast').literal_eval(node.value)
                        if isinstance(value, list) and all(isinstance(v, str) for v in value):
                            cues = value
        models = {}
        for model, result in data.get('results', {}).items():
            if model.startswith('_'):
                continue
            tag = re.sub(r'[^A-Za-z0-9]+', '_', model)
            groups = {}
            uid_sequences = {}
            for condition in 'ABCDE':
                label_name = f'lab_{tag}__{condition}.json'
                generation_name = f'gen_{tag}__{condition}.jsonl'
                if label_name not in zf.namelist() or generation_name not in zf.namelist():
                    continue
                labels = json.loads(zf.read(label_name))
                rows = [json.loads(line) for line in zf.read(generation_name).decode().splitlines() if line.strip()]
                valid_labels = all(label in {'REFUSAL', 'COMPLIANCE', 'OTHER'} for label in labels)
                uids = [row.get('uid') for row in rows]
                binding = len(labels) == len(rows) and valid_labels
                counts = Counter(labels) if valid_labels else Counter()
                responses = [row.get('response', '') for row in rows]
                no_cue = None
                if cues and binding:
                    no_cue = sum(
                        label == 'REFUSAL' and not any(cue in response[:200].lower() for cue in cues)
                        for label, response in zip(labels, responses)
                    )
                groups[condition] = {
                    'rows': len(rows), 'labels': len(labels), 'label_binding': 'positional',
                    'schema_valid': binding, 'label_counts': dict(counts),
                    'refusal_rate_all_rows_unvalidated': counts.get('REFUSAL', 0) / len(rows) if rows else None,
                    'stored_rate_matches': (
                        abs(counts.get('REFUSAL', 0) / len(rows) - result.get('rates', {}).get(
                            {'A':'A_llm_text','B':'B_vlm_text','C':'C_vlm_vision','D':'D_vlm_blank','E':'E_vlm_phrase_text'}[condition], {}
                        ).get('rate', float('inf'))) < 1e-10 if rows and valid_labels and condition in 'ABCDE' else False
                    ),
                    'unique_uids': len(set(uids)), 'duplicate_uids': len(uids) - len(set(uids)),
                    'refusal_without_v2_cue_in_first_200': no_cue,
                }
                uid_sequences[condition] = uids
            models[model] = {
                'n_reported': result.get('n'), 'groups': groups,
                'A_to_E_uid_order_matches': bool(uid_sequences) and all(
                    seq == uid_sequences.get('A') for seq in uid_sequences.values()
                ),
                'contrasts_as_reported': result.get('contrasts', {}),
                'coupling_as_reported': result.get('coupling', {}),
                'benign_refusal_as_reported': result.get('over_refusal_benign', {}),
            }
        steering = json.loads(zf.read('steering.json')) if 'steering.json' in zf.namelist() else {}
        steering_summary = {}
        for model, record in steering.items():
            selected = {}
            for key, value in record.get('results', {}).items():
                if key.startswith(('text_harm|refusal|', 'vision_harm|refusal|', 'benign_text|refusal|',
                                   'text_harm|random|', 'vision_harm|random|', 'benign_text|random|')):
                    selected[key] = {'refusal_rate_unvalidated': value.get('refusal'), 'n': value.get('n')}
            steering_summary[model] = {'layer': record.get('layer'), 'n_layers': record.get('n_layers'),
                                       'results': selected}
        summary = {
            'archive': archive.name, 'archive_sha256': archive_hash, 'archive_bytes': len(raw),
            'snapshot_created_from': str(archive), 'version': meta.get('version'), 'meta': meta,
            'notebook_path': str(notebook) if notebook else None, 'notebook_sha256': notebook_hash,
            'notebook_refusal_cues_found': len(cues), 'zip_member_count': len(zf.namelist()),
            'models': models, 'steering': steering_summary,
            'interpretation_limits': [
                'Refusal labels are model-judge labels and are not human-validated safety or harmful-completion outcomes.',
                'Rows store UIDs and responses; separate label arrays bind by position and lack per-label response hashes.',
                'The results archive omits original item prompts/images, cache identity hashes, model revisions and exact runtime provenance.',
                'The contrasts and correlations are static condition comparisons; they do not by themselves estimate a seesaw caused by an intervention.',
                'Steering covers only the reported model, layer, sampled items and settings; no uncertainty intervals are supplied in this archive.',
            ],
        }
    run_dir = output_root / archive_hash[:16]
    run_dir.mkdir(parents=True, exist_ok=True)
    snapshot = run_dir / 'source_bundle.zip'
    if snapshot.exists() and sha256(snapshot.read_bytes()) != archive_hash:
        raise ValueError('Existing bundle snapshot hash mismatch.')
    if not snapshot.exists():
        shutil.copyfile(archive, snapshot)
    summary['snapshot_path'] = str(snapshot)
    (run_dir / 'audit.json').write_text(json.dumps(summary, indent=2) + '\n')
    index_path = output_root / 'index.json'
    index = json.loads(index_path.read_text()) if index_path.is_file() else {'runs': []}
    index['runs'] = [entry for entry in index.get('runs', []) if entry.get('archive_sha256') != archive_hash]
    index['runs'].append({key: summary[key] for key in ('archive','archive_sha256','version','snapshot_path')})
    index_path.write_text(json.dumps(index, indent=2) + '\n')
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--notebook', type=Path, help='Companion notebook used to audit its refusal-cue gate.')
    args = parser.parse_args()
    result = audit(args.archive.resolve(), args.notebook.resolve() if args.notebook else None)
    print(json.dumps({'archive_sha256': result['archive_sha256'], 'version': result['version'],
                      'models': list(result['models']), 'snapshot_path': result['snapshot_path']}, indent=2))


if __name__ == '__main__':
    main()
