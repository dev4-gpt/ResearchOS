---
title: "AutoMine Solution for AV2 2026 Scenario Mining Challenge"
authors:
  - "Songliang Cao"
  - "Jiele Zhao"
  - "Yuru Wang"
  - "Hao Li"
  - "Daqi Liu"
  - "Zehan Zhang"
  - "Fangzhen Li"
  - "Yu Wang"
  - "Yue Zhang"
  - "Bing Wang"
  - "Guang Chen"
  - "Hao Lu"
  - "Hangjun Ye"
url: "http://arxiv.org/abs/2606.11874v1"
published: "2026-06-10"
citations: "0"
source: "arXiv"
id: "arxiv:2606.11874"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "topic:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target:-cvpr-2026-workshop-on-multimodal-learning-+-arxiv-pre-print"
---
# AutoMine Solution for AV2 2026 Scenario Mining Challenge

**Authors**: Songliang Cao, Jiele Zhao, Yuru Wang, Hao Li, Daqi Liu, Zehan Zhang, Fangzhen Li, Yu Wang, Yue Zhang, Bing Wang, Guang Chen, Hao Lu, Hangjun Ye
**Published**: 2026-06-10 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2606.11874v1

## Executive Summary & Abstract
With the development of autonomous driving systems, mining high-value, safety-critical, and planning-relevant scenarios from large-scale driving logs has become essential for data-driven evaluation. In this paper, we propose AutoMine, a robust self-refining scenario mining method based on LLMs and VLMs. AutoMine uses semantics-preserving prompt augmentation to reduce LLM prompt sensitivity, combines robust trajectory atomic functions with VLM-based functions to handle perception noise and open-world visual cues, and refines generated code through execution feedback from real logs. In the Argoverse 2 Scenario Mining Competition at CVPR 2026, AutoMine achieves a HOTA-Temporal score of 36.38 and a Timestamp BA score of 77.21.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
AutoMine Solution for A V2 2026 Scenario Mining Challenge
Songliang Cao1,2 * Jiele Zhao1 * Yuru Wang1 Hao Li1 Daqi Liu1 Zehan Zhang1†
Fangzhen Li1† Yu Wang Yue Zhang Bing Wang 1 Guang Chen1 Hao Lu2 Hangjun Ye1
1Xiaomi EV 2Huazhong University of Science and Technology
Abstract
With the development of autonomous driving systems, mining high-value, safety-critical, and planning-relevant scenarios from large-scale driving logs has become essential for data-driven evaluation. In this paper, we propose
AutoMine, a robust self-refining scenario mining method
based on LLMs and VLMs. AutoMine uses semanticspreserving prompt augmentation to reduce LLM prompt
sensitivity, combines robust trajectory atomic functions with
VLM-based functions to handle perception noise and openworld visual cues, and refines generated code through execution feedback from real logs. In the Argoverse 2 Scenario
Mining Competition at CVPR 2026, AutoMine achieves a
HOTA-Temporal score of36.38and a Timestamp BA score
of77.21.
1. Introduction
Autonomous driving datasets contain massive sensor logs,
while rare and safety-critical events remain sparse. Scenario mining enables targeted evaluation by retrieving logs,
timestamps, and 3D actors that match a natural language
description.
This task is challenging because query wording is precise, predicted tracks are noisy, and some scenarios require
visual evidence beyond 3D trajectories. For example,passingandovertakingmay imply different conditions, while
tracks may c
