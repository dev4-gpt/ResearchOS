---
title: "LOOK-M: Look-Once Optimization in KV Cache for Efficient Multimodal Long-Context Inference"
authors:
  - "Zhongwei Wan"
  - "Ziang Wu"
  - "Che Liu"
  - "Jinfa Huang"
  - "Zhihong Zhu"
  - "Peng Jin"
  - "Longyue Wang"
  - "Yuan Li"
url: "https://doi.org/10.18653/v1/2024.findings-emnlp.235"
published: "2024"
citations: "15"
source: "Crossref"
id: "10.18653/v1/2024.findings-emnlp.235"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# LOOK-M: Look-Once Optimization in KV Cache for Efficient Multimodal Long-Context Inference

**Authors**: Zhongwei Wan, Ziang Wu, Che Liu, Jinfa Huang, Zhihong Zhu, Peng Jin, Longyue Wang, Yuan Li
**Published**: 2024 | **Source**: Crossref
**URL**: https://doi.org/10.18653/v1/2024.findings-emnlp.235

## Abstract
Long-context Multimodal Large Language Models (MLLMs) demand substantial computational resources for inference as the growth of their multimodal Key-Value (KV) cache, in response to increasing input lengths, challenges memory and time efficiency.Unlike single-modality LLMs that manage only textual contexts, the KV cache of long-context MLLMs includes representations from multiple images with temporal and spatial relationships and related textual contexts.The predominance of image tokens means traditional optimizations for LLMs' KV caches are unsuitable for multimodal long-context settings, and no prior works have addressed this challenge.In this work, we introduce LOOK-M, a pioneering, fine-tuning-free approach that efficiently reduces the multimodal KV cache size while maintaining performance comparable to a full cache.We observe that during prompt prefilling phase, the model prioritizes more textual attention over image features, and based on the multimodal interaction observation, a new proposed text-prior method is explored to compress the KV cache.Furthermore, to mitigate the degradation of image contextual information, we propose several compensatory strategies using KV pairs merging.LOOK-M demonstrates that with a significant reduction in KV Cache memory usage, such as reducing it by 80% in some cases, it not only achieves up to 1.5x faster decoding but also maintains or even enhances performance across a variety of long context multimodal tasks.
