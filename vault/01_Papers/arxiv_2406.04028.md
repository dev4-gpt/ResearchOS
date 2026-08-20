---
title: "Contrastive Sparse Autoencoders for Interpreting Planning of Chess-Playing Agents"
authors:
  - "Yoann Poupart"
url: "http://arxiv.org/abs/2406.04028v1"
published: "2024-06-06"
citations: "0"
source: "arXiv & HAL"
id: "arxiv:2406.04028"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Contrastive Sparse Autoencoders for Interpreting Planning of Chess-Playing Agents

**Authors**: Yoann Poupart
**Published**: 2024-06-06 | **Citations**: 0 | **Source**: arXiv & HAL
**URL**: http://arxiv.org/abs/2406.04028v1

## Executive Summary & Abstract
AI led chess systems to a superhuman level, yet these systems heavily rely on black-box algorithms. This is unsustainable in ensuring transparency to the end-user, particularly when these systems are responsible for sensitive decision-making. Recent interpretability work has shown that the inner representations of Deep Neural Networks (DNNs) were fathomable and contained human-understandable concepts. Yet, these methods are seldom contextualised and are often based on a single hidden state, which makes them unable to interpret multi-step reasoning, e.g. planning. In this respect, we propose contrastive sparse autoencoders (CSAE), a novel framework for studying pairs of game trajectories. Using CSAE, we are able to extract and interpret concepts that are meaningful to the chess-agent plans. We primarily focused on a qualitative analysis of the CSAE features before proposing an automated feature taxonomy. Furthermore, to evaluate the quality of our trained CSAE, we devise sanity checks to wave spurious correlations in our results.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Contrastive Sparse Autoencoders for Interpreting
Planning of Chess-Playing Agents
Yoann Poupart
yoann.poupart@ens-lyon.org
ENS de Lyon
Abstract
AI led chess systems to a superhuman level, yet these systems heavily rely on blackbox algorithms. This is unsustainable in ensuring transparency to the end-user,
particularly when these systems are responsible for sensitive decision-making. Recent interpretability work has shown that the inner representations of Deep Neural
Networks (DNNs) were fathomable and contained human-understandable concepts.
Yet, these methods are seldom contextualised and are often based on a single hidden
state, which makes them unable to interpret multi-step reasoning, e.g. planning.
In this respect, we propose contrastive sparse autoencoders (CSAE), a novel framework for studying pairs of game trajectories. Using CSAE, we are able to extract
and interpret concepts that are meaningful to the chess-agent plans. We primarily
focused on a qualitative analysis of the CSAE features before proposing an automated feature taxonomy. Furthermore, to evaluate the quality of our trained CSAE,
we devise sanity checks to wave spurious correlations in our results.
1 Introduction
Chess is one of the very first domains where superhuman AI shined, first with DeepBlue (Campbell
et al., 2002) and more recently with Stockfish (Nasu, 2018) and AlphaZero (Silver et al., 2018). While
the design of these superhuman programs is intended to gain performances, e.g. by optimising the

