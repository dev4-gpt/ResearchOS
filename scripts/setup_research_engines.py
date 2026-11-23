#!/usr/bin/env python3
"""Download only locked UTF-8 upstream sources, verifying Git blob hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    lock = json.loads((ROOT / 'integrations/research_engines.lock.json').read_text())
    failures = []
    for name, engine in lock['engines'].items():
        for relative, expected in engine['files'].items():
            target = ROOT / '.tools/research-engines' / name / relative
            if not args.check and not target.exists():
                url = f"https://raw.githubusercontent.com/{engine['repository']}/{engine['commit']}/{relative}"
                with urllib.request.urlopen(url, timeout=30) as response:
                    body = response.read()
                if hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() != expected:
                    raise ValueError(f'Upstream hash mismatch: {relative}')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(body)
            body = target.read_bytes() if target.is_file() and not target.is_symlink() else b''
            if hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() != expected:
                failures.append(f'{name}/{relative}')
    print('Verified pinned engine sources' if not failures else 'Missing or modified: ' + ', '.join(failures))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
