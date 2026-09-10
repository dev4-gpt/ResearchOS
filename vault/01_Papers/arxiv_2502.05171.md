---
title: "Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach"
authors:
  - "Jonas Geiping"
  - "Sean McLeish"
  - "Neel Jain"
  - "John Kirchenbauer"
  - "Siddharth Singh"
  - "Brian R. Bartoldson"
  - "Bhavya Kailkhura"
  - "Abhinav Bhatele"
  - "Tom Goldstein"
url: "http://arxiv.org/abs/2502.05171v2"
published: "2025-02-07"
citations: "2"
source: "arXiv & Crossref"
id: "arxiv:2502.05171"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "test-time-compute-reasoning"
---
# Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach

**Authors**: Jonas Geiping, Sean McLeish, Neel Jain, John Kirchenbauer, Siddharth Singh, Brian R. Bartoldson, Bhavya Kailkhura, Abhinav Bhatele, Tom Goldstein
**Published**: 2025-02-07 | **Citations**: 2 | **Source**: arXiv & Crossref
**URL**: http://arxiv.org/abs/2502.05171v2

## Executive Summary & Abstract
We study a novel language model architecture that is capable of scaling test-time computation by implicitly reasoning in latent space. Our model works by iterating a recurrent block, thereby unrolling to arbitrary depth at test-time. This stands in contrast to mainstream reasoning models that scale up compute by producing more tokens. Unlike approaches based on chain-of-thought, our approach does not require any specialized training data, can work with small context windows, and can capture types of reasoning that are not easily represented in words. We scale a proof-of-concept model to 3.5 billion parameters and 800 billion tokens. We show that the resulting model can improve its performance on reasoning benchmarks, sometimes dramatically, up to a computation load equivalent to 50 billion parameters.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Scaling up Test-Time Compute with Latent Reasoning:
A Recurrent Depth Approach
Jonas Geiping 1 Sean McLeish 2 Neel Jain 2 John Kirchenbauer 2 Siddharth Singh 2 Brian R. Bartoldson 3
Bhavya Kailkhura 3 Abhinav Bhatele 2 Tom Goldstein2
Abstract
We study a novel language model architecture
that is capable of scaling test-time computation by
implicitly reasoning in latent space. Our model
works by iterating a recurrent block, thereby unrolling to arbitrary depth at test-time. This stands
in contrast to mainstream reasoning models that
scale up compute by producing more tokens. Unlike approaches based on chain-of-thought, our
approach does not require any specialized training data, can work with small context windows,
and can capture types of reasoning that are not
easily represented in words. We scale a proof-ofconcept model to 3.5 billion parameters and 800
billion tokens. We show that the resulting model
can improve its performance on reasoning benchmarks, sometimes dramatically, up to a computation load equivalent to 50 billion parameters.
Model: huggingface.co/tomg-group-umd/huginn0125
Code and Data: github.com/seal-rg/recurrentpretraining
1. Scaling by Thinking in Continuous Space
Humans naturally expend more mental effort solving some
problems than others. While humans are capable of thinking over long time spans by verbalizing intermediate results
and writing them down, a substantial amount of thought
happens through complex, recurrent firing patterns in the
brain, before 
