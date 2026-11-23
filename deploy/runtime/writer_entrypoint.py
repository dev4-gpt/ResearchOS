"""Execute pinned PaperOrchestra using a parent-owned Gemini RPC transport."""
import json
import multiprocessing
import os
from pathlib import Path
import runpy
import shutil
import signal
import subprocess
import sys

import httpx
from google import genai
from google.genai import types

MAX_FRAME = 8_000_000
rpc_lock = rpc_input = rpc_output = None


def init_transport():
    global rpc_lock, rpc_input, rpc_output
    rpc_lock = multiprocessing.Lock()
    rpc_input = os.fdopen(os.dup(0), 'rb')
    rpc_output = os.fdopen(os.dup(1), 'wb')
    os.dup2(2, 1)


def supervise(command, seconds):
    # Keep the hard deadline inside the container so loss of the host worker
    # cannot leave the upstream Python process or its children running.
    with subprocess.Popen(command, start_new_session=True) as child:
        try:
            return child.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
            return 124


def relay(request):
    if request.method != 'POST':
        raise RuntimeError('Only bounded generation is available')
    payload = json.dumps({'path': request.url.path, 'body': json.loads(request.content)}).encode()
    if len(payload) >= MAX_FRAME:
        raise ValueError('Writer request exceeds broker frame limit')
    with rpc_lock:
        rpc_output.write(payload + b'\n')
        rpc_output.flush()
        reply = rpc_input.readline(MAX_FRAME + 1)
    if not reply.endswith(b'\n') or len(reply) > MAX_FRAME:
        raise RuntimeError('Writer broker closed')
    return httpx.Response(200, json=json.loads(reply))


def use_reviewed_sources(agent, outline_path, cutoff_date=None):
    destination = Path(agent.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    for source, target in (
        (Path(outline_path), 'outline_v1.json'),
        (Path('/template/template.tex'), 'updated_template.tex'),
        (Path('/template/references.bib'), 'references.bib'),
        (Path('/template/citation_map.json'), 'citation_map.json'),
    ):
        shutil.copyfile(source, destination / target)


def main():
    init_transport()
    sys.path.insert(0, '/upstream')
    from utils import gemini_utils
    from methods.agents.literature_review_agent import HybridLiteratureAgent

    def client():
        if gemini_utils._genai_client is None:
            gemini_utils._genai_client = genai.Client(api_key='host-broker', http_options=types.HttpOptions(
                httpx_client=httpx.Client(transport=httpx.MockTransport(relay), trust_env=False),
                retry_options=types.HttpRetryOptions(attempts=1)))
        return gemini_utils._genai_client

    gemini_utils.get_genai_client = client
    HybridLiteratureAgent.run = use_reviewed_sources
    sys.argv[0] = '/upstream/paper_writing_cli.py'
    runpy.run_path(sys.argv[0], run_name='__main__')


if __name__ == '__main__':
    if sys.argv[1:2] == ['--supervise']:
        seconds = int(sys.argv[2])
        if not 1 <= seconds <= 7200:
            raise ValueError('Expected a 1..7200 second deadline')
        raise SystemExit(supervise([sys.executable, __file__, *sys.argv[3:]], seconds))
    main()
