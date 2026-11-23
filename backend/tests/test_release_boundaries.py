import asyncio
import json
import os
from pathlib import Path
import sys
import time

import pytest
import httpx

from services.durable_jobs import DurableWorker, JobStore, QueueFull, run_isolated_job
from services.paid_execution import ExecutionBudget, ProviderFailure, execution_scope, provider_request
from services.spend_ledger import SpendLedger, SpendLimit


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    path = tmp_path / 'payments.sqlite3'
    ledger = SpendLedger(path, 1)
    monkeypatch.setenv('RESEARCHINGOS_SPEND_LEDGER', str(path))
    monkeypatch.setenv('RESEARCHINGOS_SPEND_CAP_USD', '1')
    return ledger


def test_missing_configured_ledger_cannot_create_allowance(tmp_path, monkeypatch):
    path = tmp_path / 'missing.db'
    monkeypatch.setenv('RESEARCHINGOS_SPEND_LEDGER', str(path))
    monkeypatch.setenv('RESEARCHINGOS_SPEND_CAP_USD', '5')
    with pytest.raises(SpendLimit):
        SpendLedger.configured()
    assert not path.exists()


def test_pacing_persists_and_does_not_charge_a_request_that_cannot_start(ledger):
    ledger.reserve(.20, provider='test', interval=1)
    with pytest.raises(TimeoutError, match='rate slot'):
        SpendLedger.configured().reserve(.20, provider='test', interval=1, deadline=time.monotonic() + .1)
    assert ledger.status()['reserved_usd'] == .20


@pytest.mark.parametrize('failure', [ProviderFailure(429), TimeoutError('deadline')])
def test_ambiguous_call_keeps_reservation_and_cannot_replay_in_same_execution(ledger, failure):
    calls = []

    def fail(seconds):
        calls.append(seconds)
        assert ledger.status()['reserved_usd'] == .25
        raise failure

    budget = ExecutionBudget(5)
    for _ in range(2):
        with pytest.raises(type(failure)):
            budget.call('mock', .25, fail)
    assert len(calls) == 1
    assert ExecutionBudget(5).call('mock', .25, lambda _: 'next job') == 'next job'
    assert ledger.status()['reserved_usd'] == .50


def test_council_dspy_and_writer_share_budget(monkeypatch, ledger):
    import dspy
    from services.llm_router import LLMRouter
    from services.writer_broker import writer_request

    monkeypatch.setenv('GEMINI_API_KEY', 'fixture')
    monkeypatch.setenv('RESEARCHINGOS_GEMINI_APPROVED_MODELS', 'gemini-2.5-flash')
    monkeypatch.setenv('RESEARCHINGOS_GEMINI_TOKEN_PRICE_CEILING', '10')
    reply = {'candidates': [{'content': {'parts': [{'text': 'fixture'}]}}]}
    calls = []

    def generate(model, key, body, seconds):
        calls.append((model, body))
        return reply

    monkeypatch.setattr('services.llm_router.gemini_request', generate)
    monkeypatch.setattr('services.writer_broker.gemini_request', generate)
    # Use independent reservation slots in this test; persistent pacing is tested above.
    monkeypatch.setattr('services.paid_execution.reserve_provider',
                        lambda ledger, provider, usd, deadline: ledger.reserve(usd, deadline=deadline))
    router = LLMRouter()
    model = 'gemini-2.5-flash'
    with execution_scope(ExecutionBudget(5)):
        assert router.generate_content('prompt', provider='GEMINI') == 'fixture'
        with dspy.context(disable_history=True):
            assert router.get_dspy_lm('GEMINI')(prompt='DSPy prompt') == ['fixture']
    frame = {'path': f'/v1beta/models/{model}:generateContent',
             'body': {'contents': [{'parts': [{'text': 'writer prompt'}]}]}}
    assert writer_request(frame, {model}, ExecutionBudget(5)) == reply
    assert len(calls) == 3 and ledger.status()['reserved_usd'] > .10
    frame['body']['tools'] = [{'googleSearch': {}}]
    with pytest.raises(ValueError, match='tools'):
        writer_request(frame, {model}, ExecutionBudget(5))
    assert len(calls) == 3


@pytest.mark.parametrize('status', [429, None])
def test_real_transport_enforces_single_attempt_and_wall_deadline(monkeypatch, ledger, status):
    attempts = []

    async def respond(request):
        attempts.append(request.method)
        if status is None:
            await asyncio.sleep(5)
        return httpx.Response(status or 200, json={})

    client = httpx.AsyncClient
    monkeypatch.setattr(httpx, 'AsyncClient', lambda **kwargs: client(transport=httpx.MockTransport(respond), **kwargs))
    budget = ExecutionBudget(.25)
    started = time.monotonic()
    expected = ProviderFailure if status else TimeoutError
    for _ in range(2):
        with pytest.raises(expected):
            budget.call('fixture', .25, lambda seconds: provider_request('https://model.invalid', {}, {}, seconds))
    assert attempts == ['POST'] and time.monotonic() - started < 2
    assert ledger.status()['reserved_usd'] == .25


