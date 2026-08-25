---
title: "One-for-All: Generalized LoRA for Parameter-Efficient Fine-tuning"
authors:
  - "Arnav Chavan"
  - "Zhuang Liu"
  - "Deepak Gupta"
  - "Eric Xing"
  - "Zhiqiang Shen"
url: "http://arxiv.org/abs/2306.07967v2"
published: "2023-06-13"
citations: "0"
source: "arXiv"
id: "arxiv:2306.07967"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# One-for-All: Generalized LoRA for Parameter-Efficient Fine-tuning

**Authors**: Arnav Chavan, Zhuang Liu, Deepak Gupta, Eric Xing, Zhiqiang Shen
**Published**: 2023-06-13 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2306.07967v2

## Abstract
We present Generalized LoRA (GLoRA), an advanced approach for universal parameter-efficient fine-tuning tasks. Enhancing Low-Rank Adaptation (LoRA), GLoRA employs a generalized prompt module to optimize pre-trained model weights and adjust intermediate activations, providing more flexibility and capability across diverse tasks and datasets. Moreover, GLoRA facilitates efficient parameter adaptation by employing a scalable, modular, layer-wise structure search that learns individual adapter of each layer. Originating from a unified mathematical formulation, GLoRA exhibits strong transfer learning, few-shot learning and domain generalization abilities, as it adapts to new tasks through not only weights but also additional dimensions like activations. Comprehensive experiments demonstrate that GLoRA outperforms all previous methods in natural, specialized, and structured vision benchmarks, achieving superior accuracy with fewer parameters and computations. The proposed method on LLaMA-1 and LLaMA-2 also show considerable enhancements compared to the original LoRA in the language domain. Furthermore, our structural re-parameterization design ensures that GLoRA incurs no extra inference cost, rendering it a practical solution for resource-limited applications. Code and models are available at: https://github.com/Arnav0400/ViT-Slim/tree/master/GLoRA.
