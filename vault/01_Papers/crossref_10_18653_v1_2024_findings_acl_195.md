---
title: "PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference"
authors:
  - "Dongjie Yang"
  - "Xiaodong Han"
  - "Yan Gao"
  - "Yao Hu"
  - "Shilin Zhang"
  - "Hai Zhao"
url: "https://doi.org/10.18653/v1/2024.findings-acl.195"
published: "2024"
citations: "22"
source: "Crossref"
id: "10.18653/v1/2024.findings-acl.195"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference

**Authors**: Dongjie Yang, Xiaodong Han, Yan Gao, Yao Hu, Shilin Zhang, Hai Zhao
**Published**: 2024 | **Source**: Crossref
**URL**: https://doi.org/10.18653/v1/2024.findings-acl.195

## Abstract
Large Language Models (LLMs) have shown remarkable comprehension abilities but face challenges in GPU memory usage during inference, hindering their scalability for realtime applications like chatbots.To accelerate inference, we store computed keys and values (KV cache) in the GPU memory.Existing methods study the KV cache compression to reduce memory by pruning the pre-computed KV cache.However, they neglect the inter-layer dependency between layers and huge memory consumption in pre-computation.To explore these deficiencies, we find that the number of crucial keys and values that influence future generations decreases layer by layer and we can extract them by the consistency in attention weights.Based on the findings, we propose PyramidInfer, a method that compresses the KV cache by layer-wise retaining crucial context.PyramidInfer saves significant memory by computing fewer keys and values without sacrificing performance.Experimental results show PyramidInfer improves 2.2x throughput compared to Accelerate with over 54% GPU memory reduction in KV cache.Our code is available in https://github.com/mutonix/ pyramidinfer.
