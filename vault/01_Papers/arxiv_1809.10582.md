---
title: "Kernel based low-rank sparse model for single image super-resolution"
authors:
  - "Jiahe Shi"
  - "Chun Qi"
url: "http://arxiv.org/abs/1809.10582v1"
published: "2018-09-27"
citations: "0"
source: "arXiv"
id: "arxiv:1809.10582"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Kernel based low-rank sparse model for single image super-resolution

**Authors**: Jiahe Shi, Chun Qi
**Published**: 2018-09-27 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1809.10582v1

## Abstract
Self-similarity learning has been recognized as a promising method for single image super-resolution (SR) to produce high-resolution (HR) image in recent years. The performance of learning based SR reconstruction, however, highly depends on learned representation coeffcients. Due to the degradation of input image, conventional sparse coding is prone to produce unfaithful representation coeffcients. To this end, we propose a novel kernel based low-rank sparse model with self-similarity learning for single image SR which incorporates nonlocalsimilarity prior to enforce similar patches having similar representation weights. We perform a gradual magnification scheme, using self-examples extracted from the degraded input image and up-scaled versions. To exploit nonlocal-similarity, we concatenate the vectorized input patch and its nonlocal neighbors at different locations into a data matrix which consists of similar components. Then we map the nonlocal data matrix into a high-dimensional feature space by kernel method to capture their nonlinear structures. Under the assumption that the sparse coeffcients for the nonlocal data in the kernel space should be low-rank, we impose low-rank constraint on sparse coding to share similarities among representation coeffcients and remove outliers in order that stable weights for SR reconstruction can be obtained. Experimental results demonstrate the advantage of our proposed method in both visual quality and reconstruction error.
