"""Evidence review of imported TeX; does not compile or approve publication."""
import json
from pathlib import Path
import re

from services import paperorchestra as writer
from services.fact_checker import FactCheckerService
from services.research_engines import ROOT, digest, write_json

VAULT_PAPERS = ROOT / 'vault/01_Papers'
CITE = re.compile(r'\\(?:cite[a-zA-Z]*|autocite|parencite)\*?(?:\[[^\]]*\])*\{([^{}]+)\}')


def review(job_id, manuscript, mapping):
    manifest = writer.read_job(job_id)
    prefix = manifest.get('latest_intake')
    if not prefix or manuscript not in manifest['artifacts'] or not manuscript.startswith(prefix):
        raise ValueError('Select a TeX artifact from the latest intake')
    if not manuscript.endswith('.tex'):
        raise ValueError('Review requires a TeX manuscript')
    if not isinstance(mapping, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in mapping.items()):
        raise ValueError('Citation map must map BibTeX keys to exact vault paper filenames')
    root = writer.job_path(job_id)
    text = (root / manuscript).read_text()
    # TeX comments do not count as citations or evidence.
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    keys = {k.strip() for match in CITE.finditer(text) for k in match[1].split(',')}
    blockers, records, hashes = [], {}, {}
    if not keys:
        blockers.append('No manuscript citations found')
    for key in sorted(keys):
        filename = mapping.get(key, '')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+\.md', filename):
            blockers.append('Missing exact vault mapping: ' + key)
            continue
        path = VAULT_PAPERS / filename
        if path.is_symlink() or not path.is_file() or path.stat().st_size > writer.LIMIT:
            blockers.append('Missing or unsafe source: ' + key)
            continue
        body = path.read_text()
        if not re.search(r'^full_pdf_ingested:\s*true\s*$', body, re.M | re.I):
            blockers.append('Full-text ingestion not established: ' + key)
            continue
        records[Path(filename).stem] = body
        hashes[filename] = digest(path.read_bytes())
    def canonical(match):
        return ' '.join('[[' + Path(mapping[k.strip()]).stem + ']]' if k.strip() in mapping
                        else '[[' + k.strip() + ']]' for k in match[1].split(','))
    normalized = CITE.sub(canonical, text).replace(r'\%', '%')
    # Included files can carry unreviewed claims. A flattened manuscript must be
    # explicitly selected; never follow TeX file references on the host.
    if re.search(r'\\(?:input|include|write|openout|read|catcode|csname)\b', text):
        blockers.append('TeX includes or dynamic commands require manual review of a flattened manuscript')
    audit = FactCheckerService().audit_document(normalized, source_records=records, strict_evidence=True)
    blockers.extend(audit['blocking_errors'])
    report = {'job_id': job_id, 'manuscript': manuscript,
              'manuscript_sha256': manifest['artifacts'][manuscript],
              'source_hashes': hashes, 'citation_mapping': mapping, 'audit': audit,
              'status': 'blocked' if blockers else 'awaiting_human_review',
              'blocking_errors': blockers, 'publication_eligible': False,
              'remaining_reviews': ['Citation identity and entailment', 'Independent experiment replay',
                                    'Venue layout and compiled PDF', 'Human publication approval']}
    body = json.dumps(report, indent=2, allow_nan=False) + '\n'
    name = 'reviews/' + digest(body.encode()) + '.json'
    manifest['artifacts'].update(writer.persist(root, {name: body.encode()}))
    manifest.update(latest_review=name, status=report['status'], publication_eligible=False,
                    note='Evidence audit recorded; publication requires independent and human review.')
    write_json(root / 'manifest.json', manifest)
    return report
