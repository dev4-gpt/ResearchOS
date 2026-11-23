"""Adversarial checks for repair isolation, budgets and evidence binding."""
import json
from pathlib import Path
import sys

import pytest

from services.reproducibility import (
    Budget, GemmaClient, MODELS, RepairTask, RepositoryTools, benchmark, digest,
    run_arm, verify_measurement,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from run_reproducibility import FixtureClient, fixture_task

IMAGE = "python@sha256:" + "a" * 64


class InspectRunner:
    """Unit-test double only; integration demo uses DockerTests."""
    def run(self, repo, task, timeout):
        broken = "len(values) + 1" in (repo / "stats.py").read_text()
        return {"exit_code": int(broken), "timed_out": False, "output": "fixture assertion", "seconds": 0}


def test_all_arms_isolated_and_fixture_evidence_refused(tmp_path):
    task = fixture_task(tmp_path / "source", IMAGE)
    run = benchmark([task], FixtureClient(), InspectRunner(), Budget(), tmp_path / "runs", synthetic=True)
    summary = json.loads((run / "summary.json").read_text())
    assert all(row["resolved"] == 1 for row in summary["arms"].values())
    assert "len(values) + 1" in (tmp_path / "source" / "stats.py").read_text()
    for arm in summary["arms"]:
        assert json.loads((run / task.id / arm / "result.json").read_text())["baseline"]["exit_code"] == 1
    assert verify_measurement(run, "plain", "resolved", 1)["status"] == "blocked"
    assert "FIXTURE DEMO" in (run / "report.md").read_text()


def test_test_files_and_history_cannot_be_edited_or_read(tmp_path):
    task = fixture_task(tmp_path / "source", IMAGE)
    tools = RepositoryTools(Path(task.repository), task, "plain", InspectRunner(), 4000)
    for action in [
        {"tool": "read", "path": "../outside"},
        {"tool": "read", "path": ".git/config"},
        {"tool": "edit", "path": "test_stats.py", "old": "3", "new": "0"},
        {"tool": "search", "query": "mean"},
        {"tool": "neighbors", "path": "stats.py"},
    ]:
        with pytest.raises(ValueError):
            tools.invoke(action, 10)


def test_graph_candidates_and_lexical_search(tmp_path):
    task = fixture_task(tmp_path / "source", IMAGE)
    repo = Path(task.repository)
    (repo / "consumer.py").write_text("from stats import mean\nresult = mean([1, 2])\n")
    tools = RepositoryTools(repo, task, "graph", InspectRunner(), 4000)
    assert tools.search("mean values")[0]["path"] == "stats.py"
    assert any(row["path"] == "stats.py" for row in tools.neighbors("consumer.py"))


def test_zero_effect_patch_does_not_resolve_passing_baseline(tmp_path):
    task = fixture_task(tmp_path / "source", IMAGE)
    class AlwaysPass(InspectRunner):
        def run(self, *args):
            return {"exit_code": 0, "timed_out": False, "output": "", "seconds": 0}
    record = run_arm(task, "plain", Budget(), FixtureClient(), AlwaysPass(), tmp_path / "trial", True)
    assert record["status"] == "error"
    assert not record["resolved"]
    assert record["steps"] == 0


def test_usage_overrun_fails_closed(tmp_path):
    task = fixture_task(tmp_path / "source", IMAGE)
    class Overrun(FixtureClient):
        def complete(self, *args):
            return {"text": '{"tool":"finish"}', "usage": {"prompt_tokens": 100000, "completion_tokens": 1}}
    result = run_arm(task, "plain", Budget(), Overrun(), InspectRunner(), tmp_path / "trial", True)
    assert result["status"] == "error" and not result["resolved"]


def test_exact_metric_and_tamper_detection(tmp_path):
    # Test doubles in temporary storage exercise consistency, not real inference.
    class TestClient(FixtureClient):
        model = MODELS[0]
    task = fixture_task(tmp_path / "source", IMAGE)
    run = benchmark([task], TestClient(), InspectRunner(), Budget(), tmp_path / "runs")
    assert verify_measurement(run, "plain", "resolved", 7)["status"] == "blocked"
    assert verify_measurement(run, "plain", "resolved", 1)["status"] == "verified"
    (run / task.id / "plain/result.json").write_text('{"tampered":true}')
    assert verify_measurement(run, "plain", "resolved", 1)["status"] == "blocked"


def test_model_and_missing_usage_rejected(monkeypatch, tmp_path):
    with pytest.raises(ValueError):
        GemmaClient("http://localhost:9000/v1", "other-model")
    from services.spend_ledger import SpendLedger
    path = tmp_path / 'spend.db'
    ledger = SpendLedger(path, 1)
    monkeypatch.setenv('RESEARCHINGOS_SPEND_LEDGER', str(path))
    monkeypatch.setenv('RESEARCHINGOS_SPEND_CAP_USD', '1')
    monkeypatch.setenv('RESEARCHINGOS_REPRO_GEMMA_TOKEN_PRICE_CEILING', '100')
    monkeypatch.setattr('services.reproducibility.provider_request', lambda *args: {'model': MODELS[0], 'choices': []})
    with pytest.raises(ValueError, match="token usage"):
        GemmaClient("http://localhost:9000/v1", MODELS[0]).complete([], 100, 1)
    assert ledger.status()['reserved_usd'] > 0


def test_manifest_rejects_traversal_and_unpinned_images(tmp_path):
    task = fixture_task(tmp_path / "source", IMAGE).model_dump()
    task["editable_paths"] = ["../test.py"]
    with pytest.raises(ValueError): RepairTask.model_validate(task)
    task["editable_paths"] = ["stats.py"]
    task["image"] = "python:latest"
    with pytest.raises(ValueError): RepairTask.model_validate(task)


def test_read_only_api_and_fixture_claim_block(tmp_path, monkeypatch):
    import reproducibility_api as api
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    task = fixture_task(tmp_path / "source", IMAGE)
    run = benchmark([task], FixtureClient(), InspectRunner(), Budget(), tmp_path / "runs", synthetic=True)
    monkeypatch.setattr(api, "RUNS", tmp_path / "runs")
    app = FastAPI()
    app.include_router(api.router)
    client = TestClient(app)
    assert client.get('/api/reproducibility/status').status_code == 200
    assert client.get('/api/reproducibility/runs').json()["runs"][0]["synthetic"] is True
    assert "FIXTURE DEMO" in client.get(f'/api/reproducibility/runs/{run.name}').json()["report"]
    response = client.post(f'/api/reproducibility/runs/{run.name}/verify',
        json={"arm": "plain", "metric": "resolved", "value": 1})
    assert response.json()["status"] == "blocked"
    assert client.get(f'/api/reproducibility/runs/{run.name}/artifact',
        params={"path": f"{task.id}/plain/result.json"}).status_code == 200
    assert client.get(f'/api/reproducibility/runs/{run.name}/artifact',
        params={"path": "../../secrets.json"}).status_code == 404
    assert client.post('/api/reproducibility/run', json={"command": "anything"}).status_code == 404
