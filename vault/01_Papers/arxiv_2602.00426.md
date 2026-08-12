---
title: "LLMs as High-Dimensional Nonlinear Autoregressive Models with Attention: Training, Alignment and Inference"
authors:
  - "Vikram Krishnamurthy"
url: "http://arxiv.org/abs/2602.00426v1"
published: "2026-01-31"
citations: "0"
source: "arXiv"
id: "arxiv:2602.00426"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "title:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target-venues:-cvpr-2026-workshop-/-ieee-tpami-core-research-question:-does-contrastive-alignment-(clip/siglip)-or-autoregressive-generative-alignment-(lmms/chameleon/llama-vision)-provide-superior-out-of-distribution-transferability-and-lower-hallucination-rates?-why-it's-high-impact:-resolves-the-central-architectural-debate-in-modern-multimodal-ai.-corpus-target:-25-papers"
---
# LLMs as High-Dimensional Nonlinear Autoregressive Models with Attention: Training, Alignment and Inference

**Authors**: Vikram Krishnamurthy
**Published**: 2026-01-31 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2602.00426v1

## Executive Summary & Abstract
Large language models (LLMs) based on transformer architectures are typically described through collections of architectural components and training procedures, obscuring their underlying computational structure. This review article provides a concise mathematical reference for researchers seeking an explicit, equation-level description of LLM training, alignment, and generation. We formulate LLMs as high-dimensional nonlinear autoregressive models with attention-based dependencies. The framework encompasses pretraining via next-token prediction, alignment methods such as reinforcement learning from human feedback (RLHF), direct preference optimization (DPO), rejection sampling fine-tuning (RSFT), and reinforcement learning from verifiable rewards (RLVR), as well as autoregressive generation during inference. Self-attention emerges naturally as a repeated bilinear--softmax--linear composition, yielding highly expressive sequence models. This formulation enables principled analysis of alignment-induced behaviors (including sycophancy), inference-time phenomena (such as hallucination, in-context learning, chain-of-thought prompting, and retrieval-augmented generation), and extensions like continual learning, while serving as a concise reference for interpretation and further theoretical development.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
LLMs as High-Dimensional Nonlinear Autoregressive Models with
Attention: Training, Alignment and Inference
Vikram Krishnamurthy, ECE, Cornell University, vikramk@cornell.edu
February 3, 2026
Abstract
Large language models (LLMs) based on transformer architectures are typically described through
collections of architectural components and training procedures, obscuring their underlying computational structure. This review article provides a concise mathematical reference for researchers seeking an
explicit, equation-level description of LLM training, alignment, and generation. We formulate LLMs as
high-dimensional nonlinear autoregressive models with attention-based dependencies. The framework encompasses pretraining via next-token prediction, alignment methods such as reinforcement learning from
human feedback (RLHF), direct preference optimization (DPO), rejection sampling fine-tuning (RSFT),
and reinforcement learning from verifiable rewards (RL VR), as well as autoregressive generation during
inference. Self-attention emerges naturally as a repeated bilinear–softmax–linear composition, yielding
highly expressive sequence models. This formulation enables principled analysis of alignment-induced
behaviors (including sycophancy), inference-time phenomena (such as hallucination, in-context learning,
chain-of-thought prompting, and retrieval-augmented generation), and extensions like continual learning,
while serving as a concise reference for interpretation and further theoret
