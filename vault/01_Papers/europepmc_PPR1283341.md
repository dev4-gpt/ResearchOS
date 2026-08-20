---
title: "Findings from Sparse Autoencoders for DNA Sequence Models: Motif Detectors, Reading-Frame Features, and the Scarcity of Regulatory Logic"
authors:
  - "Denvis O."
url: "https://doi.org/10.21203/rs.3.rs-10434163/v1"
published: "2026"
citations: "0"
source: "EuropePMC & Crossref"
id: "europepmc:PPR1283341"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Findings from Sparse Autoencoders for DNA Sequence Models: Motif Detectors, Reading-Frame Features, and the Scarcity of Regulatory Logic

**Authors**: Denvis O.
**Published**: 2026 | **Citations**: 0 | **Source**: EuropePMC & Crossref
**URL**: https://doi.org/10.21203/rs.3.rs-10434163/v1

## Executive Summary & Abstract
Abstract
                Sparse autoencoders (SAEs) have become the standard tool for decomposing the internal activations of language models into human-interpretable features, but their behaviour on DNA sequence models— transformers and long-convolution models pretrained on genomes—remains largely uncharted. Rather than train an exhaustive suite, we present a deliberately narrow study: we fit top-𝐾 SAEs to the residual stream at a sweep of layers of Nucleotide Transformer v2 (500M) and HyenaDNA, and dissect the resulting features against a curated panel of genomic annotations (GENCODE splice sites and reading frames, ENCODE transcription-factor peaks, CpG islands, promoter elements, and repeats). Four findings emerge. First, SAE features are far more monosemantic than raw neurons: at the most interpretable layer, 62% of alive SAE features receive a confident label versus 18% of neurons, and the fraction aligning with a genomic annotation at AUROC&gt;0.8 rises from 5% to 21%. Second, interpretability is strongly layer-dependent, peaking near 0.6 relative depth and collapsing in the final layers. Third, the recovered vocabulary is dominated by local sequence grammar—single-motif detectors (splice donor GT, start codon ATG, poly-A signals, TATA boxes, individual TF motifs), GC/CpG composition, and reading-frame period-3 features that fire selectively in coding sequence. Fourth, and in contrast, features encoding regulatory logic—combinatorial or context-conditional computation not reducible to a single motif—are rare (1.4% of features by a conditional-selectivity test) and weak. Cross-model matching is high for simple motifs and near chance for combinatorial features, and causal ablation confirms that the interpretable features are genuinely used downstream. These results mirror recent single-cell findings that foundation models encode organized biological knowledge but little regulatory logic, and suggest that SAEs on current DNA models recover a genomic dictionary more than a genomic grammar engine. Code and trained SAEs are released.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Abstract
                Sparse autoencoders (SAEs) have become the standard tool for decomposing the internal activations of language models into human-interpretable features, but their behaviour on DNA sequence models— transformers and long-convolution models pretrained on genomes—remains largely uncharted. Rather than train an exhaustive suite, we present a deliberately narrow study: we fit top-𝐾 SAEs to the residual stream at a sweep of layers of Nucleotide Transformer v2 (500M) and HyenaDNA, and dissect the resulting features against a curated panel of genomic annotations (GENCODE splice sites and reading frames, ENCODE transcription-factor peaks, CpG islands, promoter elements, and repeats). Four findings emerge. First, SAE features are far more monosemantic than raw neurons: at the most interpretable layer, 62% of alive SAE features receive a confident label versus 18% of neurons, and the fraction aligning with a genomic annotation at AUROC&gt;0.8 rises from 5% to 21%. Second, interpretability is strongly layer-dependent, peaking near 0.6 relative depth and collapsing in the final layers. Third, the recovered vocabulary is dominated by local sequence grammar—single-motif detectors (splice donor GT, start codon ATG, poly-A signals, TATA boxes, individual TF motifs), GC/CpG composition, and reading-frame period-3 features that fire selectively in coding sequence. Fourth, and in contrast, features encoding regulatory logic—combinatorial or context-conditional computation 
