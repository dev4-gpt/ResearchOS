---
title: "DyLoRA: Parameter-Efficient Tuning of Pre-trained Models using Dynamic Search-Free Low-Rank Adaptation"
authors:
  - "Mojtaba Valipour"
  - "Mehdi Rezagholizadeh"
  - "Ivan Kobyzev"
  - "Ali Ghodsi"
url: "https://doi.org/10.18653/v1/2023.eacl-main.239"
published: "2023"
citations: "111"
source: "Crossref"
id: "10.18653/v1/2023.eacl-main.239"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# DyLoRA: Parameter-Efficient Tuning of Pre-trained Models using Dynamic Search-Free Low-Rank Adaptation

**Authors**: Mojtaba Valipour, Mehdi Rezagholizadeh, Ivan Kobyzev, Ali Ghodsi
**Published**: 2023 | **Source**: Crossref
**URL**: https://doi.org/10.18653/v1/2023.eacl-main.239

## Abstract
With the ever-growing size of pretrained models (PMs), fine-tuning them has become more expensive and resource-hungry. As a remedy, low-rank adapters (LoRA) keep the main pretrained weights of the model frozen and just introduce some learnable truncated SVD modules (so-called LoRA blocks) to the model. While LoRA blocks are parameter-efficient, they suffer from two major problems: first, the size of these blocks is fixed and cannot be modified after training (for example, if we need to change the rank of LoRA blocks, then we need to retrain them from scratch); second, optimizing their rank requires an exhaustive search and effort. In this work, we introduce a dynamic low-rank adaptation (DyLoRA) technique to address these two problems together. Our Dy-LoRA method trains LoRA blocks for a range of ranks instead of a single rank by sorting the representation learned by the adapter module at different ranks during training. We evaluate our solution on different natural language understanding (GLUE benchmark) and language generation tasks (E2E, DART and WebNLG) using different pretrained models such as RoBERTa and GPT with different sizes. Our results show that we can train dynamic search-free models with DyLoRA at least 4 to 7 times faster than LoRA without significantly compromising performance. Moreover, our models can perform consistently well on a much larger range of ranks compared to LoRA. 1
