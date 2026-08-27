"""Insert figure references into the grounded manuscripts.

Each figure is anchored after a stable passage in the results section it
illustrates. Idempotent: a manuscript that already references the figure is left
alone, so this can be re-run after regenerating figures.

Run:
    backend/.venv/bin/python scripts/experiments/insert_figures.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_sync import DRAFTS  # noqa: E402


# (draft stem, anchor passage, image file, caption)
PLACEMENTS = [
    (
        "review_symbol_graph_rag_vs_qlora_swe_bench_lite",
        "The confidence intervals overlap across every metric",
        "p1_retrieval_accuracy.pdf",
        "Retrieval accuracy on held-out queries. Error bars are percentile "
        "bootstrap 95\\% confidence intervals. The intervals overlap on both "
        "metrics, so the symbol-graph re-ranker is not separable from the "
        "lexical baseline it re-ranks.",
    ),
    (
        "review_symbol_graph_rag_vs_qlora_swe_bench_lite",
        "No configuration tested produced a positive effect",
        "p1_ppr_sweep.pdf",
        "Development-split MRR across the diffusion sweep. No damping factor or "
        "seed breadth lifts the re-ranker above the BM25 baseline (dashed).",
    ),
    (
        "review_architectural_dynamics_long_12_page",
        "the clearest statement of why long-context serving is a memory problem",
        "p2_kv_cache_scaling.pdf",
        "Exact KV cache size against context length, log-log. Slope one confirms "
        "linear growth; the vertical offsets are the head-sharing factor.",
    ),
    (
        "review_architectural_dynamics_long_12_page",
        "compressed above it, additional rank buys almost nothing",
        "p2_lora_capacity.pdf",
        "Update energy captured against adaptation rank, measured by SVD. "
        "Capacity saturates abruptly at the planted intrinsic rank.",
    ),
    (
        "autonomous_code_synthesis_and_self_healing_multi_agent_systems",
        "The marginal value of the symbolic stage on this corpus is zero.",
        "p3_prefilter_stages.pdf",
        "Candidates entering each pre-filter stage and the share rejected there. "
        "Static name binding carries the filter; the SMT stage rejects nothing.",
    ),
    (
        "autonomous_code_synthesis_and_self_healing_multi_agent_systems",
        "The empirical convergence profile is consistent with Theorem 1",
        "p3_repair_convergence.pdf",
        "Accepted repair steps to convergence over 300 seeded defects. Every "
        "trial terminated, with a worst case well inside the theoretical bound.",
    ),
    (
        "review_enterprise_adoption_of_multi_agent_ai_systems_infr",
        "The measured exponents confirm the asymptotic separation",
        "p5_message_scaling.pdf",
        "Coordination messages against agent count, log-log. The fitted exponent "
        "separates quadratic mesh broadcast from the linear coordinated topologies.",
    ),
    (
        "review_enterprise_adoption_of_multi_agent_ai_systems_infr",
        "Two results qualify the naive reading that hierarchy dominates.",
        "p5_cascade_containment.pdf",
        "Mean fraction of agents affected by a cascade, with bootstrap 95\\% "
        "confidence intervals over 20,000 trials per topology.",
    ),
    (
        "review_trustworthy_multi_agent_systems_formal_verification",
        "so the measured threshold coincides exactly with the classical limit",
        "p9_byzantine_threshold.pdf",
        "Honest agreement against the number of Byzantine agents in a council of "
        "seven. Agreement collapses precisely where the $f < n/3$ bound predicts.",
    ),
]


def main() -> int:
    print("=== inserting figure references ===")
    inserted = skipped = 0
    by_stem = {}
    for stem, anchor, image, caption in PLACEMENTS:
        by_stem.setdefault(stem, []).append((anchor, image, caption))

    for stem, items in by_stem.items():
        path = os.path.join(DRAFTS, f"{stem}.md")
        text = open(path, encoding="utf-8").read()
        for anchor, image, caption in items:
            if image in text:
                skipped += 1
                continue
            if anchor not in text:
                print(f"  WARNING {stem}: anchor not found for {image}")
                continue
            end = text.index(anchor) + len(anchor)
            end = text.find("\n", end)
            end = len(text) if end == -1 else end
            block = f"\n\n![{caption}](figures/{image})\n"
            text = text[:end] + block + text[end:]
            inserted += 1
        open(path, "w", encoding="utf-8").write(text)
        print(f"  {stem[:48]}")

    print(f"\n{inserted} inserted, {skipped} already present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
