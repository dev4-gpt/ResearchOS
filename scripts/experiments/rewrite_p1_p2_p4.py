"""Rewrite p1, p2 and p4 to the measurements their experiments actually recorded.

Each paper keeps its theory and loses the empirical claims that no run supports.
The retired figures are asserted absent at the end, so a partial rewrite fails
loudly instead of leaving half a fabricated result behind.

Run:
    backend/.venv/bin/python scripts/experiments/rewrite_p1_p2_p4.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_sync import (  # noqa: E402
    ManuscriptEditor, ci_text, fill, load_artifact, load_measurements,
)


# ============================================================== p1

P1_ABSTRACT = r"""Automated software engineering at repository scale depends on retrieving the right context before any patch is generated [[arxiv_2405.01543]]. This paper asks whether structural retrieval over a symbol graph improves that context beyond lexical matching, and answers it with a controlled retrieval experiment rather than an end-to-end benchmark.

We build a symbol graph from imports and call references over a corpus of @@modules@@ Python modules (@@nodes@@ graph nodes, @@edges@@ edges), seed a Personalized PageRank diffusion with BM25 scores, and evaluate against ground truth given by the module that defines each queried symbol. Queries are docstrings with the defining symbol's own name stripped, so a hit cannot come from the answer leaking into the query. Diffusion hyperparameters are selected on a held-out development half and reported on @@n_test@@ unseen queries.

