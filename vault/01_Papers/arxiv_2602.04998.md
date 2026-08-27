---
title: "Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning"
authors:
  - "Yu-Ang Lee"
  - "Ching-Yun Ko"
  - "Pin-Yu Chen"
  - "Mi-Yen Yeh"
url: "http://arxiv.org/abs/2602.04998v2"
published: "2026-02-04"
citations: "0"
source: "arXiv"
id: "arxiv:2602.04998"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning

**Authors**: Yu-Ang Lee, Ching-Yun Ko, Pin-Yu Chen, Mi-Yen Yeh
**Published**: 2026-02-04 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2602.04998v2

## Abstract
Low-Rank Adaptation (LoRA) is the prevailing approach for efficient large language model (LLM) fine-tuning. Building on this paradigm, recent studies have proposed alternative initialization strategies, architectural modifications, and optimization adjustments, reporting substantial improvements over vanilla LoRA. However, these gains are often demonstrated under fixed or narrowly tuned hyperparameter settings, despite the known sensitivity of neural networks to training configurations. In this work, we systematically re-evaluate nine representative LoRA variants alongside vanilla LoRA through extensive hyperparameter searches over learning rate, batch size, rank, and training duration. Across tasks spanning mathematical reasoning, commonsense reasoning, code generation, and instruction following at diverse model scales, we find that different LoRA methods favor distinct learning rate ranges. Crucially, once learning rates are properly tuned, all methods achieve similar peak performance (within 1-2%), with only subtle rank-dependent behaviors. These results suggest that vanilla LoRA remains a competitive baseline and that improvements reported under a single training configuration may not reflect consistent methodological advantages. Finally, a second-order analysis attributes the differing optimal learning rate ranges to variations in the largest Hessian eigenvalue, aligning with classical learning theories.
