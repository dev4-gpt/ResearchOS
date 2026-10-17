"""Install the pinned research-skill selection with the Codex skill installer.

Only copies package files. Never runs upstream installers, hooks, or skill scripts.
Re-running skips intact packages and refuses to overwrite modified documents.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installer', type=Path, default=Path.home() / '.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py')
    args = parser.parse_args()
    if not args.installer.is_file():
        parser.error('Codex skill installer not found; pass --installer with its path.')
    manifest = json.loads((ROOT / 'integrations/research_skills.json').read_text())
    for source in manifest['sources']:
        target = ROOT / manifest['install_root'] / source['id']
        selected = [skill for skill in manifest['skills'] if skill['source'] == source['id']]
        missing = []
        for skill in selected:
            package = target / skill['name']
            document = package / 'SKILL.md'
            if not package.exists():
                missing.append(skill['upstream_path'])
            elif not document.is_file() or hashlib.sha256(document.read_bytes()).hexdigest() != skill['sha256']:
                raise SystemExit(f"Refusing to overwrite modified/incomplete package: {package}")
        if missing:
            subprocess.run([sys.executable, str(args.installer), '--repo', source['repository'],
                            '--ref', source['revision'], '--dest', str(target), '--path', *missing], check=True)
        for skill in selected:
            document = target / skill['name'] / 'SKILL.md'
            if hashlib.sha256(document.read_bytes()).hexdigest() != skill['sha256']:
                raise SystemExit(f"Installed skill checksum mismatch: {skill['id']}")
        print(f"Verified {len(selected)} packages from {source['repository']} at {source['revision'][:12]}")


if __name__ == '__main__':
    main()
