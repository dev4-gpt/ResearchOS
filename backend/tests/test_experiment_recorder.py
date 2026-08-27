"""The experiment recorder must not let one experiment delete another's evidence.

`scripts/experiments/harness.py` is loaded by path rather than imported by name:
`backend/harness/` is a package, and which one `import harness` resolves to
depends on how the interpreter was started. Under pytest from the repository
root the package wins, so a plain import here tests the wrong module.
"""
import importlib.util
import json
import os
import sys

import pytest

_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "scripts", "experiments", "harness.py"))


@pytest.fixture
def harness(tmp_path):
    """The experiment harness, writing runs into a throwaway directory."""
    spec = importlib.util.spec_from_file_location("experiment_harness", _PATH)
    module = importlib.util.module_from_spec(spec)
    # Registered before exec: @dataclass resolves a class's module through
    # sys.modules, and fails on a module that is not there yet.
    sys.modules["experiment_harness"] = module
    try:
        spec.loader.exec_module(module)
        module.RUNS_ROOT = str(tmp_path)
        yield module
    finally:
        sys.modules.pop("experiment_harness", None)


def _record(harness, metrics, owns_prefix=""):
    rec = harness.ExperimentRecorder("run", "paper", "desc", owns_prefix=owns_prefix)
    artifact, digest = rec.save_artifact("a.json", {"payload": list(metrics)})
    for name, value in metrics.items():
        rec.record(name, value, "", artifact, digest, "method")
    rec.finalize()


def _metrics(tmp_path):
    path = tmp_path / "run" / "measurements.jsonl"
    return sorted(json.loads(line)["metric"]
                  for line in path.read_text().splitlines() if line.strip())


def test_second_experiment_does_not_delete_the_first(harness, tmp_path):
    """A paper can have two experiments; the file is keyed by paper, not experiment.

    Without a declared namespace the second script to run truncates the first
    one's rows -- the ERR-051 data loss by another route, since the empty-result
    guard only catches a run that recorded nothing at all.
    """
    _record(harness, {"mrr_bm25": 0.91})
    _record(harness, {"swebench_retrieval_mrr_bm25": 0.47},
            owns_prefix="swebench_retrieval_")

    assert _metrics(tmp_path) == ["mrr_bm25", "swebench_retrieval_mrr_bm25"]


def test_a_namespace_owner_removes_its_own_stale_rows(harness, tmp_path):
    """Owning a namespace means replacing it, not appending to it forever."""
    _record(harness, {"swebench_retrieval_old": 1.0, "keep_me": 2.0},
            owns_prefix="swebench_retrieval_")
    _record(harness, {"swebench_retrieval_new": 3.0},
            owns_prefix="swebench_retrieval_")

    assert _metrics(tmp_path) == ["keep_me", "swebench_retrieval_new"]


def test_no_namespace_still_replaces_the_whole_file(harness, tmp_path):
    """The default is unchanged: one experiment per paper replaces everything."""
    _record(harness, {"old_metric": 1.0})
    _record(harness, {"new_metric": 2.0})

    assert _metrics(tmp_path) == ["new_metric"]


def test_a_prefix_another_experiment_uses_would_eat_its_rows(harness, tmp_path):
    """The mechanism is only as good as the prefix, which is why drops are reported.

    p1 records four census metrics named swebench_*. p1b's first version claimed
    "swebench_" and deleted all four. The namespace must be one nothing else
    writes, and a run that removes rows says which.
    """
    _record(harness, {"swebench_instances": 300.0})
    _record(harness, {"swebench_retrieval_mrr": 0.47}, owns_prefix="swebench_")

    # The census row is gone -- correctly, given that prefix -- which is exactly
    # the outcome the printed drop list exists to make visible.
    assert "swebench_instances" not in _metrics(tmp_path)

    # With an exclusive prefix it survives.
    _record(harness, {"swebench_instances": 300.0})
    _record(harness, {"swebench_retrieval_mrr": 0.47},
            owns_prefix="swebench_retrieval_")
    assert "swebench_instances" in _metrics(tmp_path)
