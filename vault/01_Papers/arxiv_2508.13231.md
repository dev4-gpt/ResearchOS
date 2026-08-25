---
title: "Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System"
authors:
  - "Yunhua Fang"
  - "Rui Xie"
  - "Asad Ul Haq"
  - "Linsen Ma"
  - "Kaoutar El Maghraoui"
  - "Naigang Wang"
  - "Meng Wang"
  - "Liu Liu"
  - "Tong Zhang"
url: "http://arxiv.org/abs/2508.13231v2"
published: "2025-08-17"
citations: "0"
source: "arXiv"
id: "arxiv:2508.13231"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System

**Authors**: Yunhua Fang, Rui Xie, Asad Ul Haq, Linsen Ma, Kaoutar El Maghraoui, Naigang Wang, Meng Wang, Liu Liu, Tong Zhang
**Published**: 2025-08-17 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2508.13231v2

## Abstract
Large Language Model (LLM) inference is increasingly constrained by memory bandwidth, with frequent access to the key-value (KV) cache dominating data movement. While attention sparsity reduces some memory traffic, the relevance of past tokens varies over time, requiring the full KV cache to remain accessible and sustaining pressure on both bandwidth and capacity. With advances in interconnects such as NVLink and LPDDR5X, modern AI hardware now integrates high-bandwidth memory (HBM) with high-speed off-package DRAM, making heterogeneous memory systems a practical solution. This work investigates dynamic KV cache placement across such systems to maximize aggregated bandwidth utilization under capacity constraints. Rather than proposing a specific scheduling policy, we formulate the placement problem mathematically and derive a theoretical upper bound, revealing substantial headroom for runtime optimization. To our knowledge, this is the first formal treatment of dynamic KV cache scheduling in heterogeneous memory systems for LLM inference.
