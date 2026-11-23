from concurrent.futures import ThreadPoolExecutor
import pytest
from services.spend_ledger import SpendLedger, SpendLimit


def test_concurrent_cap_and_restart(tmp_path):
    path = tmp_path / 'spend.db'
    ledger = SpendLedger(path, 5)
    def attempt(_):
        try:
            SpendLedger(path, 5).reserve(1)
            return True
        except SpendLimit:
            return False
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(20))) == 5
    assert SpendLedger(path, 5).status() == {'cap_usd': 5, 'reserved_usd': 5}
    with pytest.raises(SpendLimit): ledger.reserve(.000001)
    with pytest.raises(SpendLimit): SpendLedger(path, 6)


def test_invalid_and_submicro_reservations(tmp_path):
    ledger = SpendLedger(tmp_path / 'spend.db', 1)
    for value in [-1, float('nan'), float('inf')]:
        with pytest.raises(ValueError): ledger.reserve(value)
    ledger.reserve(.00000001)
    assert ledger.status()['reserved_usd'] == .000001


def test_live_meter_requires_shared_cap_and_reserves_before_call(tmp_path, monkeypatch):
    from domain.research_experiments import ExperimentSpec
    from services.research_engines import Meter
    spec = ExperimentSpec(engine='harness2', mode='live', model='test')
    monkeypatch.delenv('RESEARCHINGOS_SPEND_LEDGER', raising=False)
    monkeypatch.delenv('RESEARCHINGOS_SPEND_CAP_USD', raising=False)
    with pytest.raises(SpendLimit, match='shared spending ledger'): Meter(spec).reserve('hello')
    monkeypatch.setenv('RESEARCHINGOS_SPEND_LEDGER', str(tmp_path / 'shared.db'))
    monkeypatch.setenv('RESEARCHINGOS_SPEND_CAP_USD', '0.21')
    SpendLedger(tmp_path / 'shared.db', .21)
    first = Meter(spec)
    first.reserve('hello')
    assert first.calls == 1
    with pytest.raises(SpendLimit): Meter(spec).reserve('hello')


def test_restore_drill_preserves_source_and_validates_sqlite(tmp_path):
    import importlib.util
    from pathlib import Path
    from services.durable_jobs import JobStore
    spec = importlib.util.spec_from_file_location('restore_drill', Path(__file__).resolve().parents[2] / 'scripts/restore_drill.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    root = tmp_path / 'source'
    (root / 'vault').mkdir(parents=True)
    (root / 'vault/paper.md').write_text('original research')
    store = JobStore(root / 'runs/service/jobs.sqlite3')
    job = store.submit('research', {'topic': 'restore'})
    report = module.drill(root, tmp_path)
    assert report['passed']
    assert report['databases']['runs/service/jobs.sqlite3']['states'] == {'queued': 1}
    assert store.get(job['id'])['status'] == 'queued'
    assert (root / 'vault/paper.md').read_text() == 'original research'
    (root / 'vault/link').symlink_to(root / 'vault/paper.md')
    with pytest.raises(RuntimeError, match='Symlink'): module.drill(root, tmp_path)
