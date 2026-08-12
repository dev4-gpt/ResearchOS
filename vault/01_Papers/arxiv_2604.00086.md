---
title: "Hierarchical Pre-Training of Vision Encoders with Large Language Model"
authors:
  - "Eugene Lee"
  - "Ting-Yu Chang"
  - "Jui-Huang Tsai"
  - "Jiajie Diao"
  - "Chen-Yi Lee"
url: "http://arxiv.org/abs/2604.00086v2"
published: "2026-03-31"
citations: "0"
source: "arXiv"
id: "arxiv:2604.00086"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"
---
# Hierarchical Pre-Training of Vision Encoders with Large Language Model

**Authors**: Eugene Lee, Ting-Yu Chang, Jui-Huang Tsai, Jiajie Diao, Chen-Yi Lee
**Published**: 2026-03-31 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2604.00086v2

## Executive Summary & Abstract
The field of computer vision has experienced significant advancements through scalable vision encoders and multimodal pre-training frameworks. However, existing approaches often treat vision encoders and large language models (LLMs) as independent modules, limiting the integration of hierarchical visual features. In this work, we propose HIVE (Hierarchical Pre-Training of Vision Encoders), a novel framework that enhances vision-language alignment by introducing hierarchical cross-attention between the vision encoder and LLM. Unlike conventional methods that flatten image embeddings, HIVE enables structured feature fusion across multiple layers, improving gradient flow and representation learning. To optimize this interaction, we introduce a three-stage training strategy that progressively aligns the vision encoder with the LLM, ensuring stable optimization and effective multimodal fusion. Empirical evaluations demonstrate that HIVE achieves superior performance not only in image classification but also on various vision-language tasks, outperforming self-attention-based methods in benchmarks such as MME, GQA, OK-VQA, and ScienceQA. Our results highlight the benefits of hierarchical feature integration, paving the way for more efficient and expressive vision-language models.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Hierarchical Pre-Training of Vision Encoders with Large Language Models
Eugene Lee1, Ting-Yu Chang2, Jui-Huang Tsai2, Jiajie Diao1, Chen-Yi Lee2
1 University of Cincinnati 2 National Yang Ming Chiao Tung University
eugene.lee@uc.edu, jiajie.diao@uc.edu, cylee@nycu.edu.tw
Abstract
The field of computer vision has experienced significant
advancements through scalable vision encoders and multimodal pre-training frameworks. However, existing approaches often treat vision encoders and large language
models (LLMs) as independent modules, limiting the integration of hierarchical visual features. In this work, we propose HIVE (Hierarchical Pre-Training of Vision Encoders),
a novel framework that enhances vision-language alignment by introducing hierarchical cross-attention between
the vision encoder and LLM. Unlike conventional methods that flatten image embeddings, HIVE enables structured feature fusion across multiple layers, improving gradient flow and representation learning. To optimize this interaction, we introduce a three-stage training strategy that
progressively aligns the vision encoder with the LLM, ensuring stable optimization and effective multimodal fusion.
Empirical evaluations demonstrate that HIVE achieves superior performance not only in image classification but
also on various vision-language tasks, outperforming selfattention-based methods in benchmarks such as MME,
GQA, OK-VQA, and ScienceQA. Our results highlight the
benefits of hierarchical feature integration
