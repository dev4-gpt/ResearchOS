---
title: "LLMs Know What to Drop: Self-Attention Guided KV Cache Eviction for Efficient Long-Context Inference"
authors:
  - "Guangtao Wang"
  - "Shubhangi Upasani"
  - "Chen Wu"
  - "Darshan Gandhi"
  - "Jonathan Li"
  - "Changran Hu"
  - "Bo Li"
  - "Urmish Thakker"
url: "http://arxiv.org/abs/2503.08879v1"
published: "2025-03-11"
citations: "0"
source: "arXiv"
id: "arxiv:2503.08879"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# LLMs Know What to Drop: Self-Attention Guided KV Cache Eviction for Efficient Long-Context Inference

**Authors**: Guangtao Wang, Shubhangi Upasani, Chen Wu, Darshan Gandhi, Jonathan Li, Changran Hu, Bo Li, Urmish Thakker
**Published**: 2025-03-11 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2503.08879v1

## Abstract
Efficient long-context inference is critical as large language models (LLMs) adopt context windows of ranging from 128K to 1M tokens. However, the growing key-value (KV) cache and the high computational complexity of attention create significant bottlenecks in memory usage and latency. In this paper, we find that attention in diverse long-context tasks exhibits sparsity, and LLMs implicitly "know" which tokens can be dropped or evicted at the head level after the pre-filling stage. Based on this insight, we propose Self-Attention Guided Eviction~(SAGE-KV), a simple and effective KV eviction cache method for long-context inference. After prefilling, our method performs a one-time top-k selection at both the token and head levels to compress the KV cache, enabling efficient inference with the reduced cache. Evaluations on LongBench and three long-context LLMs (Llama3.1-8B-Instruct-128k, Llama3-8B-Prolong-512k-Instruct, and Qwen2.5-7B-Instruct-128k) show that SAGE-KV maintains accuracy comparable to full attention while significantly improving efficiency. Specifically, SAGE-KV achieves 4x higher memory efficiency with improved accuracy over the static KV cache selection method StreamLLM, and 2x higher memory efficiency with better accuracy than the dynamic KV cache selection method Quest.
