---
title: "Mitigating Object and Action Hallucinations in Multimodal LLMs via Self-Augmented Contrastive Alignment"
authors:
  - "Kai-Po Chang"
  - "Wei-Yuan Cheng"
  - "Chi-Pin Huang"
  - "Fu-En Yang"
  - "Yu-Chiang Frank Wang"
url: "http://arxiv.org/abs/2512.04356v1"
published: "2025-12-04"
citations: "1"
source: "arXiv & Crossref"
id: "arxiv:2512.04356"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "title:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target-venues:-cvpr-2026-workshop-/-ieee-tpami-core-research-question:-does-contrastive-alignment-(clip/siglip)-or-autoregressive-generative-alignment-(lmms/chameleon/llama-vision)-provide-superior-out-of-distribution-transferability-and-lower-hallucination-rates?-why-it's-high-impact:-resolves-the-central-architectural-debate-in-modern-multimodal-ai.-corpus-target:-25-papers"
---
# Mitigating Object and Action Hallucinations in Multimodal LLMs via Self-Augmented Contrastive Alignment

**Authors**: Kai-Po Chang, Wei-Yuan Cheng, Chi-Pin Huang, Fu-En Yang, Yu-Chiang Frank Wang
**Published**: 2025-12-04 | **Citations**: 1 | **Source**: arXiv & Crossref
**URL**: http://arxiv.org/abs/2512.04356v1

## Executive Summary & Abstract
Recent advancement in multimodal LLMs (MLLMs) has demonstrated their remarkable capability to generate descriptive captions for input videos. However, these models suffer from factual inaccuracies in the generated descriptions, causing severe hallucination issues. While prior works have explored alleviating hallucinations for static images, jointly mitigating visual object and temporal action hallucinations for dynamic videos remains a challenging and unsolved task. To tackle this challenge, we propose a Self-Augmented Contrastive Alignment (SANTA) framework for enabling object and action faithfulness by exempting the spurious correlations and enforcing the emphasis on visual facts. SANTA employs a hallucinative self-augmentation scheme to identify the potential hallucinations that lie in the MLLM and transform the original captions to the contrasted negatives. Furthermore, we develop a tracklet-phrase contrastive alignment to match the regional objects and relation-guided actions with their corresponding visual and temporal phrases. Extensive experiments demonstrate that SANTA outperforms existing methods in alleviating object and action hallucinations, yielding superior performance on the hallucination examination benchmarks.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Mitigating Object and Action Hallucinations in Multimodal LLMs via
Self-Augmented Contrastive Alignment
Kai-Po Chang1,†, Wei-Yuan Cheng1, Chi-Pin Huang1, Fu-En Yang2, and Yu-Chiang Frank Wang1,2,‡
1 Graduate Institute of Communication Engineering, National Taiwan University
2 NVIDIA
†f11942093@ntu.edu.tw, ‡frankwang@nvidia.com
Abstract
Recent advancement in multimodal LLMs (MLLMs) has
demonstrated their remarkable capability to generate descriptive captions for input videos. However, these models suffer from factual inaccuracies in the generated descriptions, causing severe hallucination issues. While prior
works have explored alleviating hallucinations for static images, jointly mitigating visual object and temporal action
hallucinations for dynamic videos remains a challenging
and unsolved task. To tackle this challenge, we propose
aSelf-Augmented ContrastiveAlignment (SANTA) framework for enabling object and action faithfulness by exempting the spurious correlations and enforcing the emphasis on visual facts. SANTA employs a hallucinative
self-augmentation scheme to identify the potential hallucinations that lie in the MLLM and transform the original
captions to the contrasted negatives. Furthermore, we develop a tracklet-phrase contrastive alignment to match the
regional objects and relation-guided actions with their corresponding visual and temporal phrases. Extensive experiments demonstrate that SANTA outperforms existing methods in alleviating object and action halluci
