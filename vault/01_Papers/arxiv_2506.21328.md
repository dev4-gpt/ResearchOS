---
title: "Latent Prototype Routing: Achieving Near-Perfect Load Balancing in Mixture-of-Experts"
authors:
  - "Jiajie Yang"
url: "http://arxiv.org/abs/2506.21328v1"
published: "2025-06-26"
citations: "0"
source: "arXiv"
id: "arxiv:2506.21328"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Latent Prototype Routing: Achieving Near-Perfect Load Balancing in Mixture-of-Experts

**Authors**: Jiajie Yang
**Published**: 2025-06-26 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2506.21328v1

## Abstract
Mixture-of-Experts (MoE) architectures have emerged as a key strategy for scaling large language models (LLMs) efficiently. However, current MoE systems suffer from severe load imbalance, where only a small subset of experts is consistently activated during training and inference, leading to significant underutilization of model capacity and computational resources. In this work, we revisit expert routing through a clustering perspective and propose Latent Prototype Routing (LPR), a novel routing framework that generalizes existing approaches while promoting balanced expert utilization without compromising downstream performance. Extensive experiments across multiple open-source MoE models -- including DeepSeek-V3, Qwen3-MoE, and Mixtral -- demonstrate that LPR reduces the Gini coefficient of expert load from 0.70 to 0.035 on average, improves the min-max expert load ratio from 1e-6 to 0.70, achieving near-perfect load balancing.
