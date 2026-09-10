# Paper Analysis: Continual Safety Alignment via Gradient-Based Sample Selection

Source: Bach, Nguyen, Le, Tran. "Continual Safety Alignment via Gradient-Based Sample Selection." arXiv:2604.17215v1 [cs.LG], 19 Apr 2026. A2I2, Deakin University / Penn State.

This document is a faithful summary of what the paper states, drawn from the full text (18 pages including appendices). No numbers or claims below go beyond what the paper itself reports. Table/figure/section references point back to the source.

## 1. The problem being studied

**Not** a pretrain → SFT → safety-alignment → downstream-fine-tuning pipeline. The paper starts from an **already safety-aligned instruction-tuned model** (θ0 — one that has already been through RLHF/DPO/Constitutional-AI-style alignment) and asks what happens when that model undergoes **continual fine-tuning across a sequence of downstream task domains**.

Formally (Eq. 3, 5): given θ0 and a sequence of task datasets {D1, ..., DT}, standard continual learning minimizes task loss subject to not forgetting prior tasks. The paper adds a second constraint: the model must stay inside its **safety basin** B throughout training, not just at convergence — i.e., alignment drift Δalign(t) must stay under a tolerance δ at every step, not just the end.

Three challenges make this constraint hard to enforce directly (Section 2.3): the safety metric is expensive to compute, non-differentiable, and operates at the model level while training operates at the sample level. The paper's response is to reframe this as a **data-centric / sample-selection problem**: which individual training samples cause the drift, and can they simply be filtered out?

## 2. Theoretical grounding (imported from prior work, not original to this paper)

- **Safety basin framework** (Peng et al., 2024). Alignment is a *region* in parameter space, not a point. Perturbing an aligned model's weights along random directions reveals a flat interior (safety holds under small perturbations) with a **sharp boundary** — safety collapses in a step function, not gradually, when a perturbation crosses out of the basin. This is unlike the capability landscape, which degrades gradually. The **VISAGE** score (Eq. 1) quantifies basin volume by averaging the safety margin (Smax − attack success rate) over N=100 random perturbation directions at calibrated magnitude.
- **Elasticity framework** (Ji et al., 2024). Models exert an "elastic force" pulling them back toward their pretrained distribution during any fine-tuning, proportional to dataset size: `F_elastic ∝ |D_i| · ΔKL(p_θ || p_Di)`. Because pretraining corpora vastly outnumber alignment datasets, the pretrained distribution exerts a much stronger pull than the (comparatively tiny) alignment data does. This predicts both *resistance* (pretrained models resist being aligned in the first place) and *rebound* (aligned models drift back toward pretrained behavior under any further fine-tuning).

## 3. The paper's own hypothesis and how it was tested

**Hypothesis:** samples don't contribute to drift equally. Samples where the aligned model's predictions diverge sharply from the fine-tuning target (i.e., **high gradient norm** `G_i = ||∇θ L(x_i, y_i; θ0)||₂`) sit at "alignment tension points" and disproportionately activate elastic reversion.

**Test setup (Section 3):** fine-tune LLaMA-3.1-8B-Instruct and Qwen-2.5-7B-Instruct on Dolly (15K benign instruction examples), comparing Random, High-Gi (top 20% by gradient norm), Moderate-Gi (20% closest to median), and (in a follow-up ablation) Low-Gi (bottom 20%) — each using 3,000 samples (20% of the set), identical hyperparameters (lr=2e-5, 3 epochs, AdamW).

**Results supporting the hypothesis:**
- **Table 1** (Low-Gi vs Moderate-Gi, 3 model families): Low-Gi gives the best safety but costs 0.8–1.9 points of task performance versus Moderate-Gi — a clean Pareto tradeoff across the gradient spectrum (Low-Gi safest, Moderate-Gi best task performance, High-Gi worst on both).
- **Table 2**: High-Gi retains only 62–72% of original VISAGE and multiplies ASR 5–9×; Moderate-Gi retains 83–88% VISAGE with only 1.5–2× ASR increase.
- **Figure 2**: visualized safety landscape for Qwen-2.5-7B after Dolly fine-tuning — High-Gi narrows the safety basin sharply; Moderate-Gi stays close to the original aligned model's basin width.
- **Table 3** (KL-divergence): High-Gi training moves the model's output distribution *closer* to the pretrained distribution and *farther* from the aligned distribution, compared to Random/Moderate-Gi — direct evidence consistent with elastic reversion.
- **Section 3.2 (gradient direction analysis, explicitly labeled "preliminary")**: using a TopK-Cosine metric (restricted to the k=1000 dimensions most changed during alignment, since raw high-dimensional cosine similarity is ~0 everywhere), high-gradient samples show modestly higher directional alignment with the reversion direction `r = θ_pretrain − θ_aligned` in final-layer parameters (Qwen2.5: V/O projections, r=0.39–0.41; LLaMA: MLP, r=0.18), with **no effect in middle layers** (|r|<0.07). Correlations are modest (r=0.18–0.41) and the affected component differs by architecture — the paper is explicit that this is preliminary support, not proof, and that the method's core selection criterion (magnitude only, not direction) works "regardless of whether the directional hypothesis fully holds."

