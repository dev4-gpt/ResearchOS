---
title: "ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling"
authors:
  - "Xin He"
  - "Shunkang Zhang"
  - "Kaijie Tang"
  - "Shaohuai Shi"
  - "Yuxin Wang"
  - "Zihao Zeng"
  - "Zhenheng Tang"
  - "Xiaowen Chu"
  - "Haiyan Yin"
  - "Ivor W. Tsang"
  - "Yew Soon Ong"
url: "http://arxiv.org/abs/2410.17954v2"
published: "2024-10-23"
citations: "0"
source: "arXiv"
id: "arxiv:2410.17954"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling

**Authors**: Xin He, Shunkang Zhang, Kaijie Tang, Shaohuai Shi, Yuxin Wang, Zihao Zeng, Zhenheng Tang, Xiaowen Chu, Haiyan Yin, Ivor W. Tsang, Yew Soon Ong
**Published**: 2024-10-23 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2410.17954v2

## Abstract
Sparse Mixture-of-Experts (MoE) models can outperform dense large language models at similar computation by activating only a small set of experts per token. However, stacking many expert modules introduces substantial parameter memory, which makes MoE models difficult to deploy in memory-constrained environments such as single-GPU devices. Offloading alleviates this issue by storing inactive experts in CPU memory and loading them on demand, but existing methods remain limited: static caches disregard input-dependent routing, and methods that train separate models to predict expert usage ahead of time are often inaccurate or require significant training cost. We propose ExpertFlow, a lightweight MoE inference system that addresses this routing dependency through three coordinated components: 1) a transformer-based routing path predictor that estimates expert usage across all MoE layers in a single forward pass, 2) a token scheduler that groups tokens with similar predicted routes to improve expert utilization, and 3) a predictive expert cache that loads only the required experts while correcting mispredictions at runtime. Together, these components enable efficient expert loading and execution, reducing GPU memory usage by up to 93.72% and improving inference throughput by up to 10x over strong offloading baselines on a single GPU.
