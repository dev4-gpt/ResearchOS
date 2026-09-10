# Method Mapping: LLM Paper → VLM Replication

Every substitution below was verified against real, published literature during project scoping (Sept 2026) — none are invented. Where a citation could not be independently verified in that session, it is marked accordingly rather than asserted.

## 1. Base models

All three of the paper's model families get a VLM counterpart — this is the default target, not a stretch goal. Validation is stepwise (cheapest model first, Phase 1), but once validated, all three run as the default (Phase 2 onward), ideally in parallel once compute allows. See the project plan for the full phasing.

| Role | Original (paper) | VLM substitute | Notes |
|---|---|---|---|
| Aligned instruct model θ0, #1 (Phase 1 validation + always included) | Qwen2.5-7B-Instruct | **Qwen2-VL-2B-Instruct** | Qwen family; smallest, runs on M3 Pro — used first to validate the pipeline and the phenomenon cheaply before the other two are added |
| Aligned instruct model θ0, #2 | LLaMA-3.1-8B-Instruct | **LLaVA-1.6-7B** | Vicuna/LLaMA-based lineage — different vendor and base architecture from Qwen2-VL, standard visual-instruction-tuning (not RLHF) |
| Aligned instruct model θ0, #3 | Qwen3-4B-Instruct | **LLaVA-RLHF** | Sun et al., "Aligning Large Multimodal Models with Factually Augmented RLHF," arXiv:2309.14525 (2023) — the closest VLM analog to the paper's own RLHF-aligned starting point; LLaVA-1.6/Qwen2-VL-Instruct are instruction-tuned but not necessarily RLHF-safety-aligned in the same sense, so this model specifically covers that gap |
| θ_pretrain reference (for reversion-direction / KL-to-pretrained analyses) | Matched non-instruct base checkpoint (e.g. Qwen2.5-1.5B for Qwen2.5-1.5B-Instruct) | Base (pre-instruction-tuned) VLM checkpoint of the same family, per model above | Must be same family, matching the paper's own App. D.3 protocol — a text-only LLM base would measure the wrong distribution |

**Why these three, together:** they vary both architecture (Qwen vs. Vicuna/LLaMA lineage) *and* alignment procedure (standard instruction-tuning vs. explicit RLHF), which lets the replication speak to the paper's own cross-architecture variation finding (Table 6: 3.6×/2.4×/2.8× ASR reduction across families, unexplained by the paper) and potentially extend it — is the variation about architecture, alignment procedure, or both?

## 2. Downstream task sequence

| Order | Original (paper) | VLM substitute | Source |
|---|---|---|---|
| 1 (benign, first — reduces excess refusal) | Dolly (15K instruction examples) | LLaVA-Instruct-150K subset | Liu, Li, Wu, Lee, "Visual Instruction Tuning," NeurIPS 2023, arXiv:2304.08485 |
| 2 (reasoning) | GSM8K (8.5K math word problems) | MathVista | Lu et al., "MathVista: Evaluating Mathematical Reasoning of Foundation Models in Visual Contexts," ICLR 2024 (confirmed via ICLR proceedings this session) |
| 3 (domain QA) | MedMCQA (medical multiple-choice) | VQA-RAD (primary) or SLAKE (alternate) | VQA-RAD: Lau et al., *Scientific Data*, 2018. SLAKE: Liu et al., 2021 (both confirmed this session) |
| 4 (reading comprehension) | SQuAD v2 | DocVQA | Mathew, Karatzas, Jawahar, "DocVQA: A Dataset for VQA on Document Images," WACV 2021 (confirmed this session) |

## 3. Safety / attack-success-rate (ASR) benchmarks

