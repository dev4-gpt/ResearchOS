---
title: "TempRet: Temporal Enhancement and Two-Stage Reranking for CVPR 2026 EPIC-KITCHENS-100 Multi-Instance Retrieval Challenge"
authors:
  - "Zixu Li"
  - "Yupeng Hu"
  - "Zhiwei Chen"
  - "Zhiheng Fu"
  - "Xiaowei Zhu"
  - "Weili Guan"
  - "Liqiang Nie"
url: "http://arxiv.org/abs/2605.24470v3"
published: "2026-05-23"
citations: "0"
source: "arXiv"
id: "arxiv:2605.24470"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "topic:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target:-cvpr-2026-workshop-on-multimodal-learning-+-arxiv-pre-print"
---
# TempRet: Temporal Enhancement and Two-Stage Reranking for CVPR 2026 EPIC-KITCHENS-100 Multi-Instance Retrieval Challenge

**Authors**: Zixu Li, Yupeng Hu, Zhiwei Chen, Zhiheng Fu, Xiaowei Zhu, Weili Guan, Liqiang Nie
**Published**: 2026-05-23 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2605.24470v3

## Executive Summary & Abstract
Video-text retrieval has witnessed remarkable progress driven by large-scale vision-language pretraining, yet most existing approaches inherit an implicit assumption from image-text retrieval: that visual semantics can be captured frame-by-frame. This assumption overlooks the temporal dynamics of egocentric videos. The EPIC-KITCHENS-100 Multi-Instance Retrieval (MIR) challenge further raises the bar by providing soft-label relevance matrices rather than binary labels, demanding models that can resolve graded semantic correspondences across modalities. In this report, we present our solution, termed TempRet, to the CVPR 2026 EPIC-KITCHENS-100 MIR challenge. Our approach builds upon a CLIP-based dual-encoder backbone and introduces two key components to address the temporal and cross-modal challenges. First, a temporal transformer operates exclusively on the video side, modeling inter-frame dependencies through learnable positional encodings and multi-head self-attention over frame-level CLIP features. Second, a two-stage reranking pipeline first retrieves Top-K candidates via the dual-encoder, then refines their scores using a cross-encoder equipped with an Image-Text Matching (ITM) head. The entire system is trained with Symmetric Multi-Similarity Loss to exploit the soft-label relevance matrices provided by the challenge. Our method achieves 67.97% average mAP and 82.92% average nDCG on the EK-100 MIR benchmark, demonstrating the effectiveness of temporal modeling and cross-modal refinement for egocentric video retrieval.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
TempRet: Temporal Enhancement and Two-Stage Reranking for CVPR 2026
EPIC-KITCHENS-100 Multi-Instance Retrieval Challenge
Zixu Li1 Yupeng Hu1 Zhiwei Chen1 Zhiheng Fu1 Xiaowei Zhu1 Weili Guan2 Liqiang Nie2
1Shandong University 2Harbin Institute of Technology (Shenzhen)
{lizixu.cs, zivczw, fuzhiheng8, xiaoweizhu2005, honeyguan, nieliqiang}@gmail.com;
huyupeng@sdu.edu.cn
Abstract
Video-text retrieval has witnessed remarkable progress
driven by large-scale vision-language pretraining, yet most
existing approaches inherit an implicit assumption from
image-text retrieval: that visual semantics can be captured
frame-by-frame. This assumption overlooks the temporal
dynamics of egocentric videos. The EPIC-KITCHENS-100
Multi-Instance Retrieval (MIR) challenge further raises the
bar by providing soft-label relevance matrices rather than
binary labels, demanding models that can resolve graded
semantic correspondences across modalities. In this report, we present our solution, termedTempRet, to the CVPR
2026 EPIC-KITCHENS-100 MIR challenge. Our approach
builds upon a CLIP-based dual-encoder backbone and introduces two key components to address the temporal and
cross-modal challenges. First, atemporal transformeroperates exclusively on the video side, modeling inter-frame
dependencies through learnable positional encodings and
multi-head self-attention over frame-level CLIP features.
Second, atwo-stage rerankingpipeline first retrieves TopKcandidates via the dual-encoder, then refines their
