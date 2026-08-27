---
title: "ProjAgent: Procedural Similarity Retrieval for Repository-Level Code Generation"
authors:
  - "QiHong Chen"
  - "Aaron Imani"
  - "Iftekhar Ahmed"
url: "http://arxiv.org/abs/2607.08691v1"
published: "2026-07-09"
citations: "0"
source: "arXiv"
id: "arxiv:2607.08691"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# ProjAgent: Procedural Similarity Retrieval for Repository-Level Code Generation

**Authors**: QiHong Chen, Aaron Imani, Iftekhar Ahmed
**Published**: 2026-07-09 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2607.08691v1

## Abstract
Repository-level code generation requires implementing target functions while accounting for complex cross-file dependencies and project-specific conventions. Existing retrieval methods predominantly rely on lexical, structural, or semantic similarity, often overlooking repository functions that implement similar procedural logic despite differing in identifiers or application domains. We propose ProjAgent, a repository-level code generation system that introduces procedural similarity as an explicit retrieval signal. ProjAgent decomposes the target function into intermediate reasoning steps and employs an agentic workflow to retrieve repository functions that exhibit similar procedural behavior at each step. The retrieved procedural context is integrated with conventional semantic retrieval to construct a richer repository context for code generation. ProjAgent further incorporates a conservative static-analysis feedback loop that iteratively repairs generated code using compiler and static-analysis feedback. Evaluated on REPOCOD, ProjAgent achieves 41.14% Pass@1, outperforming existing retrieval-based baselines. These results demonstrate that procedural similarity is an effective and previously unexplored retrieval dimension for repository-level code generation.
