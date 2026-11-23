"""Explicit, isolated PaperOrchestra execution. Never runs generated TeX on the host."""
from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
import uuid

from services import paperorchestra as writer
from services.paid_execution import ExecutionBudget
from services.research_engines import pinned_source, write_json
from services.spend_ledger import SpendLedger
from services.writer_broker import serve


def preflight(image: str):
    if os.getenv('PAPERORCHESTRA_ENABLED', '').lower() != 'true':
        raise RuntimeError('Set PAPERORCHESTRA_ENABLED=true explicitly')
    if not re.fullmatch(r'(?:[^\s]+@)?sha256:[a-f0-9]{64}', image):
        raise RuntimeError('PAPERORCHESTRA_IMAGE must be pinned by digest')
    if not os.getenv('GEMINI_API_KEY'):
        raise RuntimeError('A Gemini credential for the host broker is required')
    SpendLedger.configured()
    check = subprocess.run(['docker', 'image', 'inspect', image], capture_output=True, timeout=10)
    if check.returncode:
        raise RuntimeError('Writer image unavailable locally; no host execution fallback')


def command(manifest, root, source, image, name, seconds):
    # Paths are argv elements, never shell source. Only the job directory is writable.
    args = ['docker', 'run', '-i', '--pull=never', '--name', name, '--network=none',
            '--label', 'researchingos.paperorchestra=' + manifest['id'],
            '--log-driver=none', '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
            '--pids-limit=128', '--memory=4g', '--cpus=2',
            '--user', f'{os.getuid()}:{os.getgid()}',
            '--tmpfs', '/tmp:rw,nosuid,nodev,size=256m',
            '--mount', f'type=bind,src={source},dst=/upstream,readonly',
            '--mount', f'type=bind,src={root / "raw_materials"},dst=/materials,readonly',
            '--mount', f'type=bind,src={root / "template"},dst=/template,readonly',
            '--mount', f'type=bind,src={root / "generated"},dst=/output',
            '--workdir', '/upstream', '-e', 'HOME=/tmp', '-e', 'PYTHONDONTWRITEBYTECODE=1',
            '-e', 'shell_escape=f', '-e', 'openin_any=p', '-e', 'openout_any=p']
    args += ['--entrypoint', '/usr/local/bin/python', image, '/opt/researchingos/writer_entrypoint.py',
             '--supervise', str(seconds),
             '--raw_materials_dir', '/materials', '--latex_template_dir', '/template',
             '--output_dir', '/output', '--writer_model_name', manifest['writer_model'],
             '--reflection_model_name', manifest['reflection_model'],
             '--research_cutoff', manifest['research_cutoff'], '--use_plotting', 'false']
    return args


def remove_container(name, *, job_id=None):
    if not re.fullmatch(r'researchingos-writer-[0-9a-f]{16}', name or ''):
        return False
    try:
        if job_id:
            owner = subprocess.run(['docker', 'inspect', '--format',
                                    '{{index .Config.Labels "researchingos.paperorchestra"}}', name],
                                   capture_output=True, timeout=10)
            if owner.returncode:
                return b'No such object' in owner.stderr or b'No such container' in owner.stderr
            if owner.stdout.decode().strip() != job_id:
                return False
        result = subprocess.run(['docker', 'rm', '-f', name], capture_output=True, timeout=15)
        return result.returncode == 0 or b'No such container' in result.stderr
    except (OSError, subprocess.TimeoutExpired):
        return False


def output_size(root):
    total = 0
    for path in root.rglob('*'):
        if path.is_symlink():
            raise RuntimeError('Writer produced a symlink')
        if path.is_file():
            total += path.stat().st_size
    return total


