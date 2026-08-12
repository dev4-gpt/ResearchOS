---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
authors:
  - "Rafael Rafailov"
  - "Archit Sharma"
  - "Eric Mitchell"
  - "Stefano Ermon"
  - "Christopher D. Manning"
  - "Chelsea Finn"
url: "https://arxiv.org/abs/2305.18290"
published: "2023-05-29"
citations: "1240"
source: "arXiv & OpenAlex"
id: "arxiv:2305.18290"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "multimodal-alignment-in-vision-language-models:-contrastive-vs-generative"
---
# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

**Authors**: Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn
**Published**: 2023-05-29 | **Citations**: 1240 | **Source**: arXiv & OpenAlex
**URL**: https://arxiv.org/abs/2305.18290

## Executive Summary & Abstract
We present Direct Preference Optimization (DPO), a stable, performant, and computationally lightweight algorithm for aligning LLMs to human preferences without training a reward model or using reinforcement learning.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Direct Preference Optimization:
Your Language Model is Secretly a Reward Model
Rafael Rafailov∗ † Archit Sharma∗ † Eric Mitchell∗ †
Stefano Ermon†‡ Christopher D. Manning† Chelsea Finn†
†Stanford University ‡CZ Biohub
{rafailov,architsh,eric.mitchell}@cs.stanford.edu
Abstract
While large-scale unsupervised language models (LMs) learn broad world knowledge and some reasoning skills, achieving precise control of their behavior is
difficult due to the completely unsupervised nature of their training. Existing
methods for gaining such steerability collect human labels of the relative quality of
model generations and fine-tune the unsupervised LM to align with these preferences, often with reinforcement learning from human feedback (RLHF). However,
RLHF is a complex and often unstable procedure, first fitting a reward model that
reflects the human preferences, and then fine-tuning the large unsupervised LM
using reinforcement learning to maximize this estimated reward without drifting
too far from the original model. In this paper we introduce a new parameterization
of the reward model in RLHF that enables extraction of the corresponding optimal
policy in closed form, allowing us to solve the standard RLHF problem with only a
simple classification loss. The resulting algorithm, which we call Direct Preference Optimization (DPO), is stable, performant, and computationally lightweight,
eliminating the need for sampling from the LM during fine-tuning or performing
significant hyperpa
