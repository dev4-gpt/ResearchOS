---
title: "LoRA-FAIR: Federated LoRA Fine-Tuning with Aggregation and Initialization Refinement"
authors:
  - "Jieming Bian"
  - "Lei Wang"
  - "Letian Zhang"
  - "Jie Xu"
url: "http://arxiv.org/abs/2411.14961v3"
published: "2024-11-22"
citations: "0"
source: "arXiv"
id: "arxiv:2411.14961"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# LoRA-FAIR: Federated LoRA Fine-Tuning with Aggregation and Initialization Refinement

**Authors**: Jieming Bian, Lei Wang, Letian Zhang, Jie Xu
**Published**: 2024-11-22 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2411.14961v3

## Abstract
Foundation models (FMs) achieve strong performance across diverse tasks with task-specific fine-tuning, yet full parameter fine-tuning is often computationally prohibitive for large models. Parameter-efficient fine-tuning (PEFT) methods like Low-Rank Adaptation (LoRA) reduce this cost by introducing low-rank matrices for tuning fewer parameters. While LoRA allows for efficient fine-tuning, it requires significant data for adaptation, making Federated Learning (FL) an appealing solution due to its privacy-preserving collaborative framework. However, combining LoRA with FL introduces two key challenges: the \textbf{Server-Side Aggregation Bias}, where server-side averaging of LoRA matrices diverges from the ideal global update, and the \textbf{Client-Side Initialization Lag}, emphasizing the need for consistent initialization across rounds. Existing approaches address these challenges individually, limiting their effectiveness. We propose LoRA-FAIR, a novel method that tackles both issues by introducing a correction term on the server, enhancing aggregation efficiency and accuracy. LoRA-FAIR maintains computational and communication efficiency, yielding superior performance over state-of-the-art methods. Experimental results on ViT and MLP-Mixer models across large-scale datasets demonstrate that LoRA-FAIR consistently achieves performance improvements in FL settings.