| Original | VLM substitute | Source | Notes |
|---|---|---|---|
| AdvBench (520 harmful queries) | MM-SafetyBench | Liu et al., 2024 — 13 safety-critical scenarios, 5,040 text-image pairs (confirmed this session) | Each benchmark defines its own scoring protocol; use that protocol rather than forcing one judge model across all of them |
| — | FigStep | Gong et al., 2023 — typographic jailbreak: harmful instruction embedded as image text, benign text prompt | confirmed this session |
| — | JailBreakV-28K | Luo et al., 2024 — 16 harm scenarios, large-scale | confirmed this session |
| HarmBench | Keep a text-only HarmBench slice, attacking the VLM via text-only prompts | Mazeika et al., 2024 (original) | Preserves the paper's "diverse attack vectors" intent; the VLM's language decoder is still attackable through text alone |
| Optional / stretch: modality-native attack | Adversarial pixel-perturbation jailbreak against the vision encoder | Qi, Huang, Panda, Henderson, Wang, Mittal, "Visual Adversarial Examples Jailbreak Aligned Large Language Models," arXiv:2306.13213, AAAI 2024 (confirmed this session) | Has **no text-only analog** — a VLM-native attack surface the original paper structurally could not test |
| Llama-Guard-3-8B judge | Same model, applied to the VLM's **text output** (response only, as in the original — it never judged the prompt) | Meta AI, 2024 (as cited in the source paper) | No substitution needed; add LlavaGuard (Helff et al., CVPRW 2024, arXiv:2406.05113) only if also judging image-side harmful content becomes a design goal |

## 4. Alignment-drift / safety-basin measurement

| Original | VLM substitute | Notes |
|---|---|---|
| VISAGE (weight-space perturbation, N=100 directions, ASR-based safety margin) | **Identical procedure**, applied to the VLM's fine-tuned (LoRA) parameters | Peng et al., 2024 (source paper's own citation) — this is a measurement methodology, not a benchmark, so it is model-agnostic and needs no substitution |
| KL-divergence to pretrained/aligned distributions (Table 3) | Same computation over the VLM's text-output token distributions | No change — operates on next-token distributions regardless of modality |

## 5. Truthfulness / hallucination

| Original | VLM substitute | Source |
|---|---|---|
| TruthfulQA | MMHal-Bench (primary) | Sun et al., 2023 — open-ended, GPT-4-graded hallucination benchmark (confirmed this session) |
| — | POPE (secondary) | Li et al., 2023 — polling-based object-hallucination probing (confirmed this session) |

## 6. General capability

| Original | VLM substitute | Notes |
|---|---|---|
| ARC-C, BoolQ, HellaSwag, Winogrande via lm-evaluation-harness | Same benchmarks, run in the VLM's **text-only mode** | Verify per chosen model at implementation time that text-only mode runs cleanly without image input |
| lm-evaluation-harness (Gao et al., 2024) | **lmms-eval** | EvolvingLMMs-Lab, github.com/EvolvingLMMs-Lab/lmms-eval — confirmed on GitHub this session; "One-for-All Multimodal Evaluation Toolkit" |

## 7. Training configuration

| Original | VLM substitute | Notes |
|---|---|---|
| LoRA rank 32, α=64, AdamW, lr=1e-4, batch 32, 1 epoch/task | Same starting point | Reduce rank/epoch only under M3 Pro memory pressure — log any deviation in the run manifest |
| LoRA applied to full (text-only) decoder | LoRA on **language decoder only**; vision encoder + connector frozen | Standard VLM fine-tuning practice; keeps elastic-reversion argument well-defined (pull is toward the decoder's own pretraining) |
| Per-sample gradient norm `G_i` over all trainable params | `G_i` computed over **LoRA parameters only** | Paper's own §F names this as an overhead-reduction path; full-VLM per-sample gradients aren't tractable on the M3 Pro |

## 8. Baselines

| Original | Feasibility for this replication | Tier |
|---|---|---|
| Baseline (standard FT) | Directly portable | Must-have |
| Random | Directly portable | Must-have |
| KL regularization | Directly portable (architecture-agnostic) | Should-have |
| EWC | Directly portable (architecture-agnostic, Fisher-based) | Should-have |
| Gradient clipping | Directly portable | Should-have (cheap ablation, high value per paper's own Appendix E.4) |
| O-LoRA | Requires orthogonal-subspace LoRA implementation — real architectural work | Stretch |

## 9. Items intentionally left unverified pending implementation

- Whether the chosen base VLM (Qwen2-VL-2B-Instruct) cleanly supports a text-only inference mode for the commonsense benchmarks — check before relying on it.
- Exact per-benchmark ASR scoring protocol for MM-SafetyBench / FigStep / JailBreakV-28K — confirm each benchmark's official evaluation code rather than assuming Llama-Guard applies uniformly.
- synapticjs/synaptic (github.com/synapticjs/synaptic) — a JavaScript neural-network builder library, unrelated to this Python/PyTorch pipeline. Not adopted as a dependency; flagged here only in case its naming-convention philosophy is wanted for `src/` module boundaries — pending user confirmation.
