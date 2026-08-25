---
title: "Task-Conditioned Routing Signatures in Sparse Mixture-of-Experts Transformers"
authors:
  - "Mynampati Sri Ranganadha Avinash"
url: "http://arxiv.org/abs/2603.11114v1"
published: "2026-03-11"
citations: "0"
source: "arXiv"
id: "arxiv:2603.11114"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Task-Conditioned Routing Signatures in Sparse Mixture-of-Experts Transformers

**Authors**: Mynampati Sri Ranganadha Avinash
**Published**: 2026-03-11 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2603.11114v1

## Abstract
Sparse Mixture-of-Experts (MoE) architectures enable efficient scaling of large language models through conditional computation, yet the routing mechanisms responsible for expert selection remain poorly understood. In this work, we introduce routing signatures, a vector representation summarizing expert activation patterns across layers for a given prompt, and use them to study whether MoE routing exhibits task-conditioned structure. Using OLMoE-1B-7B-0125-Instruct as an empirical testbed, we show that prompts from the same task category induce highly similar routing signatures, while prompts from different categories exhibit substantially lower similarity. Within-category routing similarity (0.8435 +/- 0.0879) significantly exceeds across-category similarity (0.6225 +/- 0.1687), corresponding to Cohen's d = 1.44. A logistic regression classifier trained solely on routing signatures achieves 92.5% +/- 6.1% cross-validated accuracy on four-way task classification. To ensure statistical validity, we introduce permutation and load-balancing baselines and show that the observed separation is not explained by sparsity or balancing constraints alone. We further analyze layer-wise signal strength and low-dimensional projections of routing signatures, finding that task structure becomes increasingly apparent in deeper layers. These results suggest that routing in sparse transformers is not merely a balancing mechanism, but a measurable task-sensitive component of conditional computation. We release MOE-XRAY, a lightweight toolkit for routing telemetry and analysis.
