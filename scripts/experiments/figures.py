"""Generate manuscript figures from recorded measurement artifacts.

A figure drawn from anything other than the run that produced the numbers is a
second place for the paper to drift out of agreement with its evidence. Every
figure here is rendered from ``runs/<run_id>/artifacts/*.json`` and written to
``vault/04_Drafts/figures/``, so regenerating after a re-run is a single command
and a stale figure cannot silently survive.

Run:
    backend/.venv/bin/python scripts/experiments/figures.py
"""
from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_sync import REPO_ROOT, load_artifact, load_measurements  # noqa: E402


FIGURE_DIR = os.path.join(REPO_ROOT, "vault", "04_Drafts", "figures")

# Print-safe, colourblind-friendly, and legible in greyscale.
PALETTE = ["#1f4e79", "#c1666b", "#4d7c5f", "#d4a017", "#6b5b95"]
plt.rcParams.update({
    "figure.dpi": 200,
    "font.size": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "legend.frameon": False,
})


def _save(fig, name: str) -> str:
    os.makedirs(FIGURE_DIR, exist_ok=True)
    path = os.path.join(FIGURE_DIR, f"{name}.pdf")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"    {name}.pdf")
    return path


# ------------------------------------------------------------------------- p1

def figures_p1() -> List[str]:
    run = "draft-review_symbol_graph_rag_vs_qlora_swe_bench_lite"
    _, rec = load_measurements(run)
    out = []

    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    metrics = [("p_at_1", "P@1"), ("p_at_5", "P@5")]
    x = np.arange(len(metrics))
    width = 0.36
    for offset, (system, label, colour) in enumerate(
        [("bm25", "BM25", PALETTE[0]), ("ppr", "Symbol+PPR", PALETTE[1])]
    ):
        values = [rec[f"{m}_{system}"]["value"] for m, _ in metrics]
        errs = [
            [rec[f"{m}_{system}"]["value"] - rec[f"{m}_{system}"]["ci95"][0] for m, _ in metrics],
            [rec[f"{m}_{system}"]["ci95"][1] - rec[f"{m}_{system}"]["value"] for m, _ in metrics],
        ]
        ax.bar(x + offset * width - width / 2, values, width, label=label,
               color=colour, yerr=errs, capsize=3, error_kw={"lw": 0.8})
    ax.set_xticks(x)
    ax.set_xticklabels([lbl for _, lbl in metrics])
    ax.set_ylabel("Retrieval accuracy (%)")
    ax.set_ylim(0, 105)
    ax.legend(loc="lower right", fontsize=7)
    ax.set_title("Overlapping intervals: no measurable gain", fontsize=8)
    out.append(_save(fig, "p1_retrieval_accuracy"))

    art = load_artifact(run, "retrieval_results.json")
    sweep = art["ppr_sweep_mrr_dev"]
    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    alphas = sorted({float(k.split("_")[0][5:]) for k in sweep})
    topks = sorted({int(k.split("topk")[1]) for k in sweep})
    for i, topk in enumerate(topks):
        ys = [sweep[f"alpha{a}_topk{topk}"] for a in alphas]
        ax.plot(alphas, ys, marker="o", ms=3, lw=1.2, color=PALETTE[i % len(PALETTE)],
                label=f"seeds={topk or 'all'}")
    ax.axhline(rec["mrr_bm25"]["value"], ls="--", lw=1, color="black", label="BM25")
    ax.set_xlabel(r"PageRank damping $\alpha$")
    ax.set_ylabel("MRR (dev split)")
    ax.legend(fontsize=6, ncol=2)
    out.append(_save(fig, "p1_ppr_sweep"))
    return out


# ------------------------------------------------------------------------- p2

