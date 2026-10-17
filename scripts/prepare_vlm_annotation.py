"""Create separate, blinded and restricted annotation files from a completed v3 run.

This utility reads local v3 outputs. It never sends data to a provider. Only share
for_annotators/annotation_packet.csv; keep restricted/ private until labels lock.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import uuid

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / '.tools/vlm-research/annotations'


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))


def read_generations(path: Path) -> dict[str, str]:
    records: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        uid, response = row.get('uid'), row.get('response')
        if not isinstance(uid, str) or not isinstance(response, str):
            raise ValueError(f'{path.name}:{line_number} has an invalid response record.')
        if uid in records:
            raise ValueError(f'{path.name} contains duplicate item uid {uid!r}.')
        records[uid] = response
    return records


def prepare(run_dir: Path, output_root: Path = DEFAULT_OUTPUT) -> dict:
    run_dir = run_dir.resolve()
    blinded_path = run_dir / 'audit_blinded.csv'
    key_path = run_dir / 'audit_key.csv'
    results_path = run_dir / 'results.json'
    for path in (blinded_path, key_path, results_path):
        if not path.is_file():
            raise FileNotFoundError(f'Required v3 artifact is missing: {path.name}')

    blinded = read_csv(blinded_path)
    source_key = read_csv(key_path)
    if not blinded or not source_key:
        raise ValueError('The blinded sample and annotation key must both contain rows.')
    if not {'row_id', 'request', 'response', 'human'} <= set(blinded[0]):
        raise ValueError('audit_blinded.csv has an unexpected schema.')
    if not {'row_id', 'model', 'cond', 'uid', 'response_file', 'response_sha256'} <= set(source_key[0]):
        raise ValueError('audit_key.csv has an unexpected schema.')

    blind_by_id = {row['row_id']: row for row in blinded}
    key_by_id = {row['row_id']: row for row in source_key}
    if len(blind_by_id) != len(blinded) or len(key_by_id) != len(source_key):
        raise ValueError('Duplicate row_id found in the audit files.')
    if set(blind_by_id) != set(key_by_id):
        raise ValueError('The blinded sample and key row_id sets do not match exactly.')

    results = json.loads(results_path.read_text(encoding='utf-8'))
    meta = results.get('meta', {})
    if meta.get('version') != 'v3':
        raise ValueError('Expected a completed v3 results.json.')
    results_hash = hashlib.sha256(results_path.read_bytes()).hexdigest()
    run_token = f"v3-{meta.get('date', 'undated')}-{results_hash[:12]}"
    target = output_root / run_token
    packet_dir = target / 'for_annotators'
    restricted_dir = target / 'restricted'
    packet_dir.mkdir(parents=True, exist_ok=False, mode=0o700)
    restricted_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(target, 0o700); os.chmod(packet_dir, 0o700); os.chmod(restricted_dir, 0o700)

    packet_rows = []
    key_rows = []
    generation_cache: dict[tuple[str, str, str], dict[str, str]] = {}
    seen_blind_row_ids = set()
    for source_id, blind in blind_by_id.items():
        source = key_by_id[source_id]
        condition = source['cond']
        model = source['model']
        uid = source['uid']
        if condition not in {'A', 'B', 'C', 'D', 'E'}:
            raise ValueError(f'Unexpected condition in harmful audit sample: {condition!r}')
        tag = re.sub(r'[^A-Za-z0-9]+', '_', model)
        generation_file = source['response_file']
        if not generation_file or Path(generation_file).name != generation_file or not generation_file.startswith(f'gen_{tag}__'):
            raise ValueError(f'Invalid response cache path for audit row {source_id}.')
        gen_path = (run_dir / generation_file).resolve()
        if gen_path.parent != run_dir:
            raise ValueError(f'Response cache path escapes the frozen run for audit row {source_id}.')
        cache_key = (model, condition, generation_file)
        if cache_key not in generation_cache:
            if not gen_path.is_file():
                raise FileNotFoundError(f'Full, untruncated response file is missing: {gen_path.name}')
            generation_cache[cache_key] = read_generations(gen_path)
        full_response = generation_cache[cache_key].get(uid)
        if full_response is None:
            raise ValueError(f'Could not find the full response for audit row {source_id}.')
        if sha256(full_response) != source['response_sha256']:
            raise ValueError(f'Response hash mismatch for audit row {source_id}; refusing to join.')
        # v3 exports the complete response with line breaks normalized for CSV.
        if full_response.replace('\r', ' ').replace('\n', ' ') != blind['response']:
            raise ValueError(f'Full response mismatch for audit row {source_id}; refusing to join.')
        if not blind['request'].strip():
            raise ValueError(f'Missing request context for audit row {source_id}.')

        opaque_id = uuid.uuid4().hex
        while opaque_id in seen_blind_row_ids:
            opaque_id = uuid.uuid4().hex
        seen_blind_row_ids.add(opaque_id)
        packet_rows.append({'row_id': opaque_id, 'request_text': blind['request'],
                            'response_text': full_response, 'task_type': 'harmful',
                            'human_label': '', 'rationale': ''})
        key = {'row_id': opaque_id, 'source_row_id': source_id, 'item_uid': uid,
               'model_id': model, 'condition': condition,
               'request_sha256': sha256(blind['request']),
               'response_sha256': sha256(full_response),
               'run_manifest_sha256': results_hash}
        key.update({name: value for name, value in source.items() if name.startswith('judge_')})
        key_rows.append(key)

    # Shuffle independently so original sample ordering cannot reveal the key order.
    secrets.SystemRandom().shuffle(packet_rows)
    secrets.SystemRandom().shuffle(key_rows)
    packet_file = packet_dir / 'annotation_packet.csv'
    restricted_key = restricted_dir / 'annotation_key.csv'
    with packet_file.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(packet_rows[0]))
        writer.writeheader(); writer.writerows(packet_rows)
    with restricted_key.open('w', newline='', encoding='utf-8') as handle:
        fields = list(key_rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(key_rows)
    os.chmod(packet_file, 0o600); os.chmod(restricted_key, 0o600)
    manifest = {'project_id': 'vlm-safety', 'source_run_dir': str(run_dir),
                'source_results_sha256': results_hash, 'source_results_meta': meta,
                'rows': len(packet_rows), 'packet_path': str(packet_file),
                'restricted_key_path': str(restricted_key),
                'sharing_rule': 'Share only packet_path. Keep the restricted key private until labels lock.'}
    manifest_path = restricted_dir / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    os.chmod(manifest_path, 0o600)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir', type=Path, help='Local completed v3 OUT_DIR containing audit and generation files')
    parser.add_argument('--output-root', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(prepare(args.run_dir, args.output_root), indent=2))


if __name__ == '__main__':
    main()
