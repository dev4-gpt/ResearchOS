import json
from pathlib import Path
import subprocess
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services import paperorchestra as writer
from services.research_engines import pinned_source
from paperorchestra_api import router


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    monkeypatch.setattr(writer, 'JOBS', tmp_path / 'jobs')
    # Pin verification is separately exercised against the actual downloaded source.
    monkeypatch.setattr(writer, 'pinned_source', lambda engine: (tmp_path / 'upstream', {'repository':'google-research/paper-orchestra','commit':'a'*40}))
    raw = tmp_path / 'materials'; raw.mkdir()
    (raw / 'idea_sparse.md').write_text('A synthetic integration fixture; not a scientific finding.')
    (raw / 'experimental_log.md').write_text('No experiments performed. Do not invent results.')
    (raw / 'unrelated.md').write_text('Do not send this.')
    template = tmp_path / 'template'; template.mkdir()
    (template / 'template.tex').write_text('\\documentclass{article}\n')
    (template / 'guidelines.md').write_text('Test template only.')
    return raw, template


def prepare(inputs):
    return writer.prepare(*inputs, 'test-writer', 'test-reflector', '2026-11')


def test_prepare_contract_and_no_execution(inputs):
    m = prepare(inputs)
    assert m['status'] == 'prepared' and not m['generation_executed']
    assert m['argv'][-2:] == ['--use_plotting', 'false']
    assert 'raw_materials/unrelated.md' not in m['artifacts']
    assert 'raw_materials/figures/info.json' in m['artifacts']
    assert not writer.read_job(m['id'])['publication_eligible']


def test_missing_material_and_template(inputs):
    raw, template = inputs
    (raw / 'experimental_log.md').unlink()
    with pytest.raises(ValueError, match='experimental_log'): prepare(inputs)
    (raw / 'experimental_log.md').write_text('No results')
    (template / 'guidelines.md').unlink()
    with pytest.raises(ValueError, match='guidelines'): prepare(inputs)


def test_changed_artifact_and_symlink(inputs, tmp_path):
    m = prepare(inputs)
    (writer.job_path(m['id']) / 'raw_materials/idea_sparse.md').write_text('altered')
    with pytest.raises(ValueError, match='integrity'): writer.read_job(m['id'])
    (inputs[0] / 'escape.md').symlink_to(tmp_path / 'outside')
    with pytest.raises(ValueError, match='Symlinks'): prepare(inputs)
    with pytest.raises(ValueError): writer.job_path('../escape')


def test_intake_remains_unverified_and_does_not_execute_tex(inputs, tmp_path):
    m = prepare(inputs)
    output = tmp_path / 'output'; output.mkdir()
    (output / 'draft.tex').write_text('\\cite{unverified_reference} N=9999. \\input{/etc/passwd}')
    (output / 'run.py').write_text('raise Exception("must not execute")')
    imported = writer.intake(m['id'], output)
    assert imported['status'] == 'awaiting_review'
    assert not imported['publication_eligible'] and not imported['generation_executed']
    assert not any(k.endswith('run.py') for k in imported['artifacts'])
    again = writer.intake(m['id'], output)
    assert again['latest_intake'] != imported['latest_intake']
    assert len(again['artifacts']) == len(imported['artifacts']) + 1


def test_pdf_alone_rejected(inputs, tmp_path):
    m = prepare(inputs)
    output = tmp_path / 'output'; output.mkdir(); (output / 'paper.pdf').write_bytes(b'%PDF')
    with pytest.raises(ValueError, match='LaTeX'): writer.intake(m['id'], output)


def test_read_only_api(inputs):
    m = prepare(inputs)
    app = FastAPI(); app.include_router(router); client = TestClient(app)
    assert client.get('/api/paperorchestra/jobs').json()['jobs'][0]['status'] == 'prepared'
    assert client.get('/api/paperorchestra/jobs/' + m['id']).status_code == 200
    assert client.post('/api/paperorchestra/jobs').status_code == 405
    assert client.get('/api/paperorchestra/jobs/missing').status_code == 409


def test_real_upstream_cli_contract():
    try: source, pin = pinned_source('paperorchestra')
    except RuntimeError: pytest.skip('Download pinned upstream first')
    p = subprocess.run([sys.executable, str(source / 'paper_writing_cli.py'), '--help'], capture_output=True, text=True, timeout=10)
    assert p.returncode == 0
    for flag in ('--raw_materials_dir', '--latex_template_dir', '--writer_model_name', '--reflection_model_name', '--use_plotting', '--research_cutoff'):
        assert flag in p.stdout
