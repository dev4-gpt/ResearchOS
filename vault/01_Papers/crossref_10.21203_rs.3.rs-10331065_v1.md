---
title: "Automated Fracture Image Captioning Using Multimodal Vision-Language Models: A Comprehensive Comparative Study on a Clinically Curated Dataset"
authors:
  - "Nikosi"
url: "https://doi.org/10.21203/rs.3.rs-10331065/v1"
published: "2026-7-14"
citations: "0"
source: "Crossref"
id: "crossref:10.21203/rs.3.rs-10331065/v1"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - ""multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms""
---
# Automated Fracture Image Captioning Using Multimodal Vision-Language Models: A Comprehensive Comparative Study on a Clinically Curated Dataset

**Authors**: Nikosi
**Published**: 2026-7-14 | **Citations**: 0 | **Source**: Crossref
**URL**: https://doi.org/10.21203/rs.3.rs-10331065/v1

## Executive Summary & Abstract
Abstract
                Medical image captioning has emerged as a critical task at the intersection of computer vision and natural language processing, with the potential to significantly augment clinical workflows by automatically generating descriptive textual  reports from radiographic images. Among the various imaging modalities, musculoskeletal radiographs particularly those depicting bone fractures present unique challenges due to the subtle visual features that distinguish fracture types, locations, and severities. Manual reporting of such images demands considerable radiologist expertise and time, making automated captioning systems highly desirable in resource-constrained healthcare settings. Recent advances in deep learning, particularly the development of transformer-based architectures, have revolutionised both visual understanding and language generation. Vision Transformers (ViT) and their variants including Swin Transformer, DeiT, and BEiT have demonstrated remarkable capacity to extract hierarchical visual representations from medical images. Concurrently, large autoregressive language models such as GPT-2 have shown strong performance in conditional text generation tasks. The integration of these two families of models through cross-attention mechanisms forms the backbone of modern vision-language systems capable of bridging visual perception and language generation. Vision-language pre-training (VLP) frameworks such as BLIP and GIT have further advanced the field by jointly optimising visual and linguistic objectives on large-scale image-text corpora, enabling richer semantic grounding between image features and generated descriptions. However, the application of such frameworks to specialised medical domains particularly fracture radiograph captioning remains underexplored, with most existing work focusing on chest X-rays or general radiology reports. In this work, we present a systematic benchmark of nine encoder-decoder architectures for automated fracture radiograph captioning on the Ibn Sina Medical Centre dataset, comprising 710 annotated fracture X-ray and caption pairs. We evaluate combinations of six visual encoders (ViT-Base, Swin-Tiny, DeiT-Base, BEiT-Base, ConvNeXt-Tiny, CLIP-ViT) with GPT-2 decoders of varying capacities, alongside two end-to-end VLP models (BLIP-Base, GIT-Base) and a pretrained ViT-GPT2 baseline. Our experiments reveal that BLIP-Base achieves the highest performance across all metrics (BLEU-4 = 0.353, METEOR = 0.530, ROUGE-L = 0.464, CIDEr = 0.505), while Swin-Tiny offers the most parameter-efficient solution. We additionally analyse failure modes including trivial solution collapse in CLIP-based models and gradient divergence in oversized decoder configurations, providing practical guidance for architecture selection in low-resource medical captioning tasks. The main contributions of this work are as follows: (i) a comprehensive benchmark of nine encoder-decoder architectures on fracture radiograph captioning; (ii) a systematic analysis of the effect of encoder pre-training strategy and decoder capacity on caption quality; (iii) an investigation of failure modes and degenerate convergence behaviours in vision-language architectures applied to small medical datasets; and (iv) empirical evidence that vision-language pre-training with unified objectives substantially outperforms independently coupled encoder-decoder systems for specialised medical image captioning.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Abstract
                Medical image captioning has emerged as a critical task at the intersection of computer vision and natural language processing, with the potential to significantly augment clinical workflows by automatically generating descriptive textual  reports from radiographic images. Among the various imaging modalities, musculoskeletal radiographs particularly those depicting bone fractures present unique challenges due to the subtle visual features that distinguish fracture types, locations, and severities. Manual reporting of such images demands considerable radiologist expertise and time, making automated captioning systems highly desirable in resource-constrained healthcare settings. Recent advances in deep learning, particularly the development of transformer-based architectures, have revolutionised both visual understanding and language generation. Vision Transformers (ViT) and their variants including Swin Transformer, DeiT, and BEiT have demonstrated remarkable capacity to extract hierarchical visual representations from medical images. Concurrently, large autoregressive language models such as GPT-2 have shown strong performance in conditional text generation tasks. The integration of these two families of models through cross-attention mechanisms forms the backbone of modern vision-language systems capable of bridging visual perception and language generation. Vision-language pre-training (VLP) frameworks such as BLIP and GIT have further advanced the
