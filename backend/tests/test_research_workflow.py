import json
import io
from itertools import chain, repeat
import subprocess
from types import SimpleNamespace

import pytest

from services import paperorchestra as writer
from services import paperorchestra_worker as worker
from services import paperorchestra_review as review
from services import research_workflow as flow


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    monkeypatch.setattr(writer, 'JOBS', tmp_path / 'jobs')
    monkeypatch.setattr(flow, 'WORKFLOWS', tmp_path / 'workflows')
    pin = lambda _: (tmp_path / 'source', {'repository': 'google-research/paper-orchestra', 'commit': 'a'*40})
    monkeypatch.setattr(writer, 'pinned_source', pin)
    monkeypatch.setattr(worker, 'pinned_source', pin)
    materials = tmp_path / 'materials'; materials.mkdir()
    (materials / 'idea_sparse.md').write_text('Integration test only')
    (materials / 'experimental_log.md').write_text('No empirical results')
    template = tmp_path / 'template'; template.mkdir()
    (template / 'template.tex').write_text('\\documentclass{article}')
    (template / 'guidelines.md').write_text('Test only')
    (template / 'references.bib').write_text('@article{fixture,title={Synthetic fixture}}')
    (template / 'citation_map.json').write_text('{"fixture": {"title": "Synthetic fixture"}}')
    monkeypatch.setenv('RESEARCHINGOS_GEMINI_APPROVED_MODELS', 'gemini-2.5-flash')
    return flow.WorkflowSpec(query='test discovery', materials=materials, template=template,
                             writer_model='gemini-2.5-flash', reflection_model='gemini-2.5-flash', cutoff='2026-11')


def test_workflow_resumes_without_repeating_completed_calls(bundle, monkeypatch):
    calls = []
    monkeypatch.setattr(flow.OpenResearchService, 'discover', lambda self, q: calls.append(q) or [{'id':'test'}])
    record = flow.create(bundle)
    assert flow.resume(record['id'])['status'] == 'prepared_for_writing'
    assert flow.resume(record['id'])['status'] == 'prepared_for_writing'
    assert calls == ['test discovery']


def test_failed_stage_is_not_automatically_rebilled(bundle, monkeypatch):
    calls = []
    def fail(self, query):
        calls.append(query)
        raise RuntimeError('offline')
    monkeypatch.setattr(flow.OpenResearchService, 'discover', fail)
    record = flow.create(bundle)
    assert flow.resume(record['id'])['status'] == 'blocked'
    assert flow.resume(record['id'])['status'] == 'blocked'
    assert len(calls) == 1


def test_changed_spec_is_rejected(bundle):
    record = flow.create(bundle)
    (flow.WORKFLOWS / record['id'] / 'spec.json').write_text('{}')
    with pytest.raises(ValueError, match='changed'):
        flow.resume(record['id'])


def test_live_dataset_required(bundle):
    from domain.research_experiments import ExperimentSpec
    bundle.experiments = [ExperimentSpec(engine='harness2', mode='live', model='test')]
    with pytest.raises(ValueError, match='explicit reviewed dataset'):
        flow.create(bundle)


def test_writer_command_isolated_and_no_secret_values(bundle, monkeypatch):
    record = flow.create(bundle)
    manifest = writer.read_job(record['job_id'])
    monkeypatch.setenv('GEMINI_API_KEY', 'test-secret-value')
    cmd = worker.command(manifest, writer.job_path(record['job_id']), '/source', 'image@sha256:'+'a'*64, 'test', 30)
    assert 'test-secret-value' not in ' '.join(cmd)
    for flag in ('--read-only', '--cap-drop=ALL', '--log-driver=none', '--pull=never', '--network=none'):
        assert flag in cmd
    assert cmd[-2:] == ['--use_plotting', 'false']
    assert not any('docker.sock' in value for value in cmd)
    assert 'GEMINI_API_KEY' not in cmd


def mock_runtime(monkeypatch, on_start):
    monkeypatch.setattr(worker, 'preflight', lambda _: None)
    monkeypatch.setattr(worker.subprocess, 'run', lambda *a, **kw: SimpleNamespace(returncode=0))
    class Process:
        returncode = 0
        def __init__(self, *args, **kwargs):
            assert kwargs['stdin'] == kwargs['stdout'] == subprocess.PIPE
            self.stdin, self.stdout = io.BytesIO(), io.BytesIO()
            on_start()
        def poll(self): return 0
    monkeypatch.setattr(worker.subprocess, 'Popen', Process)


def test_zero_exit_without_output_fails(bundle, monkeypatch):
    job = flow.create(bundle)['job_id']
    mock_runtime(monkeypatch, lambda: None)
    result = worker.run(job)
    assert result['status'] == 'failed'
    assert 'without a PDF' in result['note']
    assert not result['generation_executed']
    with pytest.raises(ValueError, match='prepared'):
        worker.run(job)


