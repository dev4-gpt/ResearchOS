---
title: "Autoencoder techniques for survival analysis on renal cell carcinoma"
authors:
  - "Iñigo Sanz Ilundain"
  - "Laura Hernández-Lorenzo"
  - "Cristina Rodríguez-Antona"
  - "Jesús García-Donas"
  - "José L Ayala"
url: "https://doi.org/10.1371/journal.pone.0321045"
published: "2025-05-15"
citations: "0"
source: "PLOS"
id: "plos:10.1371/journal.pone.0321045"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Autoencoder techniques for survival analysis on renal cell carcinoma

**Authors**: Iñigo Sanz Ilundain, Laura Hernández-Lorenzo, Cristina Rodríguez-Antona, Jesús García-Donas, José L Ayala
**Published**: 2025-05-15 | **Citations**: 0 | **Source**: PLOS
**URL**: https://doi.org/10.1371/journal.pone.0321045

## Executive Summary & Abstract

Survival is the gold standard in oncology when determining the real impact of therapies in patients outcome. Thus, identifying molecular predictors of survival (like genetic alterations or transcriptomic patterns of gene expression) is one of the most relevant fields in current research. Statistical methods and metrics to analyze time-to-event data are crucial in understanding disease progression and the effectiveness of treatments. However, in the medical field, data is often high-dimensional, complicating the application of such methodologies. In this study, we addressed this challenge by compressing the high-dimensional transcriptomic data of patients treated with immunotherapy (avelumab + axitinib) and a TKI (sunitinib) into latent, meaningful features using autoencoders. We applied a semi-parametric statistical approach based on the COX Proportional Hazards model, coupled with Breslow’s estimator, to predict each patient’s Progression-Free Survival (PFS) and determine survival functions. Our analysis explored various penalty configurations and their combinations. Given the complexity of transcriptomic data, we extended our model to incorporate both tabular data and its graph variant, where edges represent protein-protein interactions between genes, offering a more insightful approach. Recognizing the interpretability challenges inherent in neural networks, particularly autoencoders, we analyzed the mutual information between genes in the original data and their latent feature representations to clarify which genes are most associated with specific latent variables. The results indicate that different types of autoencoders are better suited for different tasks: denoising autoencoders excel at accurate reconstruction, while the sparse variant is more effective at producing meaningful representations. Additionally, combining these penalties enhances both reconstruction quality and the interpretability of latent features. The interpretable models identified genes such as LRP2 and ACE2 as highly relevant to renal cell carcinoma. This research underscores the utility of autoencoders in managing high-dimensional data problems.


## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet

Survival is the gold standard in oncology when determining the real impact of therapies in patients outcome. Thus, identifying molecular predictors of survival (like genetic alterations or transcriptomic patterns of gene expression) is one of the most relevant fields in current research. Statistical methods and metrics to analyze time-to-event data are crucial in understanding disease progression and the effectiveness of treatments. However, in the medical field, data is often high-dimensional, complicating the application of such methodologies. In this study, we addressed this challenge by compressing the high-dimensional transcriptomic data of patients treated with immunotherapy (avelumab + axitinib) and a TKI (sunitinib) into latent, meaningful features using autoencoders. We applied a semi-parametric statistical approach based on the COX Proportional Hazards model, coupled with Breslow’s estimator, to predict each patient’s Progression-Free Survival (PFS) and determine survival functions. Our analysis explored various penalty configurations and their combinations. Given the complexity of transcriptomic data, we extended our model to incorporate both tabular data and its graph variant, where edges represent protein-protein interactions between genes, offering a more insightful approach. Recognizing the interpretability challenges inherent in neural networks, particularly autoencoders, we analyzed the mutual information between genes in the original data and their latent f
