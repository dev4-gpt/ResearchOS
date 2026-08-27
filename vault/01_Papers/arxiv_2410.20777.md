---
title: "KD-LoRA: A Hybrid Approach to Efficient Fine-Tuning with LoRA and Knowledge Distillation"
authors:
  - "Rambod Azimi"
  - "Rishav Rishav"
  - "Marek Teichmann"
  - "Samira Ebrahimi Kahou"
url: "http://arxiv.org/abs/2410.20777v1"
published: "2024-10-28"
citations: "0"
source: "arXiv"
id: "arxiv:2410.20777"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# KD-LoRA: A Hybrid Approach to Efficient Fine-Tuning with LoRA and Knowledge Distillation

**Authors**: Rambod Azimi, Rishav Rishav, Marek Teichmann, Samira Ebrahimi Kahou
**Published**: 2024-10-28 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2410.20777v1

## Abstract
Large language models (LLMs) have demonstrated remarkable performance across various downstream tasks. However, the high computational and memory requirements of LLMs are a major bottleneck. To address this, parameter-efficient fine-tuning (PEFT) methods such as low-rank adaptation (LoRA) have been proposed to reduce computational costs while ensuring minimal loss in performance. Additionally, knowledge distillation (KD) has been a popular choice for obtaining compact student models from teacher models. In this work, we present KD-LoRA, a novel fine-tuning method that combines LoRA with KD. Our results demonstrate that KD-LoRA achieves performance comparable to full fine-tuning (FFT) and LoRA while significantly reducing resource requirements. Specifically, KD-LoRA retains 98% of LoRA's performance on the GLUE benchmark, while being 40% more compact. Additionally, KD-LoRA reduces GPU memory usage by 30% compared to LoRA, while decreasing inference time by 30% compared to both FFT and LoRA. We evaluate KD-LoRA across three encoder-only models: BERT, RoBERTa, and DeBERTaV3. Code is available at https://github.com/rambodazimi/KD-LoRA.