def test_deadline_crash_and_quota_leave_later_queue_work_runnable(tmp_path, ledger):
    store = JobStore(tmp_path / 'jobs.db')
    interrupted = store.submit('research', {'mode': 'interrupted'})
    assert store.claim()['id'] == interrupted['id']
    ledger.reserve(.20)
    modes = ['timeout', 'quota', 'next']
    jobs = {store.submit('research', {'mode': mode})['id']: mode for mode in modes}
    source = '''
import os, sys, time
from services.spend_ledger import SpendLedger
SpendLedger.configured().reserve(.20)
if sys.argv[1] == 'timeout':
    time.sleep(30)
if sys.argv[1] == 'quota':
    sys.exit(74)
'''
    calls = []

    def handle(job_id):
        mode = jobs[job_id]
        calls.append(mode)
        env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1]))
        run_isolated_job([sys.executable, '-c', source, mode], 1, env=env)

    worker = DurableWorker(store, None, isolated_handler=handle)
    worker.start()
    try:
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline and store.get(list(jobs)[-1])['status'] != 'completed':
            time.sleep(.02)
    finally:
        worker.stop()
    assert store.get(interrupted['id'])['status'] == 'interrupted'
    timeout, quota, next_job = [store.get(job_id) for job_id in jobs]
    assert 'deadline' in timeout['error']
    assert 'quota' in quota['error']
    assert next_job['status'] == 'completed'
    assert calls == modes
    assert ledger.status()['reserved_usd'] == .80


def test_meta_review_retry_keeps_original_snapshot_and_creates_revision(api_client, monkeypatch, tmp_path):
    import main

    store = JobStore(tmp_path / 'release-jobs.db')
    monkeypatch.setattr(main, 'job_store', store)
    main.vault_manager.save_markdown('drafts', 'paper.md', 'submitted original')
    endpoint = '/api/research/meta-review'
    payload = {'filename': 'paper.md'}
    assert api_client.post(endpoint, json=payload).status_code == 422
    headers = {'Idempotency-Key': 'same-submission'}
    original = api_client.post(endpoint, json=payload, headers=headers)
    assert original.status_code == 202
    main.vault_manager.save_markdown('drafts', 'paper.md', 'human edit')
    assert api_client.post(endpoint, json=payload, headers=headers).json() == original.json()
    assert api_client.post(endpoint, json={**payload, 'target_venue': 'ACM'}, headers=headers).status_code == 409

    def review(**kwargs):
        assert kwargs['draft_content'] == 'submitted original'
        return {'success': True, 'revised_draft': 'reviewed revision'}

    monkeypatch.setattr(main.meta_review_council, 'run_alignment_cycle', review)
    row = store.get(original.json()['project_id'])
    events = []
    main.execute_research_job(row['kind'], json.loads(row['payload']), events.append)
    filename = events[-1]['data']['draftFile']
    assert main.vault_manager.read_markdown('drafts', filename, exact=True)['content'] == 'reviewed revision'
    assert main.vault_manager.read_markdown('drafts', 'paper.md', exact=True)['content'] == 'human edit'


def test_draft_save_queue_failure_reports_committed_save(api_client, monkeypatch):
    import main

    def full(**kwargs):
        assert kwargs['target_filename'] == 'paper.md'
        assert kwargs['draft_snapshot']['content'] == 'latest edit'
        raise QueueFull('Publisher queue full')

    monkeypatch.setattr(main.publisher_readiness_jobs, 'start', full)
    response = api_client.post('/api/vault/write', json={
        'category': 'drafts', 'filename': 'paper.md', 'content': 'latest edit',
        'frontmatter': {}, 'trigger_readiness': True,
    })
    assert response.status_code == 200
    assert 'queue is full' in response.json()['readiness_error']
    assert main.vault_manager.read_markdown('drafts', 'paper.md', exact=True)['content'] == 'latest edit'


def test_real_drafting_graph_runs_with_tracing_disabled():
    from agents.drafting_graph import run_drafting_cycle

    result = run_drafting_cycle('Synthetic validation', 'Local synthesis fixture', '',
                                lambda *args: None, max_iterations=1, is_dry_run=True)
    assert result['draft']
    assert result['peer_review']['dry_run']


def test_claimed_engine_run_cannot_replay(tmp_path):
    from domain.research_experiments import ExperimentSpec
    from services.research_engines import execute

    path = tmp_path / 'engine'
    path.mkdir()
    original = b'{"status":"running"}'
    (path / 'summary.json').write_bytes(original)
    with pytest.raises(FileExistsError):
        execute(ExperimentSpec(engine='harness2'), path)
    assert (path / 'summary.json').read_bytes() == original
