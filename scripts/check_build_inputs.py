#!/usr/bin/env python3
"""Check release build declarations without downloads or executing upstream code."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    root = Path(root)
    errors = []
    for name in ('backend/uv.lock', 'frontend/package-lock.json',
                 'integrations/research_engines.lock.json'):
        if not (root / name).is_file():
            errors.append(f'Missing build input: {name}')
    runtime = root / 'deploy/runtime'
    locked = {}
    body = (runtime / 'writer-requirements.lock').read_text()
    for line in body.replace('\\\n', ' ').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        requirement = Requirement(line.split('--hash=')[0].strip())
        specs = list(requirement.specifier)
        if requirement.url or len(specs) != 1 or specs[0].operator != '==' or '*' in specs[0].version:
            errors.append(f'Writer dependency is not exactly pinned: {requirement.name}')
        elif not re.search(r'--hash=sha256:[a-f0-9]{64}(?:\s|$)', line):
            errors.append(f'Writer dependency lacks a SHA-256: {requirement.name}')
        else:
            locked.setdefault(canonicalize_name(requirement.name), []).append(specs[0].version)
    for line in (runtime / 'writer-requirements.in').read_text().splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        req = Requirement(line)
        versions = locked.get(canonicalize_name(req.name), [])
        if req.url or not versions or any(v not in req.specifier for v in versions):
            errors.append(f'Writer lock does not satisfy input: {req.name}')
    for name in ('tex.Dockerfile', 'writer.Dockerfile'):
        text = (runtime / name).read_text()
        bases = re.findall(r'^FROM\s+(\S+)', text, re.MULTILINE | re.IGNORECASE)
        if not bases or any(not re.fullmatch(r'[^\s]+@sha256:[a-f0-9]{64}', b) for b in bases):
            errors.append(f'Docker base must use a digest: {name}')
    dockerfile = (runtime / 'writer.Dockerfile').read_text()
    if '--require-hashes' not in dockerfile or 'COPY writer-requirements.lock' not in dockerfile:
        errors.append('Writer Docker build must consume the hashed lock')
    source_lock = root / 'integrations/research_engines.lock.json'
    if source_lock.is_file():
        data = json.loads(source_lock.read_text())
        if data.get('schema_version') != 1 or not data.get('engines'):
            errors.append('Invalid engine source lock schema')
        for name, engine in data.get('engines', {}).items():
            if not re.fullmatch(r'[a-f0-9]{40}', engine.get('commit', '')):
                errors.append(f'Engine commit must be immutable: {name}')
            if not re.fullmatch(r'[\w.-]+/[\w.-]+', engine.get('repository', '')):
                errors.append(f'Invalid engine repository: {name}')
            if not engine.get('files'):
                errors.append(f'No pinned engine files: {name}')
            for path, blob in engine.get('files', {}).items():
                if PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts or '\\' in path:
                    errors.append(f'Unsafe engine path: {name}/{path}')
                if not re.fullmatch(r'[a-f0-9]{40}', blob):
                    errors.append(f'Invalid Git blob hash: {name}/{path}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        failures = check(args.root)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        failures = [f'Invalid build declaration: {exc}']
    print(json.dumps({'passed': not failures, 'errors': failures}, indent=2))
    raise SystemExit(bool(failures))
