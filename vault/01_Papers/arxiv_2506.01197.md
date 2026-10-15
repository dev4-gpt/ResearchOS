---
title: "Incorporating Hierarchical Semantics in Sparse Autoencoder Architectures"
authors:
  - "Mark Muchane"
  - "Sean Richardson"
  - "Kiho Park"
  - "Victor Veitch"
url: "http://arxiv.org/abs/2506.01197v1"
published: "2025-06-01"
citations: "0"
source: "arXiv"
id: "arxiv:2506.01197"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Incorporating Hierarchical Semantics in Sparse Autoencoder Architectures

**Authors**: Mark Muchane, Sean Richardson, Kiho Park, Victor Veitch
**Published**: 2025-06-01 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2506.01197v1

## Executive Summary & Abstract
Sparse dictionary learning (and, in particular, sparse autoencoders) attempts to learn a set of human-understandable concepts that can explain variation on an abstract space. A basic limitation of this approach is that it neither exploits nor represents the semantic relationships between the learned concepts. In this paper, we introduce a modified SAE architecture that explicitly models a semantic hierarchy of concepts. Application of this architecture to the internal representations of large language models shows both that semantic hierarchy can be learned, and that doing so improves both reconstruction and interpretability. Additionally, the architecture leads to significant improvements in computational efficiency.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Incorporating Hierarchical Semantics in Sparse
Autoencoder Architectures
Mark Muchane, Sean Richardson, Kiho Park, and Victor Veitch
University of Chicago
Abstract
Sparse dictionary learning (and, in particular, sparse autoencoders) attempts to learn
a set of human-understandable concepts that can explain variation on an abstract space.
A basic limitation of this approach is that it neither exploits nor represents the semantic
relationships between the learned concepts. In this paper, we introduce a modified
SAE architecture that explicitly models a semantic hierarchy of concepts. Application of
this architecture to the internal representations of large language models shows both
that semantic hierarchy can be learned, and that doing so improves both reconstruction
and interpretability. Additionally, the architecture leads to significant improvements
in computational efficiency. Code is available at github.com/muchanem/hierarchicalsparse-autoencoders.
1 Introduction
Dictionary learning—and, in particular, sparse autoencoders (SAEs)—have attracted significant attention as a tool for interpreting representations in large language models [Bri+23;
Cun+23; Gao+24; Lie+24; Lin+25]. The aim of these methods is to jointly learn some set
of human-understandable concepts that can explain the model’s behavior, and a map from
the model’s internal representations to these concepts. Empirically, at least some of the
features learned by SAEs do seem clearly semantically interpretable—for ex
