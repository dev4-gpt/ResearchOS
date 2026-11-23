"""Compile untrusted TeX in a networkless container in authenticated deployments."""
import os
from pathlib import Path
import re
import subprocess
import uuid


def isolated():
    return os.getenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated') != 'local'


def run_tex(args, directory, timeout=30):
    if not isolated():
        return subprocess.run(args, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    image = os.getenv('RESEARCHINGOS_TEX_IMAGE', '')
    if not re.fullmatch(r'(?:[^\s]+@)?sha256:[a-f0-9]{64}', image):
        raise RuntimeError('Set RESEARCHINGOS_TEX_IMAGE to a locally available digest-pinned TeX image')
    directory = str(Path(directory).resolve())
    inner = [Path(args[0]).name] + [str(arg).replace(directory, '/work') for arg in args[1:]]
    name = 'researchingos-tex-' + uuid.uuid4().hex
    command = ['docker', 'run', '--rm', '--pull=never', '--name', name, '--network=none',
               '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
               '--memory=512m', '--cpus=1', '--pids-limit=64', '--log-driver=none',
               '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,nosuid,nodev,size=64m',
               '--mount', f'type=bind,src={directory},dst=/work', '--workdir', '/work',
               '-e', 'HOME=/tmp', '-e', 'openin_any=p', '-e', 'openout_any=p',
               '--entrypoint', inner[0], image, *inner[1:]]
    try:
        # Stream compiler logs to a temporary file rather than unbounded host RAM.
        import tempfile
        with tempfile.TemporaryFile() as log:
            completed = subprocess.run(command, stdout=log, stderr=log, timeout=timeout)
            log.seek(0)
            return subprocess.CompletedProcess(command, completed.returncode, log.read(1_000_000), b'')
    finally:
        cleanup = subprocess.run(['docker', 'rm', '-f', name], capture_output=True, timeout=10)
        if cleanup.returncode and b'No such container' not in cleanup.stderr:
            raise RuntimeError('TeX container cleanup could not be verified')
