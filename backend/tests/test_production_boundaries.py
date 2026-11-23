import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import threading
import time
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.access_control import OperatorAccess
from services.durable_jobs import JobStore, DurableWorker, JobConflict, QueueFull


def test_operator_access_protects_api_and_artifacts(monkeypatch):
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    monkeypatch.setenv('RESEARCHINGOS_PASSWORD', 'a' * 40)
    monkeypatch.setenv('RESEARCHINGOS_ORIGINS', 'https://research.example')
    app = FastAPI()
    app.add_middleware(OperatorAccess)
    for route in ['/api/session', '/api/vault/write', '/vault/private.md']:
        app.add_api_route(route, lambda: {'ok': True}, methods=['GET', 'POST'])
    with TestClient(app, base_url='https://research.example') as client:
        assert client.get('/vault/private.md').status_code == 401
        assert client.post('/api/vault/write').status_code == 401
        assert client.get('/api/session', auth=('operator', 'wrong')).status_code == 401
        signed_in = client.post('/api/session', auth=('operator', 'a' * 40))
        assert signed_in.status_code == 200
        assert 'HttpOnly' in signed_in.headers['set-cookie']
        assert 'Secure' in signed_in.headers['set-cookie']
        assert client.get('/vault/private.md').status_code == 200
        assert client.post('/api/vault/write').status_code == 401
        assert client.post('/api/vault/write', headers={'Origin': 'https://evil.example'}).status_code == 403
        assert client.post('/api/vault/write', headers={'Origin': 'https://research.example'}).status_code == 200
        monkeypatch.setenv('RESEARCHINGOS_PASSWORD', 'b' * 40)
        assert client.get('/api/session').status_code == 401
        monkeypatch.delenv('RESEARCHINGOS_PASSWORD')
        assert client.get('/api/session').status_code == 503


def test_local_mode_rejects_remote_peer_and_foreign_host(monkeypatch):
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'local')
    app = FastAPI(); app.add_middleware(OperatorAccess)
    app.get('/')(lambda: {})
    assert TestClient(app, base_url='http://localhost', client=('10.1.1.1', 5000)).get('/').status_code == 403
    assert TestClient(app, base_url='http://evil.example', client=('127.0.0.1', 5000)).get('/').status_code == 403
    assert TestClient(app, base_url='http://localhost', client=('127.0.0.1', 5000)).get('/').status_code == 200


def test_concurrent_idempotency_and_admission(tmp_path):
    store = JobStore(tmp_path / 'jobs.db', capacity=3)
    with ThreadPoolExecutor(max_workers=8) as pool:
        ids = list(pool.map(lambda _: store.submit('research', {'topic': 'one'}, 'same')['id'], range(20)))
    assert len(set(ids)) == 1
    with pytest.raises(JobConflict): store.submit('research', {'topic': 'two'}, 'same')
    second = store.submit('research', {'topic': 'two'})
    third = store.submit('research', {'topic': 'three'})
    assert len({ids[0], second['id'], third['id']}) == 3
    with pytest.raises(QueueFull): store.submit('research', {})
    store.cancel(third['id'])
    assert store.get(third['id'])['status'] == 'cancelled'


def test_reopen_preserves_events_and_never_replays_interrupted_work(tmp_path):
    path = tmp_path / 'jobs.db'
    store = JobStore(path)
    first = store.submit('research', {'topic': 'paid'})
    second = store.submit('research', {'topic': 'queued'})
    assert store.claim()['id'] == first['id']
    store.append(first['id'], {'stage': 'charged'})
    reopened = JobStore(path)
    reopened.recover()
    assert reopened.get(first['id'])['status'] == 'interrupted'
    assert reopened.claim()['id'] == second['id']
    events = reopened.events(first['id'])
    assert json.loads(events[0]['data'])['stage'] == 'charged'
    assert reopened.events(first['id'], events[0]['seq']) == []
    with pytest.raises(JobConflict): reopened.cancel(second['id'])


def test_one_worker_owns_execution_and_survives_subscriber_absence(tmp_path):
    store = JobStore(tmp_path / 'jobs.db')
    gate = threading.Event()
    calls = []
    def handle(kind, payload, emit):
        calls.append(payload)
        emit({'stage': 'start'})
        gate.wait(2)
        return {'ok': True}
    worker = DurableWorker(store, handle)
    worker.start()
    try:
        with pytest.raises(RuntimeError): DurableWorker(store, handle).start()
        job = store.submit('research', {'topic': 'one'})
        for _ in range(100):
            if store.get(job['id'])['status'] == 'running': break
            time.sleep(.01)
        # No subscriber is needed to finish and retain events.
        gate.set()
        for _ in range(100):
            if store.get(job['id'])['status'] == 'completed': break
            time.sleep(.01)
        assert store.get(job['id'])['status'] == 'completed'
        assert len(calls) == 1
        assert len(store.events(job['id'])) == 1
    finally:
        gate.set(); worker.stop()