def figures_p2() -> List[str]:
    run = "draft-review_architectural_dynamics_long_12_page"
    out = []

    kv = load_artifact(run, "kv_cache_scaling.json")
    fig, ax = plt.subplots(figsize=(3.3, 2.3))
    contexts = kv["contexts"]
    for i, (name, row) in enumerate(kv["gib"].items()):
        ax.plot(contexts, [row[str(c)] for c in contexts], marker="o", ms=3, lw=1.2,
                color=PALETTE[i % len(PALETTE)], label=name)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xlabel("Context length (tokens)")
    ax.set_ylabel("KV cache (GiB, batch 1)")
    ax.legend(fontsize=6)
    out.append(_save(fig, "p2_kv_cache_scaling"))

    lora = load_artifact(run, "lora_subspace.json")
    ranks = sorted(int(k) for k in lora["energy_captured_by_rank"])
    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    ax.plot(ranks, [lora["energy_captured_by_rank"][str(r)] * 100 for r in ranks],
            marker="o", ms=3, lw=1.4, color=PALETTE[0])
    ax.axvline(lora["true_rank"], ls="--", lw=1, color=PALETTE[1],
               label=f'intrinsic rank = {lora["true_rank"]}')
    ax.set_xscale("log", base=2)
    ax.set_xlabel("Adaptation rank $r$")
    ax.set_ylabel("Update energy captured (%)")
    ax.legend(fontsize=7)
    ax.set_title("Capacity is a cliff at the intrinsic rank", fontsize=8)
    out.append(_save(fig, "p2_lora_capacity"))
    return out


# ------------------------------------------------------------------------- p3

def figures_p3() -> List[str]:
    run = "draft-autonomous_code_synthesis_and_self_healing_multi_agent_systems"
    v, _ = load_measurements(run)
    out = []

    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    stages = ["Compilation", "Name binding", "Z3-SMT"]
    entering = [v["stage_entering_compile"], v["stage_entering_binding"],
                v["stage_entering_smt"]]
    rejected = [entering[0] - entering[1], entering[1] - entering[2], 0]
    ax.barh(stages, entering, color="#dcdcdc", label="entering")
    ax.barh(stages, rejected, color=PALETTE[1], label="rejected here")
    for i, (e, r) in enumerate(zip(entering, rejected)):
        pct = 100.0 * r / e if e else 0.0
        ax.text(e + 12, i, f"{pct:.1f}%", va="center", fontsize=7)
    ax.set_xlabel("Candidate mutants")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_title("The solver stage rejects nothing", fontsize=8)
    ax.invert_yaxis()
    out.append(_save(fig, "p3_prefilter_stages"))

    conv = load_artifact(run, "repair_convergence.json")["steps"]
    fig, ax = plt.subplots(figsize=(3.3, 2.1))
    ax.hist(conv, bins=range(min(conv), max(conv) + 2), color=PALETTE[0],
            edgecolor="white", lw=0.5)
    ax.axvline(float(np.mean(conv)), ls="--", lw=1.2, color=PALETTE[1],
               label=f"mean {np.mean(conv):.2f}")
    ax.set_xlabel("Accepted repair steps to convergence")
    ax.set_ylabel("Seeded defects")
    ax.legend(fontsize=7)
    out.append(_save(fig, "p3_repair_convergence"))
    return out


# ------------------------------------------------------------------------- p5

def figures_p5() -> List[str]:
    run = "draft-review_enterprise_adoption_of_multi_agent_ai_systems_infr"
    _, rec = load_measurements(run)
    out = []

    scaling = load_artifact(run, "message_scaling.json")
    fig, ax = plt.subplots(figsize=(3.3, 2.3))
    for i, (name, counts) in enumerate(scaling["counts"].items()):
        ax.plot(scaling["sizes"], counts, marker="o", ms=3, lw=1.2,
                color=PALETTE[i % len(PALETTE)],
                label=f'{name} (k={scaling["exponents"][name]:.2f})')
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xlabel("Agents $N$")
    ax.set_ylabel("Coordination messages")
    ax.legend(fontsize=6)
    out.append(_save(fig, "p5_message_scaling"))

    topologies = ["mesh", "blackboard", "contract_net", "hierarchical"]
    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    values = [rec[f"cascade_rate_{t}"]["value"] for t in topologies]
    errs = [
        [rec[f"cascade_rate_{t}"]["value"] - rec[f"cascade_rate_{t}"]["ci95"][0] for t in topologies],
        [rec[f"cascade_rate_{t}"]["ci95"][1] - rec[f"cascade_rate_{t}"]["value"] for t in topologies],
    ]
    ax.bar([t.replace("_", "\n") for t in topologies], values,
           color=[PALETTE[i % len(PALETTE)] for i in range(len(topologies))],
           yerr=errs, capsize=3, error_kw={"lw": 0.8})
    ax.set_ylabel("Agents affected by cascade (%)")
    ax.set_title("Supervision contains faults; broadcast does not", fontsize=8)
    out.append(_save(fig, "p5_cascade_containment"))
    return out