def test_isolated_generation_intake_and_workflow_resume(bundle, monkeypatch):
    bundle.generate = True
    record = flow.create(bundle)
    monkeypatch.setattr(flow.OpenResearchService, 'discover', lambda self, q: [])
    def produce():
        output = writer.job_path(record['job_id']) / 'generated'
        (output / 'paper.tex').write_text('Unverified manuscript')
        (output / 'paper.pdf').write_bytes(b'%PDF-test')
    mock_runtime(monkeypatch, produce)
    result = flow.resume(record['id'])
    assert result['status'] == 'awaiting_review'
    manifest = writer.read_job(record['job_id'])
    assert manifest['generation_executed'] and not manifest['publication_eligible']
    assert flow.resume(record['id'])['status'] == 'awaiting_review'


def test_review_requires_fulltext_and_claim_support(bundle, tmp_path, monkeypatch):
    job = flow.create(bundle)['job_id']
    output = tmp_path / 'output'; output.mkdir()
    (output / 'paper.tex').write_text(r'We achieved 99\% accuracy. \citep{smith2020}')
    manifest = writer.intake(job, output)
    vault = tmp_path / 'papers'; vault.mkdir()
    monkeypatch.setattr(review, 'VAULT_PAPERS', vault)
    (vault / 'source.md').write_text('---\nfull_pdf_ingested: true\n---\nUnrelated findings.')
    report = review.review(job, manifest['latest_intake'] + 'paper.tex', {'smith2020': 'source.md'})
    assert report['status'] == 'blocked'
    assert not report['publication_eligible']
    assert report['source_hashes']
    assert writer.read_job(job)['latest_review']


def test_review_never_follows_tex_includes(bundle, tmp_path, monkeypatch):
    job = flow.create(bundle)['job_id']
    output = tmp_path / 'output'; output.mkdir()
    (output / 'paper.tex').write_text('\\input{/etc/passwd}')
    manifest = writer.intake(job, output)
    report = review.review(job, manifest['latest_intake'] + 'paper.tex', {})
    assert report['status'] == 'blocked'
    assert any('flattened' in b for b in report['blocking_errors'])
    with pytest.raises(ValueError): review.review(job, '../../escape.tex', {})


def test_disabled_writer_does_not_start(bundle, monkeypatch):
    monkeypatch.delenv('PAPERORCHESTRA_ENABLED', raising=False)
    job = flow.create(bundle)['job_id']
    with pytest.raises(RuntimeError, match='PAPERORCHESTRA_ENABLED'):
        worker.run(job)
    assert writer.read_job(job)['status'] == 'prepared'


def test_writer_timeout_cleans_up_and_prevents_retry(bundle, monkeypatch):
    job = flow.create(bundle)['job_id']
    monkeypatch.setattr(worker, 'preflight', lambda _: None)
    cleanup = []
    monkeypatch.setattr(worker.subprocess, 'run', lambda args, **kw: cleanup.append(args) or SimpleNamespace(returncode=0))
    class Hung:
        stopped = False
        def __init__(self, *a, **kw):
            self.stdin, self.stdout = io.BytesIO(), io.BytesIO()
        def poll(self): return -9 if self.stopped else None
        def kill(self): self.stopped = True
        def wait(self, **kw): return -9
    monkeypatch.setattr(worker.subprocess, 'Popen', Hung)
    clock = chain([0, 0], repeat(100))
    monkeypatch.setattr(worker.time, 'monotonic', lambda: next(clock))
    result = worker.run(job, seconds=1)
    assert result['status'] == 'timed_out'
    assert result['container_cleanup_verified']
    assert cleanup[0][:3] == ['docker', 'rm', '-f']


def test_writer_recovery_cleans_up_without_starting_or_replaying(bundle, monkeypatch):
    job = flow.create(bundle)['job_id']
    manifest = writer.read_job(job)
    container = 'researchingos-writer-' + 'a' * 16
    manifest.update(status='running', container=container)
    worker.write_json(writer.job_path(job) / 'manifest.json', manifest)
    removed = []
    monkeypatch.setattr(worker, 'remove_container', lambda name, **kwargs: removed.append((name, kwargs)) or True)
    monkeypatch.setattr(worker.subprocess, 'Popen', lambda *a, **kw: pytest.fail('ambiguous job replayed'))
    assert worker.run(job)['status'] == 'interrupted'
    assert removed == [(container, {'job_id': job})]
    with pytest.raises(ValueError, match='prepared'):
        worker.run(job)


def test_workflow_context_labels_unverified_results(bundle, monkeypatch):
    monkeypatch.setattr(flow.OpenResearchService, 'discover', lambda self, q: [{'id':'arxiv:test', 'title':'Unverified'}])
    record = flow.create(bundle)
    flow.resume(record['id'])
    manifest = writer.read_job(record['job_id'])
    material = (writer.job_path(record['job_id']) / 'raw_materials/experimental_log.md').read_text()
    assert 'not full-text evidence' in material
    assert 'arxiv:test' in material
    assert 'context/original_experimental_log.md' in manifest['artifacts']
