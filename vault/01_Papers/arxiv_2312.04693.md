---
title: "GraphMETRO: Mitigating Complex Graph Distribution Shifts via Mixture of Aligned Experts"
authors:
  - "Shirley Wu"
  - "Kaidi Cao"
  - "Bruno Ribeiro"
  - "James Zou"
  - "Jure Leskovec"
url: "http://arxiv.org/abs/2312.04693v3"
published: "2023-12-07"
citations: "0"
source: "arXiv"
id: "arxiv:2312.04693"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# GraphMETRO: Mitigating Complex Graph Distribution Shifts via Mixture of Aligned Experts

**Authors**: Shirley Wu, Kaidi Cao, Bruno Ribeiro, James Zou, Jure Leskovec
**Published**: 2023-12-07 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2312.04693v3

## Abstract
Graph data are inherently complex and heterogeneous, leading to a high natural diversity of distributional shifts. However, it remains unclear how to build machine learning architectures that generalize to the complex distributional shifts naturally occurring in the real world. Here, we develop GraphMETRO, a Graph Neural Network architecture that models natural diversity and captures complex distributional shifts. GraphMETRO employs a Mixture-of-Experts (MoE) architecture with a gating model and multiple expert models, where each expert model targets a specific distributional shift to produce a referential representation w.r.t. a reference model, and the gating model identifies shift components. Additionally, we design a novel objective that aligns the representations from different expert models to ensure reliable optimization. GraphMETRO achieves state-of-the-art results on four datasets from the GOOD benchmark, which is comprised of complex and natural real-world distribution shifts, improving by 67% and 4.2% on the WebKB and Twitch datasets. Code and data are available at https://github.com/Wuyxin/GraphMETRO.