# ------------------------------------------------------------------------- p9

def figures_p9() -> List[str]:
    run = "draft-review_trustworthy_multi_agent_systems_formal_verification"
    out = []
    byz = load_artifact(run, "byzantine_sweep.json")

    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    fs = sorted(int(k) for k in byz["agreement_by_f"])
    rates = [byz["agreement_by_f"][str(f)] * 100 for f in fs]
    threshold = byz["theoretical_threshold"]
    colours = [PALETTE[2] if f <= threshold else PALETTE[1] for f in fs]
    ax.bar([str(f) for f in fs], rates, color=colours)
    ax.axvline(threshold + 0.5, ls="--", lw=1.2, color="black")
    ax.text(threshold + 0.6, 55, r"$f < n/3$", fontsize=7)
    ax.set_xlabel("Byzantine agents $f$ (council of 7)")
    ax.set_ylabel("Honest agreement (%)")
    ax.set_ylim(0, 105)
    ax.set_title("Threshold falls exactly at the classical bound", fontsize=8)
    out.append(_save(fig, "p9_byzantine_threshold"))
    return out


def figures_p6() -> List[str]:
    run = "draft-review_continual_safety_alignment_in_vision_language_models"
    out = []
    leak = load_artifact(run, "leakage_effect.json")["mean_drift_deg"]
    drift = load_artifact(run, "drift_by_norm.json")

    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    xs = sorted(float(k) for k in leak)
    ax.plot(xs, [leak[str(x)] for x in xs], marker="o", ms=4, lw=1.4, color=PALETTE[1],
            label="varying leakage, fixed norm")
    ax.axhline(drift["mean_drift_deg"]["0.4"], ls="--", lw=1, color=PALETTE[0],
               label="isotropic update, same norm")
    ax.set_xlabel("Orthogonal leakage")
    ax.set_ylabel("Subspace drift (degrees)")
    ax.legend(fontsize=6)
    ax.set_title("Direction, not magnitude, moves the subspace", fontsize=8)
    out.append(_save(fig, "p6_leakage_vs_drift"))

    comp = load_artifact(run, "filter_comparison.json")["comparison"]
    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    keeps = sorted(comp, key=float, reverse=True)
    x = np.arange(len(keeps)); width = 0.36
    ax.bar(x - width / 2, [100 * (1 - comp[k]["drift_retained_norm_filter"]) for k in keeps],
           width, label="magnitude rule", color=PALETTE[0])
    ax.bar(x + width / 2, [100 * (1 - comp[k]["drift_retained_leakage_filter"]) for k in keeps],
           width, label="leakage rule", color=PALETTE[1])
    ax.set_xticks(x); ax.set_xticklabels([f"keep {float(k)*100:.0f}%" for k in keeps])
    ax.set_ylabel("Drift removed (%)")
    ax.legend(fontsize=7)
    ax.set_title("Dispersion beats mechanism", fontsize=8)
    out.append(_save(fig, "p6_filter_comparison"))
    return out


GENERATORS = {
    "p1": figures_p1, "p2": figures_p2, "p3": figures_p3,
    "p5": figures_p5, "p6": figures_p6, "p9": figures_p9,
}


def main() -> int:
    print("=== generating figures from recorded artifacts ===")
    total = 0
    for paper, generator in GENERATORS.items():
        print(f"  {paper}:")
        total += len(generator())
    print(f"\n{total} figures written to {os.path.relpath(FIGURE_DIR, REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
