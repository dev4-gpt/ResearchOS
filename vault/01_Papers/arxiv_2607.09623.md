---
title: "Task-Specific Multimodal Question Answering Agents via Confidence Calibration and Incremental Reasoning for QANTA 2026"
authors:
  - "Nirjhar Das"
  - "Md. Al-Mamun Provath"
url: "http://arxiv.org/abs/2607.09623v1"
published: "2026-07-10"
citations: "0"
source: "arXiv"
id: "arxiv:2607.09623"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "topic:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target:-cvpr-2026-workshop-on-multimodal-learning-+-arxiv-pre-print"
---
# Task-Specific Multimodal Question Answering Agents via Confidence Calibration and Incremental Reasoning for QANTA 2026

**Authors**: Nirjhar Das, Md. Al-Mamun Provath
**Published**: 2026-07-10 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2607.09623v1

## Executive Summary & Abstract
We present our submission to the QANTA 2026 shared challenge at the ICML 2026 Workshop on Efficient Multimodal Question Answering (EMM-QA). Quanta evaluates multimodal quizbowl systems that answer pyramid-style questions from incrementally revealed text and accompanying images while operating under realistic efficiency constraints. The challenge consists of two distinct tasks: Tossup questions, which require deciding when to answer under uncertainty, and Bonus questions, which emphasize accurate answer selection and human adoption. To address these differing objectives, we develop a task-specific two-agent architecture. Our Tossup agent utilizes a GPT-4o-mini-class model (referred to as GPT-4.1-mini in the competition logs) with confidence-calibrated answering and a domain-specific numeric reasoning policy that reduces overconfident predictions from isolated quantitative clues. Our Bonus agent uses GPT-4o-class model (referred to as GPT-4.1) with leadin-aware reasoning, structured relational reasoning, and multimodal evidence integration to improve exact answer selection. Rather than relying on a retrieval pipeline or model ensembles, our approach emphasizes efficient reasoning policies and confidence calibration within a hosted-only environment. Our system achieved the highest overall leaderboard score of 0.402, including a Tossup score of 0.238 and a Bonus Effect score of 0.164. The results demonstrate that lightweight, task-specific reasoning strategies can provide strong performance on resource-constrained multimodal question answering benchmarks.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Task-Specific Multimodal Question Answering Agents via Confidence
Calibration and Incremental Reasoning for QANTA 2026
Nirjhar Das 1 Md. Al-Mamun Provath 1
Abstract
We present our submission to the QANTA 2026
shared challenge at the ICML 2026 Workshop on
Efficient Multimodal Question Answering (EMMQA). Quanta evaluates multimodal quizbowl systems that answer pyramid-style questions from
incrementally revealed text and accompanying
images while operating under realistic efficiency
constraints. The challenge consists of two distinct tasks: Tossup questions, which require deciding when to answer under uncertainty, and Bonus
questions, which emphasize accurate answer selection and human adoption. To address these
differing objectives, we develop a task-specific
two-agent architecture. Our Tossup agent utilizes
a GPT-4o-mini-class model (referred to as GPT4.1-mini in the competition logs) with confidencecalibrated answering and a domain-specific numeric reasoning policy that reduces overconfident
predictions from isolated quantitative clues. Our
Bonus agent uses GPT-4o-class model (referred
to as GPT-4.1) with leadin-aware reasoning, structured relational reasoning, and multimodal evidence integration to improve exact answer selection. Rather than relying on a retrieval pipeline
or model ensembles, our approach emphasizes
efficient reasoning policies and confidence calibration within a hosted-only environment. Our
system achieved the highest overall leaderboard
score of 0.402, inc
