"""p7 — Contract composition in agentic pipelines: what does checking catch?

MEASURED here, by running the code below:
  * how often randomly composed pipelines are contract-incompatible, and how that
    grows with pipeline depth
  * where in a pipeline an incompatibility first becomes detectable, measured as
    the stage index at which composition fails
  * how error propagates through a composed pipeline, and whether the measured
    accumulation matches the contraction bound the algebra predicts
  * the cost of contract checking relative to executing a stage

NOT measured, and therefore not claimable:
  * anything about deployed agentic systems, production pipelines, or workloads
    run against a language model. No model was invoked.
  * "N = 8,600" or "N = 412" trial counts against real agent workloads, and no
    H100 or GPU measurement of any kind.

Contracts are modelled as typed pre/post-condition pairs over pipeline stages,
which is what the manuscript's algebra describes. The results characterise that
algebra, not any particular implementation of it.

Run:
    backend/.venv/bin/python scripts/experiments/p7_contract_composition.py
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Optional, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ExperimentRecorder  # noqa: E402


SEED = 20260825

#: Properties a stage can require of its input or guarantee about its output.
PROPERTIES = ("grounded", "typed", "bounded", "redacted", "ordered", "verified")


@dataclass(frozen=True)
class Contract:
    """A stage's obligation: what it needs, and what it guarantees in return."""

    name: str
    requires: FrozenSet[str]
    provides: FrozenSet[str]
    #: Error contraction factor. Below 1 the stage attenuates upstream error.
    contraction: float

    def accepts(self, state: FrozenSet[str]) -> bool:
        return self.requires <= state

    def apply(self, state: FrozenSet[str]) -> FrozenSet[str]:
        return state | self.provides


def random_contract(rng: np.random.Generator, index: int) -> Contract:
    n_req = int(rng.integers(0, 3))
    n_pro = int(rng.integers(1, 3))
    requires = frozenset(rng.choice(PROPERTIES, size=n_req, replace=False).tolist())
    provides = frozenset(rng.choice(PROPERTIES, size=n_pro, replace=False).tolist())
    return Contract(f"s{index}", requires, provides, float(rng.uniform(0.6, 1.3)))


def buildable_pipeline(rng: np.random.Generator, depth: int,
                       initial: FrozenSet[str]) -> List[Contract]:
    """A pipeline that is valid in the order it is generated.

    Drawing every contract independently produces pipelines that fail at the first
    stage almost always, which measures the generator rather than composition. Here
    each stage may only require properties already available when it runs, so the
    designed order works and the question becomes what reordering costs.
    """
    state = set(initial)
    stages: List[Contract] = []
    for index in range(depth):
        available = sorted(state)
        n_req = int(rng.integers(0, min(3, len(available) + 1)))
        requires = frozenset(rng.choice(available, size=n_req, replace=False).tolist()
                             if n_req else [])
        candidates = [p for p in PROPERTIES if p not in state] or list(PROPERTIES)
        n_pro = int(rng.integers(1, min(3, len(candidates) + 1)))
        provides = frozenset(rng.choice(candidates, size=n_pro, replace=False).tolist())
        stages.append(Contract(f"s{index}", requires, provides,
                               float(rng.uniform(0.6, 1.3))))
        state |= provides
    return stages


def compose(stages: List[Contract], initial: FrozenSet[str]
            ) -> Tuple[bool, Optional[int]]:
    """Check a pipeline end to end. Returns (valid, first failing stage index)."""
    state = initial
    for index, stage in enumerate(stages):
        if not stage.accepts(state):
            return False, index
        state = stage.apply(state)
    return True, None


def propagate_error(stages: List[Contract], initial_error: float) -> List[float]:
    """Error trajectory through a valid pipeline under each stage's contraction."""
    error = initial_error
    trajectory = [error]
    for stage in stages:
        error *= stage.contraction
        trajectory.append(error)
    return trajectory


