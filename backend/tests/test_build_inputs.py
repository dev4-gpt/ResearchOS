"""Reject release declarations that would silently float or escape build roots."""
import importlib.util
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('check_build_inputs', ROOT / 'scripts/check_build_inputs.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


@pytest.fixture
def build_root(tmp_path):
    for relative in ('deploy/runtime', 'integrations'):
        shutil.copytree(ROOT / relative, tmp_path / relative)
    for relative in ('backend/uv.lock', 'frontend/package-lock.json'):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    return tmp_path


def test_current_build_declarations_pass():
    assert audit.check(ROOT) == []


@pytest.mark.parametrize('relative,before,after,expected', [
    ('deploy/runtime/writer-requirements.in', 'google-genai==2.17.0', 'google-genai==0.0.1', 'does not satisfy'),
    ('deploy/runtime/tex.Dockerfile', 'FROM texlive/texlive@sha256:', 'FROM texlive/texlive:', 'base must use a digest'),
    ('integrations/research_engines.lock.json', '"LICENSE":', '"../LICENSE":', 'Unsafe engine path'),
    ('deploy/runtime/writer.Dockerfile', '--require-hashes', '', 'must consume the hashed lock'),
])
def test_rejects_drift_and_unsafe_inputs(build_root, relative, before, after, expected):
    path = build_root / relative
    assert before in path.read_text()
    path.write_text(path.read_text().replace(before, after))
    assert any(expected in error for error in audit.check(build_root))


def test_rejects_unhashed_writer_dependency(build_root):
    path = build_root / 'deploy/runtime/writer-requirements.lock'
    path.write_text(path.read_text() + '\nunhashed-package==1.0\n')
    assert any('lacks a SHA-256' in error for error in audit.check(build_root))
