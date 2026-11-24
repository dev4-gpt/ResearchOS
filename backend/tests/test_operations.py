import json
import shutil
import time

from services.durable_jobs import JobStore
from services.operations import snapshot


def test_operations_detects_failed_workers_backlog_budget_and_missing_backup(tmp_path, monkeypatch):
    store = JobStore(tmp_path / 'jobs.db', capacity=1)
    job = store.submit('research', {'topic': 'private text'})
    with store.connect() as db:
        db.execute('UPDATE jobs SET created=? WHERE id=?', (time.time() - 901, job['id']))
    monkeypatch.delenv('RESEARCHINGOS_SPEND_LEDGER', raising=False)
    result = snapshot({'research': store}, {'vault': tmp_path}, {'research': False})
    assert set(result['alerts']) == {'research_queue_full', 'research_queue_age',
                                    'research_worker_unavailable', 'paid_execution_unconfigured', 'backup_unverified'}
    assert str(tmp_path) not in json.dumps(result)
    assert 'private text' not in json.dumps(result)


def test_operations_healthy_and_stale_backup(tmp_path, monkeypatch):
    from services.spend_ledger import SpendLedger
    ledger = SpendLedger(tmp_path / 'spend.db', 1)
    monkeypatch.setenv('RESEARCHINGOS_SPEND_LEDGER', str(ledger.path))
    monkeypatch.setenv('RESEARCHINGOS_SPEND_CAP_USD', '1')
    receipt = tmp_path / 'backup.json'
    receipt.write_text(json.dumps({'verified': True, 'completed_at_unix': time.time()}))
    store = JobStore(tmp_path / 'jobs.db')
    result = snapshot({'research': store}, {'vault': tmp_path}, {'research': True}, backup_receipt=receipt)
    assert result['healthy']
    receipt.write_text(json.dumps({'verified': True, 'completed_at_unix': time.time() - 86401}))
    ledger.reserve(1)
    monkeypatch.setattr(shutil, 'disk_usage', lambda _: type('Disk', (), {'free': 1})())
    result = snapshot({'research': store}, {'vault': tmp_path}, {'research': True}, backup_receipt=receipt)
    assert set(result['alerts']) == {'backup_stale', 'low_disk', 'budget_exhausted'}


def test_operations_endpoint_is_protected_and_reports_aggregate_state(api_client):
    response = api_client.get('/api/operations')
    assert response.status_code == 200
    assert set(response.json()['queues']) == {'research', 'publisher'}
