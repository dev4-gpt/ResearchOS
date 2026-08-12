---
title: "MOSAIC: A Multimodal Semantic-Oriented Alignment with Integrated Contrastive Learning for Multimodal Knowledge Graph Construction from Scientific Documents"
authors:
  - "Busisani Mac Dube"
  - "Jean Vincent Fonou Dombeu"
url: "https://doi.org/10.20944/preprints202608.0185.v1"
published: "2026-8-7"
citations: "0"
source: "Crossref"
id: "crossref:10.20944/preprints202608.0185.v1"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - ""multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target:-cvpr-2026-workshop-on-multimodal-learning-+-arxiv-pre-print"
---
# MOSAIC: A Multimodal Semantic-Oriented Alignment with Integrated Contrastive Learning for Multimodal Knowledge Graph Construction from Scientific Documents

**Authors**: Busisani Mac Dube, Jean Vincent Fonou Dombeu
**Published**: 2026-8-7 | **Citations**: 0 | **Source**: Crossref
**URL**: https://doi.org/10.20944/preprints202608.0185.v1

## Executive Summary & Abstract
Multimodal Knowledge Graphs (MMKGs) offer a promising paradigm for integrating heterogeneous sources into a unified, queryable, semantically structured representation. However, existing MMKG construction pipelines remain predominantly text-centric, extracting information from textual passages while leaving much of the visual and structural knowledge in scientific papers unrepresented. This produces fragmented graphs with disconnected components, isolated singleton nodes, and weak cross-modal connectivity, reducing the effectiveness of retrieval-augmented generation (RAG) systems that rely on interconnected graph traversal for multi-hop reasoning and evidence aggregation. We propose Multimodal Semantic-Oriented Alignment with Integrated Contrastive Learning (MOSAIC), an end-to-end framework for constructing semantically coherent MMKGs from heterogeneous scientific documents. MOSAIC introduces four complementary contributions: (i) adaptive clustering via HDBSCAN, which infers data-driven entity boundaries without the brittle ε hyperparameters of conventional DBSCAN; (ii) a confidence-aware cross-modal alignment mechanism applying cosine-similarity gating to selectively invoke Large Language Models (LLMs), reducing spurious alignments and computational overhead; (iii) post-fusion semantic bridging, which links semantically related but structurally disconnected components through cosine-similarity-weighted bridge edges; and (iv) self-supervised contrastive embedding fine-tuning using an InfoNCE-style MultipleNegativesRankingLoss objective to specialize the embedding space for cross-modal entity representations. Empirical evaluation shows MOSAIC substantially improves graph topology and structural coherence, achieving a 110% increase in average clustering coefficient, reducing fragmentation, and strengthening intra-cluster semantic consistency. Large-scale evaluation across two challenging benchmarks, MMLongBench-Doc (134 documents) and DocBench (166 documents), consistently demonstrates that the MOSAIC-RAG engine outperforms or enhances competitive retrieval and graph-based baselines across diverse document categories, establishing the framework’s effectiveness and generalizability.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Multimodal Knowledge Graphs (MMKGs) offer a promising paradigm for integrating heterogeneous sources into a unified, queryable, semantically structured representation. However, existing MMKG construction pipelines remain predominantly text-centric, extracting information from textual passages while leaving much of the visual and structural knowledge in scientific papers unrepresented. This produces fragmented graphs with disconnected components, isolated singleton nodes, and weak cross-modal connectivity, reducing the effectiveness of retrieval-augmented generation (RAG) systems that rely on interconnected graph traversal for multi-hop reasoning and evidence aggregation. We propose Multimodal Semantic-Oriented Alignment with Integrated Contrastive Learning (MOSAIC), an end-to-end framework for constructing semantically coherent MMKGs from heterogeneous scientific documents. MOSAIC introduces four complementary contributions: (i) adaptive clustering via HDBSCAN, which infers data-driven entity boundaries without the brittle ε hyperparameters of conventional DBSCAN; (ii) a confidence-aware cross-modal alignment mechanism applying cosine-similarity gating to selectively invoke Large Language Models (LLMs), reducing spurious alignments and computational overhead; (iii) post-fusion semantic bridging, which links semantically related but structurally disconnected components through cosine-similarity-weighted bridge edges; and (iv) self-supervised contrastive embedding fine-tuning u
