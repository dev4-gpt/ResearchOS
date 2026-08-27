---
title: "Continual Relation Learning via Episodic Memory Activation and Reconsolidation"
authors:
  - "Xu Han"
  - "Yi Dai"
  - "Tianyu Gao"
  - "Yankai Lin"
  - "Zhiyuan Liu"
  - "Peng Li"
  - "Maosong Sun"
  - "Jie Zhou"
url: "https://doi.org/10.18653/v1/2020.acl-main.573"
published: "2020"
citations: "95"
source: "Crossref"
id: "10.18653/v1/2020.acl-main.573"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-continual-safety-alignment-in-vision-language-models"
---
# Continual Relation Learning via Episodic Memory Activation and Reconsolidation

**Authors**: Xu Han, Yi Dai, Tianyu Gao, Yankai Lin, Zhiyuan Liu, Peng Li, Maosong Sun, Jie Zhou
**Published**: 2020 | **Source**: Crossref
**URL**: https://doi.org/10.18653/v1/2020.acl-main.573

## Abstract
Continual relation learning aims to continually train a model on new data to learn incessantly emerging novel relations while avoiding catastrophically forgetting old relations. Some pioneering work has proved that storing a handful of historical relation examples in episodic memory and replaying them in subsequent training is an effective solution for such a challenging problem. However, these memorybased methods usually suffer from overfitting the few memorized examples of old relations, which may gradually cause inevitable confusion among existing relations. Inspired by the mechanism in human long-term memory formation, we introduce episodic memory activation and reconsolidation (EMAR) to continual relation learning. Every time neural models are activated to learn both new and memorized data, EMAR utilizes relation prototypes for memory reconsolidation exercise to keep a stable understanding of old relations. The experimental results show that EMAR could get rid of catastrophically forgetting old relations and outperform the state-of-the-art continual learning models. The code and datasets are released on https://github.com/thunlp/ ContinualRE.