The result is negative. Symbol-graph diffusion is statistically indistinguishable from the BM25 baseline it re-ranks: MRR @@mrr_ppr@@ against @@mrr_bm25@@ ($\Delta = @@mrr_delta@@$, Cohen's $d = @@d@@$), and P@1 @@p1_ppr@@\% against @@p1_bm25@@\%. On this corpus the structural signal adds nothing that lexical matching has not already captured [[arxiv_2501.02497]].

We pair this with a census of SWE-bench Lite's @@swe_n@@ public instances. Every gold patch touches exactly one file (mean @@swe_files@@ files per patch, @@swe_single@@\% single-file), and the problem statement already names the file to edit in @@swe_named@@\% of cases (95\% CI @@swe_named_ci@@). Retrieval difficulty on that benchmark is therefore lower than a repository-scale framing suggests, which we argue is why retrieval-side gains there are easy to overstate [[crossref_10.1201_9788743808145-14]].

No language model was run in this study. We report no resolved-issue rate, no QLoRA comparison, and no training-cost figure; those require serving a large model and executing the benchmark's test suites."""

P1_PROTOCOL = r"""## Experimental Protocol

### Retrieval Corpus and Ground Truth

The retrieval corpus is @@modules@@ Python modules drawn from this project's backend and tooling. For each top-level function or class carrying a docstring of at least six words, we form a query from that docstring and take the defining module as the single relevant document. Both the symbol's own name and its module's filename are removed from the query, so lexical overlap with the answer cannot be produced by the identifier itself.

@@n_prepared@@ queries met the length threshold after filtering; @@n_dev@@ form the development split used to select diffusion hyperparameters and @@n_test@@ the held-out test split on which all reported numbers are computed.

### Systems Compared

1. **BM25** (baseline): Okapi BM25 over module token streams, $k_1 = 1.5$, $b = 0.75$, with identifiers split on underscores and case boundaries.
2. **Symbol-Graph + PPR**: the same BM25 scores seed a Personalized PageRank diffusion over a symbol graph of @@nodes@@ nodes and @@edges@@ edges, whose edges are `defines`, `defined_in` and cross-module `references`. Diffusion mass is projected back onto modules and re-ranked.

Selecting the diffusion's damping factor and seed breadth on the same queries used for reporting would measure the tuning rather than the method, so the sweep runs on the development split only. The selected configuration was $\alpha = @@alpha@@$ with the top @@topk@@ BM25 documents as seeds.

### Metrics

Precision@1, Precision@5 and Mean Reciprocal Rank, each with a percentile bootstrap 95\% confidence interval over @@boot@@ resamples, plus a Welch $t$-test and Cohen's $d$ on the paired MRR difference.

---

## Empirical Results

### Table 1: Retrieval Quality on Held-Out Queries ($n = @@n_test@@$)

| System | P@1 (\%) | 95\% CI | P@5 (\%) | 95\% CI | MRR | 95\% CI |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| BM25 | @@p1_bm25@@ | @@p1_bm25_ci@@ | @@p5_bm25@@ | @@p5_bm25_ci@@ | @@mrr_bm25@@ | @@mrr_bm25_ci@@ |
| Symbol-Graph + PPR | @@p1_ppr@@ | @@p1_ppr_ci@@ | @@p5_ppr@@ | @@p5_ppr_ci@@ | @@mrr_ppr@@ | @@mrr_ppr_ci@@ |

Paired difference in MRR: $\Delta = @@mrr_delta@@$, Cohen's $d = @@d@@$. The confidence intervals overlap across every metric, and the effect size is negligible by any conventional threshold.

The honest reading is that symbol-graph diffusion does not help here. Two properties of the corpus explain why. First, identifier vocabulary is highly discriminative in Python: a docstring describing a function usually shares rare tokens with the module that defines it, and BM25 already exploits that. Second, the graph's strongest edges connect a module to symbols it defines, which reinforces documents BM25 has already ranked highly rather than surfacing new ones. A structural signal should be expected to pay off where lexical overlap is weak -- cross-language repositories, heavily abbreviated identifiers, or queries phrased in user rather than developer vocabulary -- and testing that is the natural next experiment.

### Table 2: Retrieval Signal in SWE-bench Lite ($N = @@swe_n@@$ instances)

| Property | Value | Basis |
|:---|:---:|:---|
| Instances fetched | @@swe_n@@ | public dataset, live fetch |
| Mean files per gold patch | @@swe_files@@ | parsed from patch headers |
| Single-file patches | @@swe_single@@\% | share touching exactly one file |
| Problem statement names the gold file | @@swe_named@@\% | filename stem appears in the statement |

Every gold patch in SWE-bench Lite modifies exactly one file, and in @@swe_named@@\% of instances the problem statement already contains that file's name. A retriever that did nothing but extract filenames mentioned in the issue text would therefore locate the correct file for more than half the benchmark. This is a property of the benchmark, not of any system, and it bears directly on how retrieval-side improvements on SWE-bench Lite should be interpreted.

---
"""

P1_CONCLUSION = r"""We set out to test whether symbol-graph structure improves retrieval for repository-scale program repair, and found that it does not on the corpus we could measure. With hyperparameters selected on a held-out split and reported on @@n_test@@ unseen queries, Personalized PageRank over a symbol graph scores MRR @@mrr_ppr@@ against BM25's @@mrr_bm25@@ -- a difference of @@mrr_delta@@ with Cohen's $d = @@d@@$, well inside the noise.

We also find that SWE-bench Lite is an easier retrieval problem than its framing implies: all @@swe_n@@ gold patches are single-file, and @@swe_named@@\% of problem statements name the file to be edited. Retrieval gains reported on that benchmark should be read against this baseline.

The theoretical contributions stand independently of the negative empirical result: the heterogeneous graph formulation, the PAC-style bound for graph-guided retrieval, and the information-theoretic argument about structural locality. What we cannot claim is any resolved-issue rate, any comparison against QLoRA fine-tuning, or any inference-cost ratio; those require serving a large model and executing the benchmark's tests, which this study did not do. The retrieval harness and every recorded measurement are released so the negative result can be re-derived or overturned [[arxiv_2406.00584], [crossref_10.1201_9788743808145-14]]."""


def rewrite_p1() -> None:
    run = "draft-review_symbol_graph_rag_vs_qlora_swe_bench_lite"
    v, rec = load_measurements(run)
    art = load_artifact(run, "retrieval_results.json")

    ctx = {
        "modules": art["modules"], "nodes": art["graph_nodes"], "edges": art["graph_edges"],
        "n_prepared": art["dev_queries"] + art["test_queries"],
        "n_dev": art["dev_queries"], "n_test": art["test_queries"],
        "alpha": art["best_config"]["alpha"],
        "topk": art["best_config"]["seed_topk"] or "all",
        "boot": "2,000",
        "p1_bm25": f'{v["p_at_1_bm25"]:.2f}', "p1_ppr": f'{v["p_at_1_ppr"]:.2f}',
        "p5_bm25": f'{v["p_at_5_bm25"]:.2f}', "p5_ppr": f'{v["p_at_5_ppr"]:.2f}',
        "mrr_bm25": f'{v["mrr_bm25"]:.4f}', "mrr_ppr": f'{v["mrr_ppr"]:.4f}',
        "mrr_delta": f'{v["mrr_delta_ppr_minus_bm25"]:+.4f}',
        "d": f'{v["retrieval_cohens_d"]:.4f}',
        "p1_bm25_ci": ci_text(rec["p_at_1_bm25"]), "p1_ppr_ci": ci_text(rec["p_at_1_ppr"]),
        "p5_bm25_ci": ci_text(rec["p_at_5_bm25"]), "p5_ppr_ci": ci_text(rec["p_at_5_ppr"]),
        "mrr_bm25_ci": ci_text(rec["mrr_bm25"], 4), "mrr_ppr_ci": ci_text(rec["mrr_ppr"], 4),
        "swe_n": int(v["swebench_instances"]),
        "swe_files": f'{v["swebench_mean_files_per_patch"]:.3f}',
        "swe_single": f'{v["swebench_single_file_patch_rate"]:.2f}',
        "swe_named": f'{v["swebench_gold_file_named_rate"]:.2f}',
        "swe_named_ci": ci_text(rec["swebench_gold_file_named_rate"]),
    }

    editor = ManuscriptEditor("review_symbol_graph_rag_vs_qlora_swe_bench_lite")
    if editor.already_rewritten("This paper asks whether structural retrieval over a symbol graph"):
        return
    editor.replace_span("Automated software engineering demands precise context retrieval",
                        "---\n\n## Introduction", fill(P1_ABSTRACT, ctx) + "\n\n", "abstract")
    editor.replace_span("## System Architecture and Experimental Protocol",
                        "## Ablation Studies", fill(P1_PROTOCOL, ctx), "protocol+results")
    editor.replace_span("## Ablation Studies", "## Related Work",
                        "## Ablation of the Diffusion Configuration\n\n"
                        "The hyperparameter sweep in Section 4 is the only ablation this "
                        "study can support: @@sweep_n@@ configurations of damping factor "
                        "and seed breadth, scored on the development split. We report no "
                        "ablation over graph topology, call-graph edges or embedding "
                        "quality, because isolating those contributions requires an "
                        "end-to-end resolution metric that no run here produced.\n\n"
                        "Across the sweep the best development MRR was @@best_dev@@, and "
                        "the configuration achieving it did not separate from BM25 on the "
                        "held-out split. No configuration tested produced a positive "
                        "effect large enough to survive its confidence interval.\n\n---\n\n",
                        "ablation")
    editor.text = fill(editor.text, {
        "sweep_n": len(art["ppr_sweep_mrr_dev"]),
        "best_dev": f'{max(art["ppr_sweep_mrr_dev"].values()):.4f}',
    })
    editor.replace_to_end("Symbol-Graph RAG outperforms QLoRA parameter-efficient fine-tuning",
                          fill(P1_CONCLUSION, ctx) + "\n", "conclusion")
    # Remaining pockets of the retired benchmark, outside the replaced spans.
    editor.swap(
        "4. A decomposed ablation study ($N = 347$ variants) isolating the independent "
        "contributions of graph topology, call-graph edges, and embedding quality to "
        "resolution performance [[arxiv_2308.12898]].",
        "4. A hyperparameter study over the diffusion's damping factor and seed breadth, "
        "selected on a held-out split, establishing that no configuration tested separates "
        "from the lexical baseline [[arxiv_2308.12898]].")
    editor.swap(
        "For $|\\mathcal{H}| = 100$ (10 values of $K \\times 10$ values of $\\alpha$) and "
        "$\\delta = 0.05$: the generalization gap is at most "
        "$\\sqrt{(4.6 + 3.0)/600} = 0.112$. Since our empirical resolved rate is $38.7\\%$, "
        "the true population rate is at least $27.6\\%$ with 95% probability — strictly "
        "exceeding QLoRA's $27.3\\%$ empirical rate.",
        "The bound is left symbolic. Instantiating it requires an empirical resolved-issue "
        "rate, which this study does not measure: our evaluation is of retrieval quality, "
        "not end-to-end resolution.")
    editor.swap(
        "Our evaluation spans $N = 300$ SWE-bench Lite tasks with per-task bootstrap "
        "resampling ($B = 10{,}000$) for statistical robustness, and $N = 347$ ablation "
        "variant tasks.",
        "We answer a narrower question than the one that framing implies: whether "
        "structural retrieval improves context selection, measured directly, with no "
        "language model in the loop.", required=False)
    editor.assert_absent(["38.7\\%", "27.3\\%", "160 GB", "N = 347"])
    editor.save()


# ============================================================== p2

P2_ABSTRACT = r"""Transformer deployment is bounded by memory and compute budgets that parameter scaling alone cannot relieve [[arxiv_2005.14165], [arxiv_2406.00584]]. This paper derives those bounds analytically and verifies each derivation by computation rather than by hardware benchmark.

We solve the compute-optimal allocation problem numerically under the constraint $C = 6ND$, recovering a mean token-to-parameter ratio of @@tpp@@ across six compute budgets from $10^{19}$ to $10^{24}$ FLOPs. We give exact closed-form KV-cache arithmetic and evaluate it across attention variants: at a 32k context a grouped-query 7B configuration requires @@gqa@@\% less cache than multi-head, and multi-query @@mqa@@\% less, while a multi-head 7B model at 128k context needs @@kv128@@ GiB for a single sequence [[arxiv_2404.01131]].

For parameter-efficient adaptation we measure subspace capacity directly by singular value decomposition on weight-shaped update matrices: a rank-64 factorisation captures @@lora64@@\% of update energy at @@lora_param@@\% of dense parameter count, while rank 32 captures only @@lora32@@\%. The capacity curve is sharply non-linear around the intrinsic rank, which bounds how far low-rank adaptation can be compressed before it degrades.

Simulated Mixture-of-Experts routing over @@moe_tokens@@ token assignments across @@moe_experts@@ experts gives routing entropy from @@ent_unc@@ nats uncorrected to @@ent_bal@@ nats load-balanced, against a maximum of $\log @@moe_experts@@ = @@ent_max@@$.

Every figure here is either exact arithmetic or a simulation whose code is released. No accelerator was used, no model was trained, and no throughput or realised-VRAM measurement is reported [[crossref_10.1201_9788743808145-14]]."""

P2_METHOD = r"""## Methodology: Analysis and Simulation

### What Is Computed, and What Is Not

This study makes no hardware measurement. Its results fall into two categories, and the distinction is load-bearing:

**Exact arithmetic.** Compute-optimal allocation and KV-cache size are closed-form consequences of a stated architecture and a stated budget. A KV cache holds two tensors per layer per attention head per token; its size follows from those integers and needs no device to be correct.

**Simulation.** Low-rank subspace capacity is measured by singular value decomposition on synthetic weight-shaped matrices with a planted intrinsic rank. Routing entropy is measured over simulated token-to-expert assignments. These characterise the mathematical objects, not any trained model.

What is therefore absent: throughput, realised VRAM occupancy, benchmark accuracy after compression, and any comparison across GPU cluster configurations. Those require accelerators this study did not use.

### Table 1: Compute-Optimal Allocation Under $C = 6ND$

| Compute budget (FLOPs) | Optimal parameters $N$ | Optimal tokens $D$ | $D/N$ |
|:---|:---:|:---:|:---:|
@@alloc_rows@@

The ratio rises monotonically with budget, from @@tpp_min@@ at $10^{19}$ FLOPs to @@tpp_max@@ at $10^{24}$, with a mean of @@tpp@@. The optimum is found by scanning the one-dimensional family the constraint admits, not by quoting a published ratio.

### Table 2: Exact KV Cache Size (GiB, batch 1, fp16)

| Configuration | 2,048 | 8,192 | 32,768 | 131,072 |
|:---|:---:|:---:|:---:|:---:|
@@kv_rows@@

Cache size is linear in context length and in the number of key-value heads, so grouped-query attention buys a @@gqa@@\% reduction at 32k and multi-query @@mqa@@\%. The 128k multi-head 7B entry, at @@kv128@@ GiB for one sequence, is the clearest statement of why long-context serving is a memory problem before it is a compute problem.

### Table 3: Low-Rank Subspace Capacity (measured by SVD, $d_{\text{model}} = 1024$)

| Rank $r$ | Update energy captured (\%) | Parameters vs dense (\%) |
|:---:|:---:|:---:|
@@lora_rows@@

Capacity is sharply non-linear around the planted intrinsic rank: rank 32 captures @@lora32@@\% of update energy while rank 64 captures @@lora64@@\%, at @@lora_param@@\% of dense parameter count. Adaptation compressed below the intrinsic rank loses energy quickly; compressed above it, additional rank buys almost nothing.

### Table 4: Simulated MoE Routing Entropy (@@moe_tokens@@ assignments, @@moe_experts@@ experts)

| Routing scheme | Entropy (nats) | Fraction of maximum (\%) | Dead experts |
|:---|:---:|:---:|:---:|
@@moe_rows@@

Maximum attainable entropy is $\log @@moe_experts@@ = @@ent_max@@$ nats. No scheme produced a dead expert at this scale, so expert collapse in the strict sense did not occur; what varies is the sharpness of the load imbalance, which the entropy captures.

---
"""

P2_CONCLUSION = r"""Architectural choice governs deployment cost through relationships that can be derived exactly, and we derived them rather than measuring them on hardware. Compute-optimal allocation under $C = 6ND$ gives a mean token-to-parameter ratio of @@tpp@@ across six budgets. Exact KV-cache arithmetic shows grouped-query attention reducing cache by @@gqa@@\% and multi-query by @@mqa@@\% at 32k context, with a multi-head 7B model at 128k requiring @@kv128@@ GiB for a single sequence.

Singular value decomposition places low-rank adaptation capacity at @@lora64@@\% of update energy for rank 64 using @@lora_param@@\% of dense parameters, with a sharp fall to @@lora32@@\% at rank 32 -- the intrinsic rank is a cliff, not a gradual trade-off. Simulated routing entropy ranges from @@ent_unc@@ to @@ent_bal@@ nats against a @@ent_max@@ nat maximum.

The limits of this evidence are worth stating plainly. Exact arithmetic tells you what a cache costs, not what a served system achieves; SVD on planted-rank matrices tells you what a factorisation can represent, not what fine-tuning finds. Confirming that these bounds predict deployed behaviour requires accelerators and trained models, which this study did not have. Every calculation is released for re-execution [[arxiv_2406.00584], [crossref_10.1201_9788743808145-14]]."""


def rewrite_p2() -> None:
    run = "draft-review_architectural_dynamics_long_12_page"
    v, _ = load_measurements(run)
    alloc = load_artifact(run, "chinchilla_allocation.json")
    kv = load_artifact(run, "kv_cache_scaling.json")
    lora = load_artifact(run, "lora_subspace.json")
    moe = load_artifact(run, "moe_routing.json")

    alloc_rows = "\n".join(
        f'| $10^{{{round(__import__("math").log10(a["flops"]))}}}$ | '
        f'{a["optimal_params"]:.3e} | {a["optimal_tokens"]:.3e} | '
        f'{a["tokens_per_param"]:.1f} |'
        for a in alloc["allocations"]
    )
    contexts = [str(c) for c in kv["contexts"]]
    kv_rows = "\n".join(
        f"| {name} | " + " | ".join(f'{kv["gib"][name][c]:.3f}' for c in contexts) + " |"
        for name in kv["gib"]
    )
    ranks = sorted((int(k) for k in lora["energy_captured_by_rank"]))
    lora_rows = "\n".join(
        f'| {r} | {lora["energy_captured_by_rank"][str(r)] * 100:.2f} | '
        f'{100.0 * (2 * lora["d_model"] * r) / (lora["d_model"] ** 2):.2f} |'
        for r in ranks
    )
    moe_rows = "\n".join(
        f'| {name.replace("_", " ")} | {e["entropy_nats"]:.4f} | '
        f'{e["normalised_entropy"] * 100:.1f} | {e["dead_experts"]} |'
        for name, e in moe["results"].items()
    )
    ratios = [a["tokens_per_param"] for a in alloc["allocations"]]

    ctx = {
        "tpp": f'{v["chinchilla_tokens_per_param_mean"]:.2f}',
        "tpp_min": f"{min(ratios):.1f}", "tpp_max": f"{max(ratios):.1f}",
        "gqa": f'{v["kv_reduction_gqa_vs_mha"]:.1f}',
        "mqa": f'{v["kv_reduction_mqa_vs_mha"]:.1f}',
        "kv128": f'{v["kv_cache_gib_mha7b_128k"]:.1f}',
        "lora64": f'{v["lora_energy_rank64"]:.2f}',
        "lora32": f'{v["lora_energy_rank32"]:.2f}',
        "lora_param": f'{v["lora_param_fraction_rank64"]:.1f}',
        "moe_tokens": f'{moe["n_tokens"]:,}'.replace(",", "{,}"),
        "moe_experts": moe["n_experts"],
        "ent_unc": f'{v["routing_entropy_uncorrected"]:.4f}',
        "ent_bal": f'{v["routing_entropy_load_balanced"]:.4f}',
        "ent_max": f'{__import__("math").log(moe["n_experts"]):.4f}',
        "alloc_rows": alloc_rows, "kv_rows": kv_rows,
        "lora_rows": lora_rows, "moe_rows": moe_rows,
    }

    editor = ManuscriptEditor("review_architectural_dynamics_long_12_page")
    if editor.already_rewritten("This paper derives those bounds analytically and verifies"):
        return
    editor.replace_span("The rapid evolution of Large Language Models (LLMs) has established",
                        "---\n\n## Introduction", fill(P2_ABSTRACT, ctx) + "\n\n", "abstract")
    editor.replace_span("## Research Methodology & Empirical Benchmarks",
                        "## FLOPs Scaling Law", fill(P2_METHOD, ctx), "methodology")
    editor.replace_to_end("Structured architectural dynamics — combining low-rank parameter efficiency",
                          fill(P2_CONCLUSION, ctx) + "\n", "conclusion")
    editor.swap(
        "4. An empirical scaling benchmark across $N = 892$ multi-node GPU cluster "
        "configurations evaluating FLOPs efficiency, KV cache memory scaling, and "
        "inference throughput.",
        "4. A reproducible analytical suite: compute-optimal allocation solved "
        "numerically, exact KV-cache arithmetic across attention variants, SVD-measured "
        "low-rank capacity, and simulated routing entropy -- released with every "
        "recorded value. No accelerator is required to re-run it, and none was used.")
    editor.assert_absent(["N = 892", "68.2\\%", "98.4\\%", "3.1\\times"])
    editor.save()


# ============================================================== p4

P4_ABSTRACT = r"""Enterprise adoption of generative AI has outpaced the evidence base for evaluating it [[crossref_10.2139_ssrn.7052339]]. This review characterises that evidence base by census rather than by meta-analytic pooling, because the primary studies do not report the comparable effect sizes pooling requires.

Five search strings against the OpenAlex corpus returned @@identified@@ records, @@unique@@ unique after deduplication and @@screened@@ retaining a usable abstract. The literature is recent and dispersed: @@recent@@\% appeared in 2023 or later, spread across @@venues@@ distinct venues, with median citation count @@median_cit@@ and only @@zero_cit@@\% uncited.

The finding that matters for practice is how little of this literature reports data. Abstract-level screening for sample-size and study-design markers classifies @@empirical@@\% as empirical (bootstrap 95\% lower bound @@empirical_lo@@\%); the remainder is conceptual, positional, or descriptive. A field in which roughly two-thirds of the published record reports no measurement cannot yet support the quantitative ROI benchmarks that practitioners ask of it [[crossref_10.2139_ssrn.6374778]].

We therefore present a measurement framework and a taxonomy of what would need to be reported, rather than a pooled ROI estimate. Where individual studies report returns, those figures belong to the study that measured them and are attributed accordingly. This review conducted no survey of its own and reports no enterprise deployment count [[openalex_W4400993506]]."""

P4_METHOD = r"""## Review Methodology and Corpus Census

### Search and Screening

The corpus was assembled by querying the OpenAlex API with five search strings covering enterprise adoption, business value, return on investment, multi-agent workflow, and cost of ownership, restricted to publications from 2019 onward. Records were deduplicated by OpenAlex work identifier and screened for a reconstructable abstract and title.

### Table 1: Identification and Screening

| Stage | Records |
|:---|:---:|
| Identified across five search strings | @@identified@@ |
| Unique after deduplication | @@unique@@ |
| Screened (abstract and title present) | @@screened@@ |

### Table 2: Corpus Characteristics ($n = @@screened@@$)

| Property | Value |
|:---|:---:|
| Published 2023 or later (\%) | @@recent@@ |
| Distinct venues | @@venues@@ |
| Median citation count | @@median_cit@@ |
| Uncited share (\%) | @@zero_cit@@ |
| Open access share (\%) | @@oa@@ |
| Abstracts reporting data (\%) | @@empirical@@ |

### A Sampling Caveat That Changes the Reading

OpenAlex returns results ranked by relevance, so this corpus is the top of each query's ranking rather than a random sample of the literature. Rates computed over it are biased upward: the @@oa@@\% open-access share and median of @@median_cit@@ citations describe well-indexed, well-cited work and should not be read as properties of the field as a whole. The measure we rely on -- the share of abstracts reporting data -- is biased in the same direction, which makes @@empirical@@\% an optimistic upper estimate. That strengthens rather than weakens the conclusion drawn from it.

### Why No Pooled Effect Size

A meta-analysis requires primary studies reporting comparable outcomes with dispersion estimates. In this corpus most reported returns are single-organisation figures with no variance, no control condition, and no common definition of the denominator. Pooling them would manufacture precision that the underlying studies do not have. We report the census and the measurement framework instead.

---
"""


def rewrite_p4() -> None:
    run = "draft-review_enterprise_genai_roi"
    v, _ = load_measurements(run)
    ctx = {
        "identified": int(v["literature_identified_total"]),
        "unique": int(v["literature_unique_after_dedup"]),
        "screened": int(v["literature_screened"]),
        "recent": f'{v["literature_recent_share"]:.2f}',
        "venues": int(v["literature_distinct_venues"]),
        "median_cit": int(v["literature_median_citations"]),
        "zero_cit": f'{v["literature_zero_citation_share"]:.2f}',
        "oa": f'{v["literature_open_access_share"]:.2f}',
        "empirical": f'{v["literature_empirical_share"]:.2f}',
        "empirical_lo": f'{v["literature_empirical_share_ci_low"]:.2f}',
    }

    editor = ManuscriptEditor("review_enterprise_genai_roi")
    if editor.already_rewritten("This review characterises that evidence base by census"):
        return
    editor.replace_span("Enterprise adoption of Generative Artificial Intelligence (GenAI) and autonomous",
                        "## Quantitative Analysis & Empirical Evidence",
                        fill(P4_ABSTRACT, ctx) + "\n\n---\n\n", "abstract")
    editor.replace_span("## Quantitative Analysis & Empirical Evidence",
                        "## Compute Costs and Resource Management",
                        fill(P4_METHOD, ctx), "methodology")
    editor.save()


def main() -> int:
    print("=== rewriting manuscripts from recorded measurements ===")
    rewrite_p1()
    rewrite_p2()
    rewrite_p4()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
