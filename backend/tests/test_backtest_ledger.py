import json

from services.backtest_ledger import BacktestLedger


def test_backtest_ledger_preserves_baseline_and_candidate_decisions(vault):
    ledger = BacktestLedger(vault)
    run = ledger.start(
        filename="paper.md",
        venue="IEEEtran",
        baseline_content="# baseline",
        max_iters=2,
    )
    ledger.record(
        run["run_id"],
        iteration=1,
        stage="evaluate",
        status="discard",
        content="# candidate",
        details={"reason": "regression"},
    )
    manifest = ledger.finish(
        run["run_id"],
        status="BLOCKED",
        final_content="# baseline",
        iterations=1,
        reason="regression",
    )

    assert manifest["baseline_sha256"] == manifest["final_sha256"]
    events = (ledger.root / run["run_id"] / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert json.loads(events[0])["status"] == "discard"
    assert json.loads(events[0])["content_sha256"] != manifest["final_sha256"]
    assert json.loads(events[0])["details"]["reason"] == "regression"
