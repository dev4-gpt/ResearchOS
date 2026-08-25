---
title: "Adversarial Feature Alignment: Avoid Catastrophic Forgetting in Incremental Task Lifelong Learning"
authors:
  - "Xin Yao"
  - "Tianchi Huang"
  - "Chenglei Wu"
  - "Rui-Xiao Zhang"
  - "Lifeng Sun"
url: "https://doi.org/10.1162/neco_a_01232"
published: "2019"
citations: "27"
source: "Crossref"
id: "10.1162/neco_a_01232"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-continual-safety-alignment-in-vision-language-models"
---
# Adversarial Feature Alignment: Avoid Catastrophic Forgetting in Incremental Task Lifelong Learning

**Authors**: Xin Yao, Tianchi Huang, Chenglei Wu, Rui-Xiao Zhang, Lifeng Sun
**Published**: 2019 | **Source**: Crossref
**URL**: https://doi.org/10.1162/neco_a_01232

## Abstract
, is one of the major roadblocks that prevent deep neural networks from achieving human-level artificial intelligence. Several research efforts (e.g., lifelong or continual learning algorithms) have proposed to tackle this problem. However, they either suffer from an accumulating drop in performance as the task sequence grows longer, or require storing an excessive number of model parameters for historical memory, or cannot obtain competitive performance on the new tasks. In this letter, we focus on the incremental multitask image classification scenario. Inspired by the learning process of students, who usually decompose complex tasks into easier goals, we propose an adversarial feature alignment method to avoid catastrophic forgetting. In our design, both the low-level visual features and high-level semantic features serve as soft targets and guide the training process in multiple stages, which provide sufficient supervised information of the old tasks and help to reduce forgetting. Due to the knowledge distillation and regularization phenomena, the proposed method gains even better performance than fine-tuning on the new tasks, which makes it stand out from other methods. Extensive experiments in several typical lifelong learning scenarios demonstrate that our method outperforms the state-of-the-art methods in both accuracy on new tasks and performance preservation on old tasks.
