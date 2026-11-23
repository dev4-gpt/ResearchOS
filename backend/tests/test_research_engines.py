import json
from pathlib import Path
import time

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from domain.research_experiments import EngineBudget, ExperimentSpec
from services import research_engines as engines
from services import research_ranking as ranking
from services.harness2 import apply_edits
from services.fact_checker import FactCheckerService
from research_engines_api import router


@pytest.fixture
def dataset():
    return ranking.load_dataset()


def test_ranking_metrics_and_permutations(dataset):
    task = dataset['tasks'][0]
    ideal = ranking.lexical(task)
    assert ranking.measure(ideal, task) == {'ndcg_at_10': 1.0, 'recall_at_20': 1.0}
    assert ranking.measure(ranking.rrf(task), task)['ndcg_at_10'] < 1
    for bad in [ideal[:-1], ideal + [ideal[0]], ['fabricated'], 'not a list']:
        with pytest.raises(ValueError): ranking.measure(bad, task)
    assert 'labels' not in ranking.public_task(task)
    assert 'split' not in ranking.public_task(task)


def test_dataset_validation(tmp_path, dataset):
    dataset['tasks'][0]['id'] = '../escape'
    p = tmp_path / 'bad.json'; p.write_text(json.dumps(dataset))
    with pytest.raises(ValueError, match='Unsafe'): ranking.load_dataset(p)


def test_spec_and_budget_fail_closed():
    for values in [{'parent_run': '../escape'}, {'mode': 'live'}, {'seed': -1}]:
        with pytest.raises(ValidationError): ExperimentSpec(engine='alphaevolve', **values)
    with pytest.raises(ValidationError): ExperimentSpec(engine='harness2', steps=2)
    with pytest.raises(ValidationError): EngineBudget(max_usd=float('nan'))
    meter = engines.Meter(ExperimentSpec(engine='alphaevolve', budget=EngineBudget(calls=1)))
    meter.reserve('hello')
    with pytest.raises(engines.BudgetExceeded): meter.reserve('again')
    meter.started -= 1000
    with pytest.raises(engines.BudgetExceeded): meter.check()
    meter = engines.Meter(ExperimentSpec(engine='alphaevolve', budget=EngineBudget(tokens=256)))
    with pytest.raises(engines.BudgetExceeded): meter.reserve('hello')
    meter = engines.Meter(ExperimentSpec(engine='alphaevolve', budget=EngineBudget(max_usd=0.00001)))
    with pytest.raises(engines.BudgetExceeded): meter.reserve('hello')


def test_harness_edit_surface(tmp_path):
    for key in ['../outside', 'guardrails.md', 'scripts/evil.py', 'plugins/evil.py', 'LongTermMEMORY.md']:
        with pytest.raises(ValueError): apply_edits(tmp_path, {key: 'changed'})
    apply_edits(tmp_path, {'systemprompt.md': 'Rank papers.'})
    assert (tmp_path / 'systemprompt.md').read_text() == 'Rank papers.'


def require_source(engine):
    try: engines.pinned_source(engine)
    except RuntimeError: pytest.skip('Pinned upstream not installed; run setup_research_engines.py')


@pytest.mark.parametrize('engine', ['alphaevolve', 'harness2'])
def test_real_upstream_fixture_and_evidence(engine, tmp_path):
    require_source(engine)
    result = engines.execute(ExperimentSpec(engine=engine), tmp_path / engine)
    assert result['status'] == 'completed', result
    assert result['usage']['calls'] == 0
    assert result['metrics']['candidate']['ndcg_at_10'] == 1
    check = engines.verify_run(tmp_path / engine)
    assert check['integrity_verified'] and check['metrics_recomputed']
    assert not check['publication_eligible']
    assert not FactCheckerService().verify_research_engine_run(tmp_path / engine)['publication_eligible']
    # Changing raw measurements invalidates hashes. Resealing cannot validate fake metrics.
    p = tmp_path / engine / 'measurements.json'
    rows = json.loads(p.read_text()); rows[0]['metrics']['ndcg_at_10'] = 0.99
    engines.write_json(p, rows)
    assert not engines.verify_run(tmp_path / engine)['integrity_verified']
    engines.seal_run(tmp_path / engine)
    assert not engines.verify_run(tmp_path / engine)['metrics_recomputed']


def test_live_disabled_records_blocker(tmp_path, monkeypatch):
    require_source('alphaevolve')
    monkeypatch.delenv('RESEARCH_ENGINES_ENABLED', raising=False)
    result = engines.execute(ExperimentSpec(engine='alphaevolve', mode='live', model='explicit-model'), tmp_path / 'blocked')
    assert result['status'] == 'blocked'
    assert result['usage']['calls'] == 0
    assert 'disabled' in result['error']


def test_pinned_source_tampering(tmp_path, monkeypatch):
    monkeypatch.setattr(engines, 'ROOT', tmp_path)
    assert not engines.status()['engines']['harness2']['sources_verified']


def test_api_read_only_and_path_security(tmp_path, monkeypatch):
    monkeypatch.setattr(engines, 'RUNS', tmp_path)
    app = FastAPI(); app.include_router(router)
    client = TestClient(app)
    assert client.get('/api/research-engines/status').status_code == 200
    assert client.get('/api/research-engines/runs').json() == {'runs': []}
    assert client.post('/api/research-engines/runs').status_code == 405
    assert client.get('/api/research-engines/runs/missing').status_code == 404
    path = tmp_path / 'valid'; path.mkdir()
    (path / 'summary.json').write_text('{"status":"blocked"}')
    engines.seal_run(path)
    assert client.get('/api/research-engines/runs/valid').status_code == 200
    assert client.get('/api/research-engines/runs/valid/artifact', params={'name': '../outside'}).status_code == 404
    (path / 'summary.json').write_text('{"status":"forged"}')
    assert client.get('/api/research-engines/runs/valid/artifact', params={'name': 'summary.json'}).status_code == 409
    with pytest.raises(ValueError): engines.safe_run(tmp_path, '../escape')
    (tmp_path / 'link').symlink_to(path)
    assert client.get('/api/research-engines/runs/link').status_code == 404


def test_docker_missing_image_no_fallback(monkeypatch):
    monkeypatch.delenv('RESEARCH_ENGINE_IMAGE', raising=False)
    with pytest.raises(RuntimeError, match='pinned by digest'): engines.docker_preflight()


def test_api_rejects_symlink_records(tmp_path, monkeypatch):
    monkeypatch.setattr(engines, 'RUNS', tmp_path / 'runs')
    root = engines.RUNS / 'run'; root.mkdir(parents=True)
    secret = tmp_path / 'outside.json'; secret.write_text('{"private":"do not expose"}')
    (root / 'summary.json').symlink_to(secret)
    (root / 'artifacts.json').write_text('{}')
    app = FastAPI(); app.include_router(router)
    response = TestClient(app).get('/api/research-engines/runs/run')
    assert response.status_code == 409
    assert 'do not expose' not in response.text


def test_registered_routes_and_core_connectivity(api_client):
    for url in ('/api/health', '/api/vault/files', '/api/vault/files?category=drafts', '/api/research-engines/status', '/api/research-engines/runs'):
        assert api_client.get(url).status_code == 200, url
