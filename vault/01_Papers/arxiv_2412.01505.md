---
title: "Scaling Law for Language Models Training Considering Batch Size"
authors:
  - "Xian Shuai"
  - "Yiding Wang"
  - "Yimeng Wu"
  - "Xin Jiang"
  - "Xiaozhe Ren"
url: "http://arxiv.org/abs/2412.01505v1"
published: "2024-12-02"
citations: "0"
source: "arXiv"
id: "arxiv:2412.01505"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Scaling Law for Language Models Training Considering Batch Size

**Authors**: Xian Shuai, Yiding Wang, Yimeng Wu, Xin Jiang, Xiaozhe Ren
**Published**: 2024-12-02 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2412.01505v1

## Abstract
Large language models (LLMs) have made remarkable advances in recent years, with scaling laws playing a critical role in this rapid progress. In this paper, we empirically investigate how a critical hyper-parameter, i.e., the global batch size, influences the LLM training prdocess. We begin by training language models ranging from 125 million to 2.6 billion parameters, using up to 300 billion high-quality tokens. Through these experiments, we establish a basic scaling law on model size and training data amount. We then examine how varying batch sizes and learning rates affect the convergence and generalization of these models. Our analysis yields batch size scaling laws under two different cases: with a fixed compute budget, and with a fixed amount of training data. Extrapolation experiments on models of increasing sizes validate our predicted laws, which provides guidance for optimizing LLM training strategies under specific resource constraints.
