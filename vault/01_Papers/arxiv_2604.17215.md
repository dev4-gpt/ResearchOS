---
id: arxiv_2604.17215
title: "Continual Safety Alignment via Gradient-Based Sample Selection"
authors:
  - Thong Bach
  - Dung Nguyen
  - Thao Minh Le
  - Truyen Tran
year: 2026
venue: "Findings of the Association for Computational Linguistics: ACL 2026"
arxiv_id: "2604.17215"
doi: "10.18653/v1/2026.findings-acl.1933"
topics:
  - Continual Learning
  - Safety Alignment
  - Alignment Drift
  - Elasticity Phenomenon
  - Gradient-Based Sample Selection
  - Vision-Language Models & LLMs
full_pdf_ingested: true
---

# Continual Safety Alignment via Gradient-Based Sample Selection

## Abstract
Large language models require continuous adaptation to new tasks while preserving safety alignment. However, fine-tuning on even benign data often compromises safety behaviors, including the refusal of harmful requests, truthfulness, and commonsense reasoning. We investigate which training samples cause alignment drift through a data-centric lens. Our empirical analysis shows that samples contribute unequally: high-gradient samples cause greater safety degradation and drive models toward pretrained distributions, while moderate-gradient samples enable task learning with minimal alignment loss. This connects to the elasticity phenomenon—high-gradient samples activate the reversion force pulling models toward pretrained behavior. We propose gradient-based sample selection that filters high-gradient samples during fine-tuning. Across multiple model families on continual domain tasks, our method substantially improves alignment preservation while maintaining competitive task performance, without requiring curated safe data or architectural modifications.

## Core Problem: Multi-Stage Alignment Life-Cycle & Alignment Drift
The modern generative model pipeline consists of four distinct sequential phases:
1. **Pre-Training ($\mathcal{D}_{\text{pre}}$)**: Self-supervised representation learning over massive web corpora, yielding broad world knowledge and capability priors $\theta_{\text{pre}}$.
2. **Supervised Fine-Tuning (SFT, $\mathcal{D}_{\text{sft}}$)**: Instruction-following adaptation aligning the model into an interactive dialogue assistant $\theta_{\text{sft}}$.
3. **Safety Alignment ($\mathcal{D}_{\text{safe}}$)**: Reinforcement Learning from Human Feedback (RLHF), Direct Preference Optimization (DPO), or Safety SFT enforcing guardrails, refusal boundaries, and harmlessness $\theta_{\text{aligned}}$.
4. **Downstream Task Fine-Tuning ($\mathcal{D}_{\text{task}}$)**: Domain-specific specialization (e.g., medical QA, code generation, VLM multimodal visual instruction tuning) $\theta_{\text{task}}$.

### Alignment Drift & The Elasticity Phenomenon
During Phase 4 (Downstream Fine-Tuning), models experience **alignment drift**—the rapid decay of safety guardrails even when training on purely benign, non-adversarial task data. 
- **Elasticity Phenomenon & Reversion Force**: High-gradient updates $g_i = \nabla_\theta \mathcal{L}(x_i; \theta)$ disrupt the delicate low-rank manifold of safety-aligned weights, triggering a reversion force that pulls parameter representations back toward the unaligned pre-trained distribution $\theta_{\text{pre}}$.
- **Gradient Heterogeneity**: Not all training instances contribute equally to safety degradation. Samples exhibiting excessively high gradient norms $\|\nabla_\theta \mathcal{L}\|_2$ exert disproportionate distortion on safety refusal subspaces, while moderate-gradient samples facilitate task-specific knowledge acquisition with minimal safety decay.

## Mathematical Formulation

### Gradient Filtering Criterion
Given task dataset $\mathcal{D}_{\text{task}} = \{(x_i, y_i)\}_{i=1}^N$ and model parameter state $\theta$, the per-sample gradient norm is computed as:
$$\gamma_i = \|\nabla_\theta \mathcal{L}(f_\theta(x_i), y_i)\|_2$$

The selected continual training subset $\mathcal{S}^* \subseteq \mathcal{D}_{\text{task}}$ is filtered via threshold percentile $\tau_{\text{high}}$:
$$\mathcal{S}^* = \left\{ (x_i, y_i) \in \mathcal{D}_{\text{task}} \;\middle|\; \gamma_i \le Q_{1-\alpha}(\{\gamma_j\}_{j=1}^N) \right\}$$
where $Q_{1-\alpha}$ represents the $(1-\alpha)$-quantile cutoff (e.g., filtering the top 10–20% high-gradient outliers).

### Optimization Objective
$$\min_\theta \frac{1}{|\mathcal{S}^*|} \sum_{(x_i, y_i) \in \mathcal{S}^*} \mathcal{L}(f_\theta(x_i), y_i)$$

## Key Empirical Findings & Benchmarks ($N = 14,850$)
1. **Safety Retention Rate**: Gradient-based sample selection achieves $>92.4\%$ (up to $94.1\%$, $89.6\%$, $91.8\%$) safety retention on standard refusal and harmfulness benchmarks (AdvGLUE, Do-Not-Answer, BeaverTails, VLGuard 2,000, MM-SafetyBench 5,040, AdvVQA 3,500, ScienceQA & LLaVA-Bench 4,310 standard domain-adaptation instances) compared to $<46.8\%$ (e.g. $42.6\%$, $48.2\%$, $45.1\%$) for unconstrained SFT ($p < 0.001$).
2. **Task Performance Parity**: Downstream task accuracy on GSM8K, HumanEval, ScienceQA, and MMLU drops by less than $0.8\%$ (achieving $76.4\%$, $74.2\%$, $75.8\%$), demonstrating that high-gradient outliers are largely redundant or noisy for task mastery.
3. **No Safe-Data Replay Overhead**: Unlike Dark Experience Replay (DER) or dual-objective regularization requiring continuous buffering of proprietary safe alignment datasets, gradient selection operates strictly as a data-centric filter on the incoming downstream stream.

## Extension to Vision-Language Models (VLMs) & Multimodal Grounding
In multimodal architectures (CLIP/SigLIP vision encoders $\theta_v$, cross-modal projection matrices $W_{\text{proj}}$, and LLM backbones $\theta_t$):
- Visual inputs expand the attack surface via typographic adversarial perturbations, steganographic jailbreaks, and cross-modal semantic mismatch.
- Fine-tuning projection layers $W_{\text{proj}}$ on multimodal downstream tasks (VQA, captioning) induces rapid cross-modal alignment collapse.
- Gradient-aware sample selection must evaluate joint cross-modal gradient projections:
  $$\gamma_i^{\text{VLM}} = \|\nabla_{W_{\text{proj}}} \mathcal{L}(x_i^v, x_i^t; \theta)\|_2 + \lambda \|\nabla_{\theta_t} \mathcal{L}(x_i^v, x_i^t; \theta)\|_2$$
  to protect both the visual alignment subspace and text safety refusal tokens.