def run(job_id: str, seconds: int = 1800):
    if type(seconds) is not int or not 1 <= seconds <= 7200:
        raise ValueError('Writer timeout must be 1..7200 seconds')
    root = writer.job_path(job_id)
    # OS lock is released on crash. Restarted running jobs are not silently rerun/billed.
    with (root / 'execution.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('Writer job is already running') from exc
        manifest = writer.read_job(job_id)
        if manifest['status'] == 'running':
            cleanup = remove_container(manifest.get('container'), job_id=job_id)
            manifest.update(status='interrupted' if cleanup else 'blocked', container_cleanup_verified=cleanup,
                            note='Recovered an interrupted writer without replay. Reconcile provider usage before retrying.')
            write_json(root / 'manifest.json', manifest)
            return manifest
        if manifest['status'] != 'prepared':
            raise ValueError('Only prepared jobs can execute; create a new job for a retry')
        models = {manifest['writer_model'], manifest['reflection_model']}
        allowed = {m.strip() for m in os.getenv('RESEARCHINGOS_GEMINI_APPROVED_MODELS', '').split(',')}
        if models != {'gemini-2.5-flash'} or not models <= allowed:
            raise RuntimeError('Writer and reflection require allowlisted Gemini 2.5 Flash')
        if not {'template/references.bib', 'template/citation_map.json'} <= set(manifest['artifacts']):
            raise RuntimeError('A reviewed references.bib and citation_map.json must be included in the frozen template')
        references = json.loads((root / 'template/citation_map.json').read_text())
        if not isinstance(references, dict) or not references or not (root / 'template/references.bib').read_text().strip():
            raise RuntimeError('The reviewed citation map and bibliography must be nonempty')
        image = os.getenv('PAPERORCHESTRA_IMAGE', '')
        preflight(image)
        source, pin = pinned_source('paperorchestra')
        if manifest['commit'] != pin['commit']:
            raise RuntimeError('Prepared source pin differs from installed source')
        output = root / 'generated'
        output.mkdir(exist_ok=False)
        name = 'researchingos-writer-' + uuid.uuid4().hex[:16]
        manifest.update(status='running', container=name, image=image,
                        timeout_seconds=seconds, note='Isolated writer running; output remains unverified.')
        write_json(root / 'manifest.json', manifest)
        child = None
        broker = None
        failure = []
        budget = ExecutionBudget(seconds)
        try:
            env = {key: value for key, value in os.environ.items() if key in {
                'PATH', 'HOME', 'DOCKER_HOST', 'DOCKER_CONTEXT'}}
            child = subprocess.Popen(command(manifest, root, source, image, name, seconds),
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
            broker = threading.Thread(target=serve, args=(child, models, budget, failure), daemon=True)
            broker.start()
            start = time.monotonic()
            while child.poll() is None:
                if time.monotonic() - start >= seconds:
                    raise TimeoutError('Writer wall-clock budget exhausted')
                if failure:
                    raise RuntimeError(failure[0])
                if output_size(output) > writer.LIMIT:
                    raise RuntimeError('Writer output budget exhausted')
                time.sleep(0.2)
            broker.join(timeout=1)
            if failure:
                raise RuntimeError(failure[0])
            if child.returncode in (124, 137):
                raise TimeoutError('Writer container deadline or resource limit exhausted')
            if child.returncode:
                raise RuntimeError('Writer process failed with exit code ' + str(child.returncode))
            if output_size(output) > writer.LIMIT:
                raise RuntimeError('Writer output budget exhausted')
            # Upstream may exit zero after a failed pipeline. Require concrete output.
            if not any(p.stat().st_size for p in output.rglob('*.pdf') if p.is_file()):
                raise RuntimeError('Writer exited without a PDF')
            manifest = writer.intake(job_id, output)
            manifest.update(generation_executed=True, image=image,
                            note='Isolated generation completed. Citation, claim and venue review required.')
        except (Exception, KeyboardInterrupt) as exc:
            manifest.update(status='cancelled' if isinstance(exc, KeyboardInterrupt) else
                            'timed_out' if isinstance(exc, TimeoutError) else 'failed',
                            generation_executed=False, note=str(exc), publication_eligible=False)
        finally:
            manifest['container_cleanup_verified'] = remove_container(name)
            if not manifest['container_cleanup_verified']:
                manifest.update(status='blocked', note='Container cleanup unverified; inspect container ' + name)
            if child is not None and child.poll() is None:
                child.kill()
                child.wait(timeout=5)
            if broker:
                broker.join(timeout=1)
            if child is not None and (not broker or not broker.is_alive()):
                child.stdin.close()
                child.stdout.close()
            write_json(root / 'manifest.json', manifest)
        return manifest
