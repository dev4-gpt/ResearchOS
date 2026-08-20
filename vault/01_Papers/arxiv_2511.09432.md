---
title: "Equivariant Sparse Autoencoders: Mechanistic Interpretability of Neural Networks on Symmetric Data"
authors:
  - "Ege Erdogan"
  - "Ana Lucic"
url: "http://arxiv.org/abs/2511.09432v2"
published: "2025-11-12"
citations: "0"
source: "arXiv"
id: "arxiv:2511.09432"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Equivariant Sparse Autoencoders: Mechanistic Interpretability of Neural Networks on Symmetric Data

**Authors**: Ege Erdogan, Ana Lucic
**Published**: 2025-11-12 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2511.09432v2

## Executive Summary & Abstract
Machine learning (ML) models achieve remarkable performance but remain hard to interpret due to their scale and complexity. In particular, their activations entangle many concepts into fewer dimensions, a phenomenon known as superposition. Mechanistic interpretability methods such as sparse autoencoders (SAEs) can disentangle these dense activations into sparse sums of interpretable features, but SAEs suffer from unidentifiability: different explanations can fit the data equally well without necessarily being more interpretable or faithful to the underlying model. We show that this problem is exacerbated by data symmetries such as rotations that are prevalent in scientific domains. We extend the Linear Representation Hypothesis, the theory behind SAEs, to account for symmetries and show on synthetic as well as real-world scientific datasets and models that the resulting Equivariant SAEs can (1) avoid the pitfalls of existing SAEs on symmetric data and (2) discover features more useful for downstream tasks despite worse reconstructions. Our results show that incorporating the correct priors in SAEs can significantly improve their usefulness while highlighting that reconstruction quality can be inversely correlated with feature usefulness under symmetries, cautioning against its use as a key measure of interpretability. Code: https://github.com/ege-erdogan/equivariant-sae

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Equivariant Sparse Autoencoders: Mechanistic Interpretability of Neural Networks
on Symmetric Data
Ege Erdogan∗, Ana Lucic
University of Amsterdam
e.erdogan@uva.nl
Abstract
Machine learning (ML) models achieve remarkable performance but remain hard to interpret due to their scale and complexity. In particular, their activations entangle many concepts
into fewer dimensions, a phenomenon known as superposition.
Mechanistic interpretability methods such assparse autoencoders(SAEs) can disentangle these dense activations into
sparse sums of interpretablefeatures, but SAEs suffer from
unidentifiability: different explanations can fit the data equally
well without necessarily being more interpretable or faithful
to the underlying model. We show that this problem is exacerbated by data symmetries such as rotations that are prevalent
in scientific domains. We extend the Linear Representation
Hypothesis, the theory behind SAEs, to account for symmetries and show on synthetic as well as real-world scientific
datasets and models that the resultingEquivariant SAEscan
(1) avoid the pitfalls of existing SAEs on symmetric data and
(2) discover features more useful for downstream tasks despite
worse reconstructions. Our results show that incorporating
the correct priors in SAEs can significantly improve their usefulness while highlighting that reconstruction quality can be
inversely correlated with feature usefulness under symmetries,
cautioning against its use as a key measure of interpreta
