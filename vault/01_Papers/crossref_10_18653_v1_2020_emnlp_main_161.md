---
title: "HERO: Hierarchical Encoder for Video+Language Omni-representation Pre-training"
authors:
  - "Linjie Li"
  - "Yen‐Chun Chen"
  - "Yu Cheng"
  - "Zhe Gan"
  - "Licheng Yu"
  - "Jingjing Liu"
url: "https://doi.org/10.18653/v1/2020.emnlp-main.161"
published: "2020"
citations: "393"
source: "Crossref"
id: "10.18653/v1/2020.emnlp-main.161"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-spatio-temporal-grounding-in-video-question-answering"
---
# HERO: Hierarchical Encoder for Video+Language Omni-representation Pre-training

**Authors**: Linjie Li, Yen‐Chun Chen, Yu Cheng, Zhe Gan, Licheng Yu, Jingjing Liu
**Published**: 2020 | **Source**: Crossref
**URL**: https://doi.org/10.18653/v1/2020.emnlp-main.161

## Abstract
We present HERO, a novel framework for large-scale video+language omnirepresentation learning. HERO encodes multimodal inputs in a hierarchical structure, where local context of a video frame is captured by a Cross-modal Transformer via multimodal fusion, and global video context is captured by a Temporal Transformer. In addition to standard Masked Language Modeling (MLM) and Masked Frame Modeling (MFM) objectives, we design two new pre-training tasks: (i) Video-Subtitle Matching (VSM), where the model predicts both global and local temporal alignment; and (ii) Frame Order Modeling (FOM), where the model predicts the right order of shuffled video frames. HERO is jointly trained on HowTo100M and large-scale TV datasets to gain deep understanding of complex social dynamics with multi-character interactions. Comprehensive experiments demonstrate that HERO achieves new state of the art on multiple benchmarks over Text-based Video/Video-moment Retrieval, Video Question Answering (QA), Video-and-language Inference and Video Captioning tasks across different domains. We also introduce two new challenging benchmarks How2QA and How2R for Video QA and Retrieval, collected from diverse video content over multimodalities.
