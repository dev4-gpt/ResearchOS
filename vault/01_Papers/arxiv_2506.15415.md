---
title: "Targeted Lexical Injection: Unlocking Latent Cross-Lingual Alignment in Lugha-Llama via Early-Layer LoRA Fine-Tuning"
authors:
  - "Stanley Ngugi"
url: "http://arxiv.org/abs/2506.15415v1"
published: "2025-06-18"
citations: "0"
source: "arXiv"
id: "arxiv:2506.15415"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# Targeted Lexical Injection: Unlocking Latent Cross-Lingual Alignment in Lugha-Llama via Early-Layer LoRA Fine-Tuning

**Authors**: Stanley Ngugi
**Published**: 2025-06-18 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2506.15415v1

## Abstract
Large Language Models (LLMs) have demonstrated remarkable capabilities, yet their performance in low-resource languages (LRLs), such as Swahili, often lags due to data scarcity and underrepresentation in pre-training. A key challenge is achieving robust cross-lingual lexical alignment, crucial for tasks like translation and cross-lingual information retrieval. This paper introduces Targeted Lexical Injection (TLI), a novel and efficient fine-tuning approach. We first demonstrate that Lugha-Llama-8B-wura, a Swahili-centric LLM, exhibits strong, near-perfect lexical alignment for Swahili-English word pairs in its early internal layers (specifically Layer 2, with ~0.99998 average cosine similarity based on a pilot study), a capability not fully reflected in its final output representations (baseline ~0.32 similarity on our evaluation set). TLI leverages this insight by using Low-Rank Adaptation (LoRA) and a contrastive learning objective to fine-tune the model, specifically targeting embeddings from this empirically identified optimal early layer. Our experiments show that TLI significantly improves the output-level lexical alignment for 623 trained Swahili-English word pairs, increasing average cosine similarity from 0.3211 to 0.4113 (+28.08%, p < 1.33 x 10^-240). More importantly, these improvements generalize remarkably well to 63 unseen control word pairs, with similarity increasing from 0.3143 to 0.4033 (+28.32%, p < 7.17 x 10^-27). These findings suggest TLI enhances the model's ability to preserve and propagate its inherent early-layer cross-lingual knowledge, offering a parameter-efficient and effective strategy for improving lexical alignment in LRL-focused LLMs.
