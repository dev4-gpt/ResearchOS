import asyncio
import shutil

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from services.access_control import COOKIE, OperatorAccess
from services.durable_jobs import JobStore, QueueFull
from services.request_limits import RequestBodyLimit


def secured(monkeypatch):
    monkeypatch.setenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    monkeypatch.setenv('RESEARCHINGOS_PASSWORD', 'x' * 40)
    monkeypatch.setenv('RESEARCHINGOS_ORIGINS', 'https://research.example')
    app = FastAPI()
    app.add_middleware(OperatorAccess)
    app.add_api_route('/api/session', lambda: {}, methods=['GET', 'POST', 'DELETE'])
    app.get('/vault/private')(lambda: {})
    return app


def test_failed_auth_throttles_across_routes_and_headers(monkeypatch):
    with TestClient(secured(monkeypatch), base_url='https://research.example') as client:
        for n in range(10):
            path = '/api/session' if n % 2 else '/vault/private'
            assert client.get(path, auth=('operator', 'wrong')).status_code == 401
        response = client.get('/vault/private', headers={'X-Forwarded-For': 'different-peer'})
        assert response.status_code == 429
        assert response.headers['Retry-After'] == '60'
        # Valid operator credentials remain usable during an attack.
        assert client.post('/api/session', auth=('operator', 'x' * 40)).status_code == 200
        assert client.get('/vault/private').status_code == 200


def test_logout_revokes_captured_cookie_and_preserves_other_session(monkeypatch):
    app = secured(monkeypatch)
    with TestClient(app, base_url='https://research.example') as client:
        client.post('/api/session', auth=('operator', 'x' * 40))
        first = client.cookies.get(COOKIE)
        client.post('/api/session', auth=('operator', 'x' * 40))
        second = client.cookies.get(COOKIE)
        assert first != second
        response = client.delete('/api/session', headers={'Origin': 'https://research.example'})
        assert response.status_code == 200
        assert client.get('/vault/private', headers={'Cookie': f'{COOKIE}={second}'}).status_code == 401
        assert client.get('/vault/private', headers={'Cookie': f'{COOKIE}={first}'}).status_code == 200
    # A process/middleware restart invalidates previously issued sessions.
    with TestClient(secured(monkeypatch), base_url='https://research.example') as restarted:
        assert restarted.get('/vault/private', headers={'Cookie': f'{COOKIE}={first}'}).status_code == 401


def test_unauthorized_logout_cannot_revoke_cookie(monkeypatch):
    with TestClient(secured(monkeypatch), base_url='https://research.example') as client:
        client.post('/api/session', auth=('operator', 'x' * 40))
        assert client.delete('/api/session').status_code == 401
        assert client.get('/api/session').status_code == 200


@pytest.mark.parametrize('path', ['/api/feynman/autoresearch', '/api/fx/dispatch',
                                 '/api/fx/mcp/call', '/api/voice/synthesize', '/api/ecc/sync', '/api/evomap/pilot'])
def test_authenticated_mode_does_not_launch_unqualified_legacy_executor(monkeypatch, path):
    with TestClient(secured(monkeypatch), base_url='https://research.example') as client:
        response = client.post(path, auth=('operator', 'x' * 40))
        assert response.status_code == 403
        assert 'experimental executor' in response.json()['detail']


@pytest.mark.parametrize('declared', [False, True])
def test_request_body_limit_blocks_before_application(declared):
    calls = []
    messages = iter([{'type': 'http.request', 'body': b'123', 'more_body': True},
                     {'type': 'http.request', 'body': b'456', 'more_body': False}])
    sent = []
    async def app(scope, receive, send):
        calls.append(True)
    async def receive():
        return next(messages)
    async def send(message):
        sent.append(message)
    scope = {'type': 'http', 'headers': [(b'content-length', b'6')] if declared else []}
    asyncio.run(RequestBodyLimit(app, max_bytes=5)(scope, receive, send))
    assert not calls
    assert sent[0]['status'] == 413


def test_low_disk_rejects_new_job_but_allows_idempotent_lookup(tmp_path, monkeypatch):
    store = JobStore(tmp_path / 'jobs.db')
    first = store.submit('research', {'topic': 'one'}, key='one')
    monkeypatch.setattr(shutil, 'disk_usage', lambda _: type('Disk', (), {'free': 1})())
    assert store.submit('research', {'topic': 'one'}, key='one')['id'] == first['id']
    with pytest.raises(QueueFull, match='storage is low'):
        store.submit('research', {'topic': 'two'})
    assert store.metrics()['states'] == {'queued': 1}


def test_payload_limit_and_metrics_do_not_expose_prompt(tmp_path):
    store = JobStore(tmp_path / 'jobs.db')
    with pytest.raises(QueueFull, match='admission limit'):
        store.submit('research', {'topic': 'x' * 1_000_000})
    store.submit('research', {'topic': 'private prompt'})
    assert 'private prompt' not in str(store.metrics())
    assert store.metrics()['oldest_queued_seconds'] >= 0