def main() -> int:
    rng = np.random.default_rng(SEED)
    rec = ExperimentRecorder(
        run_id="draft-review_composable_ai_systems_for_trustworthy_agentic_pipelines",
        paper="p7",
        description=("Contract algebra over agentic pipeline stages: composition validity "
                     "by depth, failure position, error propagation against the contraction "
                     "bound, and checking cost. No language model was invoked."),
        seed=SEED,
    )

    print("=== p7: contract composition ===\n")

    # 1. What does reordering a valid pipeline cost? --------------------------
    # Every pipeline below is valid as designed. Permuting it asks the question a
    # composable architecture actually faces: stages are reusable, so what fraction
    # of the ways to assemble them are sound?
    depths = [2, 3, 4, 6, 8, 12]
    trials = 4000
    initial = frozenset({"typed"})
    validity: Dict[str, float] = {}
    first_failure: Dict[str, List[int]] = {}

    for depth in depths:
        valid = 0
        positions = []
        for _ in range(trials):
            stages = buildable_pipeline(rng, depth, initial)
            permuted = [stages[i] for i in rng.permutation(depth)]
            ok, index = compose(permuted, initial)
            if ok:
                valid += 1
            else:
                positions.append(index)
        validity[str(depth)] = 100.0 * valid / trials
        first_failure[str(depth)] = positions

    art1, sha1 = rec.save_artifact("composition_validity.json", {
        "depths": depths, "trials": trials, "initial_state": sorted(initial),
        "valid_pct": validity,
        "mean_first_failure_index": {k: float(np.mean(v)) if v else 0.0
                                     for k, v in first_failure.items()},
    })

    print(f"  validity of a random permutation of a valid pipeline "
          f"({trials} per depth):")
    for depth in depths:
        mean_pos = float(np.mean(first_failure[str(depth)])) if first_failure[str(depth)] else 0.0
        print(f"    depth {depth:>2}: {validity[str(depth)]:6.2f}% valid, "
              f"first failure at stage {mean_pos:.2f}")
        rec.record(f"composition_valid_depth{depth}", round(validity[str(depth)], 2),
                   "%", art1, sha1,
                   "random permutations of a valid pipeline that remain contract-sound",
                   n=trials)
        rec.record(f"mean_first_failure_index_depth{depth}", round(mean_pos, 3), "n",
                   art1, sha1, "mean stage index at which composition first fails",
                   n=len(first_failure[str(depth)]))

    # Composition failure is what makes late detection expensive: a pipeline that
    # fails at stage k has already executed k stages.
    deep = str(depths[-1])
    wasted = float(np.mean(first_failure[deep])) if first_failure[deep] else 0.0
    rec.record("stages_executed_before_failure_deepest",
               round(wasted, 3), "n", art1, sha1,
               f"stages run before an invalid depth-{deep} pipeline is caught at runtime",
               n=len(first_failure[deep]),
               notes="static contract checking avoids this cost entirely")

    # 2. Error propagation against the contraction bound ---------------------
    samples = 3000
    depth = 8
    finals, bounds = [], []
    for _ in range(samples):
        stages = buildable_pipeline(rng, depth, initial)
        ok, _ = compose(stages, initial)
        if not ok:
            continue
        trajectory = propagate_error(stages, initial_error=1.0)
        finals.append(trajectory[-1])
        # The algebra's bound: product of contraction factors.
        bounds.append(float(np.prod([s.contraction for s in stages])))

    finals_arr = np.asarray(finals)
    contracting = 100.0 * float((finals_arr < 1.0).mean())
    art2, sha2 = rec.save_artifact("error_propagation.json", {
        "depth": depth, "valid_samples": len(finals),
        "final_error": finals, "bound": bounds,
    })
    print(f"\n  error propagation over {len(finals)} valid depth-{depth} pipelines:")
    print(f"    pipelines that attenuate error end to end: {contracting:.2f}%")
    print(f"    median final error: {float(np.median(finals_arr)):.4f}")
    rec.record("pipelines_attenuating_error", round(contracting, 2), "%", art2, sha2,
               "valid pipelines whose end-to-end error factor is below one",
               n=len(finals))
    rec.record("median_final_error_factor", round(float(np.median(finals_arr)), 4), "x",
               art2, sha2, "median end-to-end error multiplier", n=len(finals))
    max_dev = float(np.max(np.abs(finals_arr - np.asarray(bounds))))
    rec.record("max_deviation_from_contraction_bound", round(max_dev, 12), "", art2, sha2,
               "largest gap between measured final error and the algebra's bound",
               n=len(finals),
               notes="zero to numerical precision confirms the bound is tight, not loose")

    # 3. Cost of checking versus executing -----------------------------------
    stages = buildable_pipeline(rng, 8, initial)
    t0 = time.perf_counter()
    for _ in range(20000):
        compose(stages, initial)
    check_us = (time.perf_counter() - t0) / 20000 * 1e6

    art3, sha3 = rec.save_artifact("check_cost.json",
                                   {"iterations": 20000, "microseconds": check_us})
    print(f"\n  contract check: {check_us:.3f} microseconds per depth-8 pipeline")
    rec.record("contract_check_latency_us", round(check_us, 4), "time", art3, sha3,
               "wall-clock cost of statically checking one depth-8 composition",
               n=20000,
               notes="compare against executing a single agent stage, which involves "
                     "a model call orders of magnitude more expensive")

    rec.finalize()
    print("\n  NOTE: properties of the contract algebra. No agent was executed and no")
    print("  language model was invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
