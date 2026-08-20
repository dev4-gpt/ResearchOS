---
title: "Rethinking Fine-Tuning when Scaling Test-Time Compute: Limiting Confidence Improves Mathematical Reasoning"
authors:
  - "Feng Chen"
  - "Allan Raventos"
  - "Nan Cheng"
  - "Surya Ganguli"
  - "Shaul Druckmann"
url: "http://arxiv.org/abs/2502.07154v4"
published: "2025-02-11"
citations: "0"
source: "arXiv & Crossref"
id: "arxiv:2502.07154"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "test-time-compute-reasoning"
---
# Rethinking Fine-Tuning when Scaling Test-Time Compute: Limiting Confidence Improves Mathematical Reasoning

**Authors**: Feng Chen, Allan Raventos, Nan Cheng, Surya Ganguli, Shaul Druckmann
**Published**: 2025-02-11 | **Citations**: 0 | **Source**: arXiv & Crossref
**URL**: http://arxiv.org/abs/2502.07154v4

## Executive Summary & Abstract
Recent progress in large language models (LLMs) highlights the power of scaling test-time compute to achieve strong performance on complex tasks, such as mathematical reasoning and code generation. This raises a critical question: how should model training be modified to optimize performance under a subsequent test-time compute strategy and budget? To explore this, we focus on pass@N, a simple test-time strategy that searches for a correct answer in $N$ independent samples. We show, surprisingly, that training with cross-entropy (CE) loss can be ${\it misaligned}$ with pass@N in that pass@N accuracy ${\it decreases}$ with longer training. We explain the origins of this misalignment in terms of model overconfidence induced by CE, and experimentally verify our prediction of overconfidence as an impediment to scaling test-time compute via pass@N. Furthermore we suggest a principled, modified training loss that is better aligned to pass@N by limiting model confidence and rescuing pass@N test performance. Our algorithm demonstrates improved mathematical reasoning on MATH and MiniF2F benchmarks under several scenarios: (1) providing answers to math questions; and (2) proving theorems by searching over proof trees of varying shapes. Overall our work underscores the importance of co-designing two traditionally separate phases of LLM development: training-time protocols and test-time search and reasoning strategies.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Rethinking Fine-Tuning when Scaling Test-Time
Compute: Limiting Confidence Improves
Mathematical Reasoning
Feng Chen∗
Stanford University
Stanford, CA 94305
fengc@stanford.edu
Allan Raventós*
Stanford University
Stanford, CA 94305
aravento@stanford.edu
Nan Cheng
University of Michigan
Ann Arbor, MI 48109
nancheng@umich.edu
Surya Ganguli
Stanford University
Stanford, CA 94305
sganguli@stanford.edu
Shaul Druckmann
Stanford University
Stanford, CA 94305
shauld@stanford.edu
Abstract
Recent progress in large language models (LLMs) highlights the power of scaling
test-time compute to achieve strong performance on complex tasks, such as mathematical reasoning and code generation. This raises a critical question: how should
model training be modified to optimize performance under a subsequent test-time
compute strategy and budget? To explore this, we focus on pass@N, a simple
test-time strategy that searches for a correct answer in N independent samples. We
show, surprisingly, that training with cross-entropy (CE) loss can bemisaligned
with pass@N in that pass@N accuracydecreaseswith longer training. We explain
the origins of this misalignment in terms of model overconfidence induced by CE,
and experimentally verify our prediction of overconfidence as an impediment to
scaling test-time compute via pass@N. Furthermore we suggest a principled, modified training loss that is better aligned to pass@N by limiting model confidence and
rescuing pass@N test performance. Our algorithm demonst
