---
title: "Sparse Low-rank Adaptation of Pre-trained Language Models"
authors:
  - "Ning Ding"
  - "Xingtai Lv"
  - "Qiaosen Wang"
  - "Yulin Chen"
  - "Bowen Zhou"
  - "Zhiyuan Liu"
  - "Maosong Sun"
url: "http://arxiv.org/abs/2311.11696v1"
published: "2023-11-20"
citations: "0"
source: "arXiv"
id: "arxiv:2311.11696"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Sparse Low-rank Adaptation of Pre-trained Language Models

**Authors**: Ning Ding, Xingtai Lv, Qiaosen Wang, Yulin Chen, Bowen Zhou, Zhiyuan Liu, Maosong Sun
**Published**: 2023-11-20 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2311.11696v1

## Abstract
Fine-tuning pre-trained large language models in a parameter-efficient manner is widely studied for its effectiveness and efficiency. The popular method of low-rank adaptation (LoRA) offers a notable approach, hypothesizing that the adaptation process is intrinsically low-dimensional. Although LoRA has demonstrated commendable performance, it is implemented with a fixed and unalterable intrinsic rank that might not always be the ideal choice. Recognizing the need for more flexible adaptation, we extend the methodology of LoRA to an innovative approach we call sparse low-rank adaptation (SoRA) that enables dynamic adjustments to the intrinsic rank during the adaptation process. We achieve this through the incorporation of a gate unit optimized with proximal gradient method in the training stage, controlling the cardinality of rank under the sparsity of the gate. In the subsequent inference stage, we eliminate the parameter blocks corresponding to the zeroed-out ranks, to reduce each SoRA module back to a concise yet rank-optimal LoRA. Our approach strengthens the representation power of LoRA by initializing it with a higher rank, while efficiently taming a temporarily increased number of parameters via updating in a sparse way. We further introduce a sparsifying scheduler for SoRA, aiming to examine the impact of the number of non-zero parameters on the model's memorization and generalization. Our experimental results demonstrate that SoRA can outperform other baselines even with 70% retained parameters and 70% training time.
