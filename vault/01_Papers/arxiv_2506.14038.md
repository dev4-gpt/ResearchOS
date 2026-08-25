---
title: "Load Balancing Mixture of Experts with Similarity Preserving Routers"
authors:
  - "Nabil Omi"
  - "Siddhartha Sen"
  - "Ali Farhadi"
url: "http://arxiv.org/abs/2506.14038v2"
published: "2025-06-16"
citations: "0"
source: "arXiv"
id: "arxiv:2506.14038"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Load Balancing Mixture of Experts with Similarity Preserving Routers

**Authors**: Nabil Omi, Siddhartha Sen, Ali Farhadi
**Published**: 2025-06-16 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2506.14038v2

## Abstract
Sparse Mixture of Experts (MoE) models offer a scalable and efficient architecture for training large neural networks by activating only a subset of parameters ("experts") for each input. A learned router computes a distribution over these experts, and assigns input tokens to a small subset. However, without auxiliary balancing mechanisms, routers often converge to using only a few experts, severely limiting model capacity and degrading performance. Most current load balancing mechanisms encourage a distribution over experts that resembles a roughly uniform distribution of experts per token. During training, this can result in inconsistent routing behavior, resulting in the model spending its capacity to learn redundant knowledge. We address this by introducing a novel load balancing loss that preserves token-wise relational structure, encouraging consistent expert choices for similar inputs during training. Our experimental results show that applying our loss to the router results in 36% faster convergence and lower redundancy compared to a popular load balancing loss.
