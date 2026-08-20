---
title: "Sleep-time Compute: Beyond Inference Scaling at Test-time"
authors:
  - "Kevin Lin"
  - "Charlie Snell"
  - "Yu Wang"
  - "Charles Packer"
  - "Sarah Wooders"
  - "Ion Stoica"
  - "Joseph E. Gonzalez"
url: "http://arxiv.org/abs/2504.13171v1"
published: "2025-04-17"
citations: "0"
source: "arXiv"
id: "arxiv:2504.13171"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "test-time-compute-reasoning"
---
# Sleep-time Compute: Beyond Inference Scaling at Test-time

**Authors**: Kevin Lin, Charlie Snell, Yu Wang, Charles Packer, Sarah Wooders, Ion Stoica, Joseph E. Gonzalez
**Published**: 2025-04-17 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2504.13171v1

## Executive Summary & Abstract
Scaling test-time compute has emerged as a key ingredient for enabling large language models (LLMs) to solve difficult problems, but comes with high latency and inference cost. We introduce sleep-time compute, which allows models to "think" offline about contexts before queries are presented: by anticipating what queries users might ask and pre-computing useful quantities, we can significantly reduce the compute requirements at test-time. To demonstrate the efficacy of our method, we create modified versions of two reasoning tasks - Stateful GSM-Symbolic and Stateful AIME. We find that sleep-time compute can reduce the amount of test-time compute needed to achieve the same accuracy by ~ 5x on Stateful GSM-Symbolic and Stateful AIME and that by scaling sleep-time compute we can further increase accuracy by up to 13% on Stateful GSM-Symbolic and 18% on Stateful AIME. Furthermore, we introduce Multi-Query GSM-Symbolic, which extends GSM-Symbolic by including multiple related queries per context. By amortizing sleep-time compute across related queries about the same context using Multi-Query GSM-Symbolic, we can decrease the average cost per query by 2.5x. We then conduct additional analysis to understand when sleep-time compute is most effective, finding the predictability of the user query to be well correlated with the efficacy of sleep-time compute. Finally, we conduct a case-study of applying sleep-time compute to a realistic agentic SWE task.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Sleep-time Compute: Beyond Inference Scaling at Test-time
Kevin Lin 1∗ Charlie Snell 2∗
Yu Wang 1 Charles Packer 1 Sarah Wooders 1 Ion Stoica 1 2 Joseph E. Gonzalez 1 2
1Letta 2University of California, Berkeley
research@letta.com
Abstract
Scaling test-time compute has emerged as a key ingredient for enabling large language models (LLMs) to
solve difficult problems, but comes with high latency and inference cost. We introduce sleep-time compute,
which allows models to “think” offline about contexts before queries are presented: by anticipating what
queries users might ask and pre-computing useful quantities, we can significantly reduce the compute
requirements at test-time. To demonstrate the efficacy of our method, we create modified versions of two
reasoning tasks – Stateful GSM-Symbolic and Stateful AIME. We find that sleep-time compute can reduce
the amount of test-time compute needed to achieve the same accuracy by ∼ 5× on Stateful GSM-Symbolic
and Stateful AIME and that by scaling sleep-time compute we can further increase accuracy by up to 13% on
Stateful GSM-Symbolic and 18% on Stateful AIME. Furthermore, we introduce Multi-Query GSM-Symbolic,
which extends GSM-Symbolic by including multiple related queries per context. By amortizing sleep-time
compute across related queries about the same context using Multi-Query GSM-Symbolic, we can decrease
the average cost per query by 2.5×. We then conduct additional analysis to understand when sleep-time
compute is most effecti