## 4. The method: Gradient-Based Sample Selection (Algorithm 1)

Three-stage batch selection, run each training step:

1. **Loss-based pre-filter.** Compute per-sample loss `L_i`. Keep only samples with `L_i ∈ [μ_L − σ_L, μ_L + σ_L]` — this removes both memorized samples (very low loss) and outliers (very high loss), retaining ~68% of candidates and cutting subsequent gradient computation by ~32%.
2. **Gradient norms on survivors.** Compute `G_i = ||∇θ L(x_i, y_i; θ)||₂` only for the pre-filtered candidates (not the full batch — this is the compute-saving step).
3. **Median-based selection.** `μ_G = median({G_i})`; select the `⌊ρ|B|⌋` samples whose gradient norm is closest to `μ_G` (median, not mean, chosen specifically for robustness to heavy-tailed gradient distributions).

Default `ρ = 0.2` (recommended range `[0.15, 0.25]`). Sensitivity analysis (Table 5, Qwen3-4B, full 4-task pipeline) shows ASR stays low (2.7–6.0%) across `ρ ∈ [0.1, 0.4]`; smaller ρ trades a small amount of task performance for slightly better safety; larger ρ converges toward random-sampling behavior.

## 5. Full experimental results

**Setup (Section 5.1):** three model families — Qwen2.5-7B-Instruct, LLaMA-3.1-8B-Instruct, Qwen3-4B-Instruct — fine-tuned **sequentially** on four domains: **Dolly → GSM8K → MedMCQA → SQuAD v2**. Dolly goes first specifically "to reduce excessive refusal behavior in RLHF-aligned models." LoRA (rank 32, α=64), AdamW, lr=1e-4, batch 32, 1 epoch/task, averaged over 3 seeds.

**Baselines:** Baseline (standard FT), Random, KL-divergence regularization against the aligned model, O-LoRA (orthogonal subspace learning), EWC (Fisher-based continual learning), and gradient-norm clipping (clip=0.5, best of {0.1, 0.5, 1.0}).

**Evaluation:** task performance via lm-evaluation-harness; safety via ASR on AdvBench (520 harmful queries, judged by Llama-Guard-3-8B) and HarmBench; truthfulness via TruthfulQA; general capability via ARC-C, BoolQ, HellaSwag, Winogrande.

**Key results:**
- **Table 6** — checkpoint-averaged ASR: Moderate-Gi achieves 10.2% (Qwen2.5), 18.3% (LLaMA-3.1), 6.0% (Qwen3) vs. Baseline's 36.7%, 44.2%, 16.6% — reductions of 3.6×, 2.4×, 2.8×. EWC *worsens* safety on LLaMA-3.1 relative to baseline (40.2% vs 44.2%), showing Fisher-based regularization (designed for task-parameter protection) doesn't address alignment. Gradient clipping gives only marginal improvement (31.2% on Qwen2.5), evidence the issue is *which* samples produce gradients, not gradient magnitude alone.
- **Table 9** — HarmBench ASR on LLaMA-3.1 across the full pipeline: Moderate-Gi 5.0% vs Baseline 27.8% (5.6× reduction), generalizing beyond AdvBench.
- **Table 7/8** — continual-learning performance: Moderate-Gi's task-average advantage grows on more forgetting-prone models (58.1% vs 55.0% Random vs 54.2% Baseline on Qwen3). BWT improves from −18.5% (Baseline) to −4.3% (Moderate-Gi) on Qwen3 — a 14.2-point improvement; Forgetting Measure drops 4.3× correspondingly.
- **Figure 3** — task-interference matrix: MedMCQA training causes −32.5% interference with GSM8K under Baseline on Qwen3, vs. only −2.5% under Moderate-Gi; total interference drops from −37.1% to −8.5% (4.4× reduction).
- **Table 8 "Max Drop"** — worst single-step performance drop: 5.6% (Moderate-Gi) vs 32.5% (Baseline) on Qwen3, a 5.8× reduction — the paper frames this as directly relevant to safety because catastrophic single-step drops are what risk crossing a safety-basin boundary.
- **Cross-architecture variation** is explicitly noted and not fully explained: Qwen2.5 shows 3.6× ASR reduction, Qwen3 2.8×, LLaMA-3.1 only 2.4× with no task-performance gain over baseline — attributed to differences in each family's alignment procedure, not a limitation of the method itself.
- **Truthfulness/capability**: Moderate-Gi matches or exceeds baselines on TruthfulQA (42.5–42.8%) and stays within 1–2 points on ARC-C/BoolQ/HellaSwag/Winogrande — sample selection is not trading general capability for safety.

