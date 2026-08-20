---
title: "Reward Model Generalization for Compute-Aware Test-Time Reasoning"
authors:
  - "Zeen Song"
  - "Wenwen Qiang"
  - "Siyu Zhao"
  - "Changwen Zheng"
  - "Gang Hua"
url: "http://arxiv.org/abs/2505.18065v1"
published: "2025-05-23"
citations: "0"
source: "arXiv"
id: "arxiv:2505.18065"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "test-time-compute-reasoning"
---
# Reward Model Generalization for Compute-Aware Test-Time Reasoning

**Authors**: Zeen Song, Wenwen Qiang, Siyu Zhao, Changwen Zheng, Gang Hua
**Published**: 2025-05-23 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2505.18065v1

## Executive Summary & Abstract
External test-time reasoning enhances large language models (LLMs) by decoupling generation and selection. At inference time, the model generates multiple reasoning paths, and an auxiliary process reward model (PRM) is used to score and select the best one. A central challenge in this setting is test-time compute optimality (TCO), i.e., how to maximize answer accuracy under a fixed inference budget. In this work, we establish a theoretical framework to analyze how the generalization error of the PRM affects compute efficiency and reasoning performance. Leveraging PAC-Bayes theory, we derive generalization bounds and show that a lower generalization error of PRM leads to fewer samples required to find correct answers. Motivated by this analysis, we propose Compute-Aware Tree Search (CATS), an actor-critic framework that dynamically controls search behavior. The actor outputs sampling hyperparameters based on reward distributions and sparsity statistics, while the critic estimates their utility to guide budget allocation. Experiments on the MATH and AIME benchmarks with various LLMs and PRMs demonstrate that CATS consistently outperforms other external TTS methods, validating our theoretical predictions.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Reward Model Generalization for Compute-Aware
Test-Time Reasoning
Zeen Song
Institute of Software,
China Academy of Sciences
University of Chinese Academy of Science
Wenwen Qiang
Institute of Software,
China Academy of Sciences
Siyu Zhao
University of Chinese Academy of Science
Changwen Zheng
Institute of Software,
China Academy of Sciences
Gang Hua
Multimodal Experiences Lab,
Dolby Laboratories Inc
Institute of Artificial Intelligence and Robotics,
Xi’an Jiaotong University
Abstract
External test-time reasoning enhances large language models (LLMs) by decoupling generation and selection. At inference time, the model generates multiple
reasoning paths, and an auxiliary process reward model (PRM) is used to score
and select the best one. A central challenge in this setting is test-time compute
optimality (TCO), i.e., how to maximize answer accuracy under a fixed inference
budget. In this work, we establish a theoretical framework to analyze how the
generalization error of the PRM affects compute efficiency and reasoning performance. Leveraging PAC-Bayes theory, we derive generalization bounds and
show that a lower generalization error of PRM leads to fewer samples required
to find correct answers. Motivated by this analysis, we propose Compute-Aware
Tree Search (CATS), an actor-critic framework that dynamically controls search
behavior. The actor outputs sampling hyperparameters based on reward distributions and sparsity statistics, while the critic estimates their utility to 
