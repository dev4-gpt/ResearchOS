#!/usr/bin/env python3
"""Offline release probes for the built IEEEtran and writer images."""
import argparse
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import uuid

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

from services.latex_exporter import LaTeXExporterService
from services.paperorchestra_worker import command, remove_container
from services.research_engines import digest, pinned_source
from services.tex_runtime import run_tex


def image_id(tag):
    return subprocess.check_output(['docker', 'image', 'inspect', '--format', '{{.Id}}', tag],
                                   text=True, timeout=10).strip()


def registered_containers():
    return set(subprocess.check_output(['docker', 'ps', '-aq'], text=True, timeout=10).split())


def ledger_state(path):
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as db:
        cap, reserved = db.execute('SELECT cap,reserved FROM budget WHERE id=1').fetchone()
    return {'cap_usd': cap / 1_000_000, 'reserved_usd': reserved / 1_000_000,
            'sha256': digest(path.read_bytes())}


def validate(tex, writer):
    ledger = ROOT / 'runs/service/validation-spend.sqlite3'
    before = ledger_state(ledger)
    containers = registered_containers()
    os.environ.update(RESEARCHINGOS_TEX_IMAGE=tex, RESEARCHINGOS_ACCESS_MODE='authenticated')
    latex = r"""
\documentclass[conference]{IEEEtran}
\begin{document}
\title{Release validation fixture}\author{ResearchingOS}\maketitle
Evidence appears here \cite{reference}.
\bibliographystyle{IEEEtran}\bibliography{references}
\end{document}
"""
    bibliography = '@article{reference,author={Operator},title={Synthetic reference},journal={Fixture},year={2024}}'
    exporter = LaTeXExporterService(None)
    pdf = exporter.compile_pdflatex(latex, bib_code=bibliography, allow_package_fallback=False)
    assert pdf, exporter.last_build_log[-3000:]
    pages = PdfReader(io.BytesIO(pdf)).pages
    assert len(pages) == 1 and '[1]' in pages[0].extract_text(), 'IEEEtran citation did not resolve'

    source, pin = pinned_source('paperorchestra')
    with tempfile.TemporaryDirectory(prefix='release-runtime.', dir=ROOT / '.tools') as folder:
        root = Path(folder)
        for directory in ('raw_materials', 'template', 'generated'):
            (root / directory).mkdir()
        try:
            run_tex(['sh', '-c', 'sleep 30'], root, timeout=1)
        except subprocess.TimeoutExpired:
            tex_timeout = True
        else:
            raise AssertionError('TeX compiler deadline did not trigger')

        spec = dict(id='release-runtime-probe', writer_model='gemini-2.5-flash',
                    reflection_model='gemini-2.5-flash', research_cutoff='2026-11')

        def writer_probe(*args, input=b''):
            name = 'researchingos-writer-' + uuid.uuid4().hex[:16]
            full = command(spec, root, source, writer, name, 15)
            image_index = full.index(writer)
            try:
                return subprocess.run(full[:image_index + 1] + list(args), input=input,
                                      capture_output=True, timeout=70)
            finally:
                assert remove_container(name), 'Writer probe container cleanup failed'

        help_probe = writer_probe('/opt/researchingos/writer_entrypoint.py', '--supervise', '60', '--help')
        help_output = help_probe.stdout + help_probe.stderr
        assert help_probe.returncode == 0 and b'--research_cutoff' in help_output, (help_probe.returncode, help_output[-2400:])
        probe_source = """
import json, os, pathlib, socket, sys
sys.path.insert(0, '/opt/researchingos')
import writer_entrypoint as entry
entry.init_transport()
from google import genai
from google.genai import types
import httpx
assert not {'GEMINI_API_KEY', 'OPENAI_API_KEY', 'SEMANTIC_SCHOLAR_API_KEY'} & set(os.environ)
try:
    socket.create_connection(('192.0.2.1', 443), 1)
except OSError:
    pass
else:
    raise RuntimeError('writer had an external route')
try:
    pathlib.Path('/probe').write_text('unexpected')
except OSError:
    pass
else:
    raise RuntimeError('writer had a writable root')
client = genai.Client(api_key='probe-only', http_options=types.HttpOptions(
    httpx_client=httpx.Client(transport=httpx.MockTransport(entry.relay), trust_env=False),
    retry_options=types.HttpRetryOptions(attempts=1)))
assert client.models.generate_content(model='gemini-2.5-flash', contents='Offline fixture').text == 'fixture'
"""
        reply = json.dumps({'candidates': [{'content': {'parts': [{'text': 'fixture'}]}}]}).encode() + b'\n'
        broker_probe = writer_probe('-c', probe_source, input=reply)
        assert broker_probe.returncode == 0, broker_probe.stderr[-1600:]
        request = json.loads(broker_probe.stdout)
        assert request['path'].endswith('gemini-2.5-flash:generateContent')
        writer_timeout = writer_probe('-c', "import sys; sys.path.insert(0, '/opt/researchingos'); "
            "from writer_entrypoint import supervise; "
            "raise SystemExit(supervise([sys.executable, '-c', 'import time; time.sleep(30)'], 1))")
        assert writer_timeout.returncode == 124

    after = ledger_state(ledger)
    assert before == after, 'Offline probes changed the spending ledger'
    assert registered_containers() == containers, 'Container inventory changed during probes'
    return {'tex_image_id': tex, 'writer_image_id': writer, 'writer_upstream_commit': pin['commit'],
            'ieeetran_pages': len(pages), 'ieeetran_citation_resolved': True, 'tex_timeout_cleanup': tex_timeout,
            'writer_cli_help': True, 'writer_sdk_stdio_roundtrip': True, 'writer_external_route_blocked': True,
            'writer_root_read_only': True, 'writer_credentials_absent': True, 'writer_timeout_cleanup': True,
            'container_inventory_unchanged': True, 'paid_provider_calls': 0, 'ledger': before,
            'scope': 'Built-image offline probes; provider-backed manuscript generation was not executed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tex', default='research-os-tex:release-validation')
    parser.add_argument('--writer', default='research-os-writer:release-validation')
    args = parser.parse_args()
    print(json.dumps(validate(image_id(args.tex), image_id(args.writer)), indent=2))


if __name__ == '__main__':
    main()
