#!/usr/bin/env python3
"""Copy and restore vault/run data in isolation; never overwrite the source."""
import argparse
from contextlib import ExitStack
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import time


def inventory(root):
    result = {}
    for name in ('vault', 'runs'):
        base = root / name
        if not base.is_dir():
            raise RuntimeError(f'Missing source directory: {name}')
        for path in sorted(base.rglob('*')):
            if path.is_symlink():
                raise RuntimeError('Symlink encountered; review backup scope before proceeding')
            if path.is_file() and not path.name.endswith('.lock'):
                h = hashlib.sha256()
                with path.open('rb') as handle:
                    for block in iter(lambda: handle.read(1024 * 1024), b''): h.update(block)
                result[str(path.relative_to(root))] = {'sha256': h.hexdigest(), 'bytes': path.stat().st_size}
    return result


def verify_databases(root, manifest):
    results = {}
    for relative in manifest:
        if relative.endswith(('.sqlite3', '.sqlite', '.db')):
            path = root / relative
            with sqlite3.connect(f'{path.as_uri()}?mode=ro', uri=True) as db:
                integrity = db.execute('PRAGMA integrity_check').fetchall()
                if integrity != [('ok',)]: raise RuntimeError('Restored SQLite integrity check failed')
                tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                result = {'integrity': 'ok'}
                if 'jobs' in tables:
                    result['states'] = dict(db.execute('SELECT status,count(*) FROM jobs GROUP BY status'))
                if 'budget' in tables:
                    budget = db.execute('SELECT cap,reserved FROM budget WHERE id=1').fetchone()
                    if not budget or not 0 <= budget[1] <= budget[0]:
                        raise RuntimeError('Restored spending ledger has invalid totals')
                    result.update(cap_usd=budget[0] / 1_000_000, reserved_usd=budget[1] / 1_000_000)
                results[relative] = result
    return results


def drill(root, scratch):
    root, scratch = Path(root).resolve(), Path(scratch).resolve()
    if scratch == root or any(source == scratch or source in scratch.parents
                              for source in (root / 'vault', root / 'runs')):
        raise ValueError('Restore scratch must be outside the source vault and run directories')
    started = time.monotonic()
    with ExitStack() as stack:
        locks = [root / 'vault/.write.lock']
        locks += list((root / 'runs').rglob('*.worker.lock'))
        for path in locks:
            handle = stack.enter_context(path.open('a'))
            try: fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError: raise RuntimeError('Stop active workers/writers before taking a snapshot')
        before = inventory(root)
        with tempfile.TemporaryDirectory(prefix='researchingos-restore-', dir=scratch) as folder:
            snapshot, restored = Path(folder) / 'snapshot', Path(folder) / 'restored'
            snapshot.mkdir(mode=0o700); restored.mkdir(mode=0o700)
            for name in ('vault', 'runs'): (snapshot / name).mkdir()
            for relative in before:
                target = snapshot / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / relative, target)
                target.chmod(0o600)
            if inventory(root) != before or inventory(snapshot) != before:
                raise RuntimeError('Source changed during snapshot; stop all CLI writers and retry')
            for name in ('vault', 'runs'):
                shutil.copytree(snapshot / name, restored / name)
            if inventory(restored) != before: raise RuntimeError('Restored content hashes differ')
            databases = verify_databases(restored, before)
            return {'passed': True, 'files_verified': len(before),
                    'bytes_verified': sum(v['bytes'] for v in before.values()),
                    'seconds': round(time.monotonic() - started, 3), 'databases': databases,
                    'scope': 'Local isolated vault and runs restore; not off-host disaster recovery',
                    'missing_release_evidence': ['Encrypted off-host backup', 'Deployment configuration and secret restoration',
                        'Application startup from restored production state', 'Measured off-host RPO/RTO'],
                    'temporary_copies_removed_on_exit': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--scratch', type=Path, default=Path('/tmp'))
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = drill(args.root, args.scratch)
    if args.report: args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