def test_tex_requires_isolated_configuration(monkeypatch, tmp_path):
    from services.tex_runtime import run_tex
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    monkeypatch.delenv('RESEARCHINGOS_TEX_IMAGE', raising=False)
    with pytest.raises(RuntimeError, match='digest-pinned'):
        run_tex(['pdflatex', 'document.tex'], tmp_path)


def test_tex_container_has_no_network_or_host_fallback(monkeypatch, tmp_path):
    import subprocess
    from services.tex_runtime import run_tex
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    monkeypatch.setenv('RESEARCHINGOS_TEX_IMAGE', 'tex@sha256:' + 'a' * 64)
    calls = []
    def fake(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, b'', b'')
    monkeypatch.setattr(subprocess, 'run', fake)
    run_tex(['pdflatex', '-no-shell-escape', str(tmp_path / 'document.tex')], tmp_path)
    assert '--network=none' in calls[0]
    assert '--read-only' in calls[0]
    assert '--pull=never' in calls[0]
    assert '/work/document.tex' in calls[0]
    assert calls[1][:3] == ['docker', 'rm', '-f']


def test_stale_manuscript_update_rejected(vault):
    vault.save_markdown('drafts', 'one.md', 'old')
    expected = vault.read_markdown('drafts', 'one.md')
    vault.save_markdown('drafts', 'one.md', 'user edit')
    with pytest.raises(ValueError, match='changed'):
        vault.save_markdown('drafts', 'one.md', 'agent edit', expected=expected)
    assert vault.read_markdown('drafts', 'one.md')['content'] == 'user edit'


def test_startup_configuration_fails_before_workers(monkeypatch):
    from services.access_control import validate_configuration
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    monkeypatch.delenv('RESEARCHINGOS_PASSWORD', raising=False)
    with pytest.raises(RuntimeError, match='authentication'): validate_configuration()
    monkeypatch.setenv('RESEARCHINGOS_PASSWORD', 'a' * 40)
    monkeypatch.setenv('RESEARCHINGOS_ORIGINS', 'http://localhost:3000')
    with pytest.raises(RuntimeError, match='HTTPS'): validate_configuration()
    monkeypatch.setenv('RESEARCHINGOS_ORIGINS', 'https://research.example')
    validate_configuration()


def test_sse_replay_disconnect_and_terminal_state(api_client, tmp_path, monkeypatch):
    import main
    store = JobStore(tmp_path / 'stream.sqlite3')
    monkeypatch.setattr(main, 'job_store', store)
    job = store.submit('research', {'topic': 'replay'})
    store.claim()
    store.append(job['id'], {'message': 'first'})
    store.append(job['id'], {'message': 'second'})
    store.finish(job['id'])
    first = store.events(job['id'])[0]['seq']
    response = api_client.get('/api/research/stream/' + job['id'], headers={'Last-Event-ID': str(first)})
    assert response.status_code == 200
    assert 'first' not in response.text
    assert 'second' in response.text
    assert 'event: end' in response.text and 'completed' in response.text
    assert len(store.events(job['id'])) == 2
    assert api_client.get('/api/research/stream/' + job['id']).text.count('data:') == 3
    assert api_client.get('/api/research/stream/' + job['id'], headers={'Last-Event-ID': 'bad'}).status_code == 422
    class Disconnected:
        headers = {}
        async def is_disconnected(self): return True
    async def disconnect():
        stream = await main.durable_stream(job['id'], Disconnected(), 0)
        return [part async for part in stream.body_iterator]
    assert asyncio.run(disconnect()) == []
    assert len(store.events(job['id'])) == 2


def test_sqlite_backup_restores_jobs_and_events(tmp_path):
    import sqlite3
    store = JobStore(tmp_path / 'source.sqlite3')
    job = store.submit('research', {'topic': 'restore'}, 'restore-key')
    store.append(job['id'], {'message': 'persisted'})
    backup = tmp_path / 'backup.sqlite3'
    with store.connect() as source, sqlite3.connect(backup) as destination:
        source.backup(destination)
    restored = JobStore(backup)
    assert restored.get(job['id'])['status'] == 'queued'
    assert restored.submit('research', {'topic': 'restore'}, 'restore-key')['id'] == job['id']
    assert len(restored.events(job['id'])) == 1


def test_readiness_reports_dead_workers(api_client, monkeypatch):
    import main
    from types import SimpleNamespace
    stopped = SimpleNamespace(thread=None, stopping=threading.Event())
    monkeypatch.setattr(main, 'job_worker', stopped)
    monkeypatch.setattr(main.publisher_readiness_jobs, 'worker', stopped)
    response = api_client.get('/api/ready')
    assert response.status_code == 503
    assert response.json()['ready'] is False