## 6. Why not simpler alternatives (Appendix E.1, E.4)

- **What gets filtered is a format-mismatch signal, not a content signal.** Auditing 10,000 Dolly samples (Table 12): High-Gi samples average only 11.5 response tokens with high per-token loss (5.23) and are dominated by short-answer tasks (classification 28.6%, closed QA 15.2%). Large gradients arise because the aligned model's verbose output distribution diverges from terse targets — not because the content is harmful or semantically unusual. The paper is explicit that this indicates **no fairness concern**.
- **Gradient clipping is not a substitute** (Table 14): clipping bounds step size but still trains on high-gradient samples, so the model still receives a reversion-pushing signal from their content; best clipping config gets 31.2% ASR vs. 10.2% for selection — clipping attenuates magnitude, selection removes the offending samples entirely.

## 7. Robustness checks (Appendix E.5, 4.2)

- **Task-order robustness**: two alternate orderings plus a domain substitution (Alpaca replacing Dolly) on LLaMA-3.1 all show Moderate-Gi achieving best-or-near-best ASR *and* task accuracy — Pareto dominance independent of ordering (Table 15).
- **ρ sensitivity**: robust across ρ ∈ [0.1, 0.4] (Table 5), as noted above.
- **Computational overhead** (Table 16): 1.5× baseline wall-clock time (21.6 min/epoch vs 14.4 min baseline on a single H100, Qwen2.5-7B on Dolly) — due to gradient computation on filtered candidates. Inference cost is unchanged; the paper suggests gradient checkpointing, LoRA-only gradient computation, and caching gradient statistics across epochs as mitigations, none of which were implemented in the paper itself.

## 8. Explicitly stated limitations (Section F, verbatim in substance)

1. **Computational overhead** — 1.5× training cost, may be prohibitive for very large models or tight compute budgets.
2. **Exact gradients only** — per-sample gradients require sequential backward passes; approximation techniques (influence functions, gradient sketching) were not tried and might affect selection quality.
3. **Fixed selection ratio** — ρ=0.2 used throughout; no adaptive threshold based on observed drift.
4. **No formal theory** connecting sample gradients to safety-basin geometry — the paper's support is empirical, and Section 3.2's directional analysis is explicitly labeled preliminary.
5. **Multi-modal models — named directly as the paper's own future work:** *"Our experiments focus on text-only models. Extending gradient-based selection to vision-language models or other modalities requires further investigation."* This is the explicit basis for the VLM replication project this document accompanies.

## 9. What this paper does NOT claim (guardrails for the replication write-up)

- It does **not** study a separate pretraining → SFT → safety-alignment → downstream-fine-tuning pipeline as distinct stages; θ0 is already a fully aligned instruct model throughout.
- It does **not** use adversarial or intentionally harmful fine-tuning data anywhere — Dolly, GSM8K, MedMCQA, and SQuAD v2 are all benign task datasets; the safety degradation studied is *unintentional*, a side effect of ordinary task adaptation.
- It does **not** test model families or task domains beyond the three LLM families (Qwen2.5-7B, LLaMA-3.1-8B, Qwen3-4B) and four task domains (Dolly, GSM8K, MedMCQA, SQuAD v2) named above — any broader claim requires new evidence, not extrapolation from this paper.
- It does **not** claim to have proven the mechanism by which high-gradient samples cause drift — the gradient-direction analysis is explicitly preliminary, with modest and architecture-dependent correlations. The method's practical effectiveness (magnitude-based filtering) does not depend on that mechanistic story being fully correct.
- It does **not** provide a defense against intentional/adversarial fine-tuning attacks — related work on that (Vaccine, Booster, LISA, Safe LoRA, Antidote, etc.) is discussed as related but distinct (Appendix A), addressing single-step harmful fine-tuning rather than the continual, benign-data setting this paper studies.
