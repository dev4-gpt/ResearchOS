---
title: "Towards Thinking-Optimal Scaling of Test-Time Compute for LLM Reasoning"
authors:
  - "Wenkai Yang"
  - "Shuming Ma"
  - "Yankai Lin"
  - "Furu Wei"
url: "http://arxiv.org/abs/2502.18080v2"
published: "2025-02-25"
citations: "0"
source: "arXiv & Crossref"
id: "arxiv:2502.18080"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "test-time-compute-reasoning"
---
# Towards Thinking-Optimal Scaling of Test-Time Compute for LLM Reasoning

**Authors**: Wenkai Yang, Shuming Ma, Yankai Lin, Furu Wei
**Published**: 2025-02-25 | **Citations**: 0 | **Source**: arXiv & Crossref
**URL**: http://arxiv.org/abs/2502.18080v2

## Executive Summary & Abstract
Recent studies have shown that making a model spend more time thinking through longer Chain of Thoughts (CoTs) enables it to gain significant improvements in complex reasoning tasks. While current researches continue to explore the benefits of increasing test-time compute by extending the CoT lengths of Large Language Models (LLMs), we are concerned about a potential issue hidden behind the current pursuit of test-time scaling: Would excessively scaling the CoT length actually bring adverse effects to a model's reasoning performance? Our explorations on mathematical reasoning tasks reveal an unexpected finding that scaling with longer CoTs can indeed impair the reasoning performance of LLMs in certain domains. Moreover, we discover that there exists an optimal scaled length distribution that differs across different domains. Based on these insights, we propose a Thinking-Optimal Scaling strategy. Our method first uses a small set of seed data with varying response length distributions to teach the model to adopt different reasoning efforts for deep thinking. Then, the model selects its shortest correct response under different reasoning efforts on additional problems for self-improvement. Our self-improved models built upon Qwen2.5-32B-Instruct outperform other distillation-based 32B o1-like models across various math benchmarks, and achieve performance on par with the teacher model QwQ-32B-Preview that produces the seed data.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Towards Thinking-Optimal Scaling of Test-Time
Compute for LLM Reasoning
Wenkai Yang1∗ , Shuming Ma2, Yankai Lin1† , Furu Wei2
1Gaoling School of Artificial Intelligence, Renmin University of China
2Microsoft Research
{wenkaiyang, yankailin}@ruc.edu.cn
{shuming.ma, fuwei}@microsoft.com
Abstract
Recent studies have shown that making a model spend more time thinking through
longer Chain of Thoughts (CoTs) enables it to gain significant improvements in
complex reasoning tasks. While current researches continue to explore the benefits
of increasing test-time compute by extending the CoT lengths of Large Language
Models (LLMs), we are concerned about a potential issue hidden behind the current
pursuit of test-time scaling:Would excessively scaling the CoT length actually
bring adverse effects to a model’s reasoning performance?Our explorations on
mathematical reasoning tasks reveal an unexpected finding that scaling with longer
CoTs can indeed impair the reasoning performance of LLMs in certain domains.
Moreover, we discover that there exists an optimal scaled length distribution that
differs across different domains. Based on these insights, we propose a ThinkingOptimal Scaling strategy. Our method first uses a small set of seed data with
varying response length distributions to teach the model to adopt different reasoning
efforts for deep thinking. Then, the model selects its shortest correct response
under different reasoning efforts on additional problems for self-improvement.

