---
title: "Near-Oracle KV Selection via Pre-hoc Sparsity for Long-Context Inference"
authors:
  - "Yifei Gao"
  - "Lei Wang"
  - "Rong-Cheng Tu"
  - "Qixin Zhang"
  - "Jun Cheng"
  - "Dacheng Tao"
url: "http://arxiv.org/abs/2602.08329v1"
published: "2026-02-09"
citations: "0"
source: "arXiv"
id: "arxiv:2602.08329"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Near-Oracle KV Selection via Pre-hoc Sparsity for Long-Context Inference

**Authors**: Yifei Gao, Lei Wang, Rong-Cheng Tu, Qixin Zhang, Jun Cheng, Dacheng Tao
**Published**: 2026-02-09 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2602.08329v1

## Abstract
A core bottleneck in large language model (LLM) inference is the cost of attending over the ever-growing key-value (KV) cache. Although near-oracle top-k KV selection can preserve the quality of dense attention while sharply reducing computation and bandwidth, existing sparse methods generally rely on posterior heuristics, i.e., selectors conditioned on observed attention or proxy scores. Such conditioning introduces posterior bias: it tends to distort true token importance and miss salient tokens, thereby impairing long-range reasoning. To tackle this problem, we propose Pre-hoc Sparsity (PrHS), which selects KV entries before attention scoring and provides explicit accuracy control. Let the attention mass of discarded entries be delta (the dropped mass). Through a marginal-to-mutual-information analysis, we derive an upper bound on the mutual-information loss that depends only on the dropped mass. This relation explains failure modes of posterior heuristics and enables verifiable guarantees by controlling the dropped mass in advance. Within PrHS, we instantiate three orthogonal pre-hoc selectors along the axes of time, depth, and layer. Extensive experiments on LLaMA and Mistral families validate PrHS. Across GSM8K and CoQA, PrHS reduces retrieval overhead by over 90%, achieving 3x higher retrieval sparsity than HShare at matched or better accuracy. It incurs under 1% average degradation on LongBench, lowers attention FLOPs by about 15% versus prior sparse baselines, and yields a 9.9x speedup in attention-operator latency and 2.8x higher throughput on NVIDIA A100-80GB GPUs than the dense baseline.
