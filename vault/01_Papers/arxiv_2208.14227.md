---
title: "CLUDA : Contrastive Learning in Unsupervised Domain Adaptation for Semantic Segmentation"
authors:
  - "Midhun Vayyat"
  - "Jaswin Kasi"
  - "Anuraag Bhattacharya"
  - "Shuaib Ahmed"
  - "Rahul Tallamraju"
url: "http://arxiv.org/abs/2208.14227v2"
published: "2022-08-27"
citations: "0"
source: "arXiv"
id: "arxiv:2208.14227"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"
---
# CLUDA : Contrastive Learning in Unsupervised Domain Adaptation for Semantic Segmentation

**Authors**: Midhun Vayyat, Jaswin Kasi, Anuraag Bhattacharya, Shuaib Ahmed, Rahul Tallamraju
**Published**: 2022-08-27 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2208.14227v2

## Executive Summary & Abstract
In this work, we propose CLUDA, a simple, yet novel method for performing unsupervised domain adaptation (UDA) for semantic segmentation by incorporating contrastive losses into a student-teacher learning paradigm, that makes use of pseudo-labels generated from the target domain by the teacher network. More specifically, we extract a multi-level fused-feature map from the encoder, and apply contrastive loss across different classes and different domains, via source-target mixing of images. We consistently improve performance on various feature encoder architectures and for different domain adaptation datasets in semantic segmentation. Furthermore, we introduce a learned-weighted contrastive loss to improve upon on a state-of-the-art multi-resolution training approach in UDA. We produce state-of-the-art results on GTA $\rightarrow$ Cityscapes (74.4 mIOU, +0.6) and Synthia $\rightarrow$ Cityscapes (67.2 mIOU, +1.4) datasets. CLUDA effectively demonstrates contrastive learning in UDA as a generic method, which can be easily integrated into any existing UDA for semantic segmentation tasks. Please refer to the supplementary material for the details on implementation.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
CLUDA : Contrastive Learning in Unsupervised
Domain Adaptation for Semantic Segmentation
Midhun Vayyat, Jaswin Kasi, Anuraag Bhattacharya, Shuaib Ahmed, Rahul Tallamraju
Mercedes Benz Research and Development India
{midhun.vayyat, kasi.jaswin, anuraag.bhattacharya, shuaib.ahmed, rahul.tallamraju}@mercedes-benz.com
Abstract
In this work, we propose CLUDA, a simple, yet novel method for performing
unsupervised domain adaptation (UDA) for semantic segmentation by incorporating
contrastive losses into a student-teacher learning paradigm, that makes use of
pseudo-labels generated from the target domain by the teacher network. More
speciﬁcally, we extract a multi-level fused-feature map from the encoder, and
apply contrastive loss across different classes and different domains, via sourcetarget mixing of images. We consistently improve performance on various feature
encoder architectures and for different domain adaptation datasets in semantic
segmentation. Furthermore, we introduce a learned-weighted contrastive loss to
improve upon on a state-of-the-art multi-resolution training approach in UDA. We
produce state-of-the-art results on GTA→ Cityscapes (74.4 mIOU, +0.6, standard
deviation: 0.32) and Synthia→ Cityscapes (66.8 mIOU, +1.0, standard deviation:
0.44) datasets. CLUDA effectively demonstrates contrastive learning in UDA as a
generic method, which can be easily integrated into any existing UDA for semantic
segmentation tasks. Please refer to the appendix (section 7.7) for t
