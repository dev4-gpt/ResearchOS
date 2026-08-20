---
title: "Opening the Black Box of Scientific Foundation Models: A Review of Sparse Autoencoders for Mechanistic Interpretability"
authors:
  - "Olivia Denvis"
url: "https://doi.org/10.2139/ssrn.6955478"
published: "2026-7-29"
citations: "0"
source: "Crossref"
id: "crossref:10.2139/ssrn.6955478"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Opening the Black Box of Scientific Foundation Models: A Review of Sparse Autoencoders for Mechanistic Interpretability

**Authors**: Olivia Denvis
**Published**: 2026-7-29 | **Citations**: 0 | **Source**: Crossref
**URL**: https://doi.org/10.2139/ssrn.6955478

## Executive Summary & Abstract
Foundation models trained on biological sequences-proteins, genomes, and single-cell transcriptomesnow rival or exceed task-specific methods across structure prediction, variant effect estimation, and cell-state annotation. Yet their internal representations remain opaque, a liability that is especially acute in science, where a prediction is only as useful as the mechanism it can be traced to. Sparse autoencoders (SAEs), originally developed to decompose the polysemantic activations of large language models into monosemantic, human-interpretable features, have rapidly become the leading tool for mechanistic interpretability and are now being applied to scientific foundation models. This review synthesizes the emerging literature at this intersection. We first trace the conceptual lineage of SAEs from classical sparse coding and dictionary learning to the superposition hypothesis and modern architectural variants (Gated, JumpReLU, and TopK SAEs). We then survey applications across the biological model landscape: protein language models, where SAEs recover features aligned to binding sites, structural motifs, and functional annotations; single-cell foundation models, where SAEs expose interpretable cell-type programs and steerable directions; and genomic language models, where features map to regulatory and structural sequence elements. We contrast these with non-biological scientific domains-chemistry, materials, climate, and time series-to identify what is general and what is biology-specific. Throughout, we emphasize a recurring tension between the seductive interpretability of SAE features and a growing body of critical evaluations questioning their faithfulness and practical utility. We close with open problems: ground-truth evaluation against biological knowledge bases, the role of nonlinear and cross-layer features, and the path from interpretation to validated scientific discovery.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Foundation models trained on biological sequences-proteins, genomes, and single-cell transcriptomesnow rival or exceed task-specific methods across structure prediction, variant effect estimation, and cell-state annotation. Yet their internal representations remain opaque, a liability that is especially acute in science, where a prediction is only as useful as the mechanism it can be traced to. Sparse autoencoders (SAEs), originally developed to decompose the polysemantic activations of large language models into monosemantic, human-interpretable features, have rapidly become the leading tool for mechanistic interpretability and are now being applied to scientific foundation models. This review synthesizes the emerging literature at this intersection. We first trace the conceptual lineage of SAEs from classical sparse coding and dictionary learning to the superposition hypothesis and modern architectural variants (Gated, JumpReLU, and TopK SAEs). We then survey applications across the biological model landscape: protein language models, where SAEs recover features aligned to binding sites, structural motifs, and functional annotations; single-cell foundation models, where SAEs expose interpretable cell-type programs and steerable directions; and genomic language models, where features map to regulatory and structural sequence elements. We contrast these with non-biological scientific domains-chemistry, materials, climate, and time series-to identify what is general and what i
