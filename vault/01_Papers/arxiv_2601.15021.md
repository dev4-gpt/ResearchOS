---
title: "Mixture-of-Experts Models in Vision: Routing, Optimization, and Generalization"
authors:
  - "Adam Rokah"
  - "Daniel Veress"
  - "Caleb Caulk"
  - "Sourav Sharan"
url: "http://arxiv.org/abs/2601.15021v1"
published: "2026-01-21"
citations: "0"
source: "arXiv"
id: "arxiv:2601.15021"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Mixture-of-Experts Models in Vision: Routing, Optimization, and Generalization

**Authors**: Adam Rokah, Daniel Veress, Caleb Caulk, Sourav Sharan
**Published**: 2026-01-21 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2601.15021v1

## Abstract
Mixture-of-Experts (MoE) architectures enable conditional computation by routing inputs to multiple expert subnetworks and are often motivated as a mechanism for scaling large language models. In this project, we instead study MoE behavior in an image classification setting, focusing on predictive performance, expert utilization, and generalization. We compare dense, SoftMoE, and SparseMoE classifier heads on the CIFAR10 dataset under comparable model capacity. Both MoE variants achieve slightly higher validation accuracy than the dense baseline while maintaining balanced expert utilization through regularization, avoiding expert collapse. To analyze generalization, we compute Hessian-based sharpness metrics at convergence, including the largest eigenvalue and trace of the loss Hessian, evaluated on both training and test data. We find that SoftMoE exhibits higher sharpness by these metrics, while Dense and SparseMoE lie in a similar curvature regime, despite all models achieving comparable generalization performance. Complementary loss surface perturbation analyses reveal qualitative differences in non-local behavior under finite parameter perturbations between dense and MoE models, which help contextualize curvature-based measurements without directly explaining validation accuracy. We further evaluate empirical inference efficiency and show that naively implemented conditional routing does not yield inference speedups on modern hardware at this scale, highlighting the gap between theoretical and realized efficiency in sparse MoE models.
