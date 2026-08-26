"""Derive the statistics the Analysis sections need, from artifacts already recorded.

The template puts an Analysis section before the Method: establish empirically what
is happening, then propose something that follows from the finding. Our manuscripts
skipped straight to results, even though each run recorded distributional detail
that was never examined -- per-query win/loss, the singular value spectrum, the
cascade tail, the shape of the reachable state space.

This reads the existing artifacts and appends the derived quantities to the same
measurements file. It deliberately does not re-run the experiments: p1 and p3 draw
their corpus from this repository's working tree, so re-running would move the
numbers the manuscripts were written against (ERR-052).

    backend/.venv/bin/python scripts/experiments/analysis_pass.py
    backend/.venv/bin/python scripts/experiments/analysis_pass.py --apply
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any, Callable, Dict, List, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_sync import REPO_ROOT, load_artifact, load_measurements  # noqa: E402

RUNS = os.path.join(REPO_ROOT, "runs")


def artifact_digest(run_id: str, name: str) -> Tuple[str, str]:
    path = os.path.join(RUNS, run_id, "artifacts", name)
    blob = open(path, "rb").read()
    return f"artifacts/{name}", hashlib.sha256(blob).hexdigest()


def row(metric: str, value: float, unit: str, artifact: str, sha: str,
        method: str, n: int = None, notes: str = "") -> Dict[str, Any]:
    entry = {"metric": metric, "value": float(value), "unit": unit,
             "artifact": artifact, "sha256": sha, "method": method}
    if n is not None:
        entry["n"] = n
    if notes:
        entry["notes"] = notes
    return entry


# --------------------------------------------------------------------- p1

def analyse_p1(run_id: str) -> List[Dict[str, Any]]:
    art, sha = artifact_digest(run_id, "retrieval_results.json")
    data = load_artifact(run_id, "retrieval_results.json")
    per_query = data["per_query"]

    wins = sum(1 for q in per_query if q["ppr"][2] > q["bm25"][2] + 1e-9)
    losses = sum(1 for q in per_query if q["ppr"][2] < q["bm25"][2] - 1e-9)
    ties = len(per_query) - wins - losses
    n = len(per_query)

    # Where BM25 already ranks the answer first, diffusion can only do harm.
    top1 = [q for q in per_query if q["bm25"][0] == 1.0]
    top1_damaged = sum(1 for q in top1 if q["ppr"][0] == 0.0)
    # Where BM25 misses the top slot, can diffusion recover it?
    missed = [q for q in per_query if q["bm25"][0] == 0.0]
    recovered = sum(1 for q in missed if q["ppr"][0] == 1.0)

    return [
        row("queries_improved_by_diffusion", wins, "n", art, sha,
            "per-query MRR strictly higher under PPR than BM25", n=n),
        row("queries_degraded_by_diffusion", losses, "n", art, sha,
            "per-query MRR strictly lower under PPR than BM25", n=n),
        row("queries_unchanged_by_diffusion", ties, "n", art, sha,
            "per-query MRR identical under both systems", n=n),
        row("bm25_top1_queries", len(top1), "n", art, sha,
            "queries where BM25 already ranks the gold module first", n=n),
        row("bm25_top1_damaged_by_diffusion", top1_damaged, "n", art, sha,
            "of those, how many diffusion demotes out of first place", n=len(top1)),
        row("bm25_missed_recovered_by_diffusion", recovered, "n", art, sha,
            "queries BM25 ranked below first that diffusion promotes to first",
            n=len(missed)),
    ]


# --------------------------------------------------------------------- p2

def analyse_p2(run_id: str) -> List[Dict[str, Any]]:
    art, sha = artifact_digest(run_id, "lora_subspace.json")
    data = load_artifact(run_id, "lora_subspace.json")
    singular = np.asarray(data["singular_values"], dtype=float)
    energy = np.cumsum(singular ** 2) / float((singular ** 2).sum())

    def rank_for(target: float) -> int:
        return int(np.searchsorted(energy, target) + 1)

    # How abruptly capacity saturates: the ratio of ranks bracketing the knee.
    r90, r95, r99 = rank_for(0.90), rank_for(0.95), rank_for(0.99)
    spectral_gap = float(singular[data["true_rank"] - 1] /
                         singular[data["true_rank"]]) if len(singular) > data["true_rank"] else 0.0

    return [
        row("rank_for_90pct_energy", r90, "n", art, sha,
            "smallest rank whose truncation retains 90% of update energy",
            n=len(singular)),
        row("rank_for_95pct_energy", r95, "n", art, sha,
            "smallest rank retaining 95% of update energy", n=len(singular)),
        row("rank_for_99pct_energy", r99, "n", art, sha,
            "smallest rank retaining 99% of update energy", n=len(singular)),
        row("spectral_gap_at_intrinsic_rank", round(spectral_gap, 4), "x", art, sha,
            "ratio of the singular value at the planted rank to the next one",
            notes="a large ratio is what makes the capacity curve a cliff"),
    ]


# --------------------------------------------------------------------- p3

def analyse_p3(run_id: str) -> List[Dict[str, Any]]:
    art, sha = artifact_digest(run_id, "mutation_results.json")
    data = load_artifact(run_id, "mutation_results.json")
    per_op = data["per_operator"]

    rates = [e["rejection_rate_pct"] for e in per_op.values()]
    validity = [e["syntactic_validity_pct"] for e in per_op.values()]
    guards = sum(e.get("guards_checked", 0) for e in per_op.values())
    produced = sum(e["produced"] for e in per_op.values())

    return [
        row("operator_rejection_spread_pp", round(max(rates) - min(rates), 2), "pp",
            art, sha, "range of pre-filter rejection rate across the five operators",
            n=len(rates)),
        row("min_operator_rejection_rate", round(min(rates), 2), "%", art, sha,
            "least-filtered mutation operator", n=len(rates)),
        row("max_operator_rejection_rate", round(max(rates), 2), "%", art, sha,
            "most-filtered mutation operator", n=len(rates)),
        row("min_syntactic_validity", round(min(validity), 2), "%", art, sha,
            "lowest per-operator compile rate", n=len(validity)),
        row("guards_per_hundred_mutants", round(100.0 * guards / produced, 2), "n",
            art, sha, "integer guards the solver could extract per 100 mutants",
            n=produced,
            notes="the solver's reach is bounded by how few guards mutation exposes"),
    ]


# --------------------------------------------------------------------- p5

def analyse_p5(run_id: str) -> List[Dict[str, Any]]:
    art, sha = artifact_digest(run_id, "cascade_trials.json")
    data = load_artifact(run_id, "cascade_trials.json")
    hist = data["histogram"]
    trials = data["trials"]

    out = []
    for topology, counts in hist.items():
        counts = np.asarray(counts, dtype=float)
        # Bin 0 spans [0, 0.05): trials where the fault reached almost nobody.
        contained = 100.0 * counts[0] / counts.sum()
        # Bins from 0.5 upward: trials where at least half the population was hit.
        catastrophic = 100.0 * counts[10:].sum() / counts.sum()
        out.append(row(f"trials_fully_contained_{topology}", round(contained, 2), "%",
                       art, sha, "share of trials where under 5% of agents were affected",
                       n=trials))
        out.append(row(f"trials_catastrophic_{topology}", round(catastrophic, 2), "%",
                       art, sha, "share of trials where at least half the agents were affected",
                       n=trials))
    return out


# --------------------------------------------------------------------- p9

def analyse_p9(run_id: str) -> List[Dict[str, Any]]:
    art, sha = artifact_digest(run_id, "model_checking.json")
    data = load_artifact(run_id, "model_checking.json")
    enforced = data["with_invariant"]
    removed = data["without_invariant"]

    growth = 100.0 * (removed["states"] - enforced["states"]) / enforced["states"]
    branching = enforced["transitions"] / max(enforced["states"], 1)

    return [
        row("state_space_growth_without_invariant", round(growth, 2), "%", art, sha,
            "increase in reachable states when the safety invariant is removed",
            n=enforced["states"],
            notes="the invariant prunes the state space as well as guaranteeing safety"),
        row("mean_branching_factor", round(branching, 3), "x", art, sha,
            "transitions per reachable state under the enforced invariant",
            n=enforced["states"]),
        row("terminal_states_enforced", enforced["terminal_states"], "n", art, sha,
            "reachable commit or abort states", n=enforced["states"]),
    ]


ANALYSES: Dict[str, Callable[[str], List[Dict[str, Any]]]] = {
    "draft-review_symbol_graph_rag_vs_qlora_swe_bench_lite": analyse_p1,
    "draft-review_architectural_dynamics_long_12_page": analyse_p2,
    "draft-autonomous_code_synthesis_and_self_healing_multi_agent_systems": analyse_p3,
    "draft-review_enterprise_adoption_of_multi_agent_ai_systems_infr": analyse_p5,
    "draft-review_trustworthy_multi_agent_systems_formal_verification": analyse_p9,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=== deriving analysis statistics from recorded artifacts ===")
    for run_id, analyse in ANALYSES.items():
        path = os.path.join(RUNS, run_id, "measurements.jsonl")
        existing = {json.loads(l)["metric"] for l in open(path, encoding="utf-8") if l.strip()}
        derived = [r for r in analyse(run_id) if r["metric"] not in existing]

        print(f"  {run_id[6:52]:54} +{len(derived)} derived")
        for entry in derived[:3]:
            print(f"      {entry['metric']:44} {entry['value']}")

        if args.apply and derived:
            with open(path, "a", encoding="utf-8") as handle:
                for entry in derived:
                    handle.write(json.dumps(entry, sort_keys=True) + "\n")

    if not args.apply:
        print("\nDry run. Re-run with --apply to append.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
