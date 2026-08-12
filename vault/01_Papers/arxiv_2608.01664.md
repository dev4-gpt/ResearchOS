---
title: "FAU at ImageCLEF 2026 Task on Multimodal Reasoning Robust Candidate Scoring and Concise Multilingual Visual Answering"
authors:
  - "Mohamed Basem"
  - "Vincent Christlein"
url: "http://arxiv.org/abs/2608.01664v1"
published: "2026-08-03"
citations: "0"
source: "arXiv"
id: "arxiv:2608.01664"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "topic:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target:-cvpr-2026-workshop-on-multimodal-learning-+-arxiv-pre-print"
---
# FAU at ImageCLEF 2026 Task on Multimodal Reasoning Robust Candidate Scoring and Concise Multilingual Visual Answering

**Authors**: Mohamed Basem, Vincent Christlein
**Published**: 2026-08-03 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2608.01664v1

## Executive Summary & Abstract
We present our ImageCLEF 2026 Multimodal Reasoning system for the Visual Multiple Choice Question Answering (Visual MCQ) and Visual Open Question Answering (Visual OpenQA) subtasks. The challenge requires reliable reasoning over multilingual educational and scientific images with dense text, diagrams, charts, tables, formulas, and units, while enforcing strict answer formats. Our central finding is that robust output control is as important as model choice. For Visual MCQ, we replace fragile free-form generation with direct candidate label scoring from vision-language model logits, then combine complementary runs through score fusion and voting. For Visual OpenQA, we use image enhancement, concise final answer prompting, deterministic decoding, and targeted post-processing to remove reasoning traces and formatting artifacts. Without task-specific model training, our official submissions achieved third place in Visual MCQ with 0.7108 accuracy and first place in Visual OpenQA with 0.6488 COMET, 0.1391 BLEU, 0.2762 ROUGE L, and 0.2383 METEOR. The results highlight the practical value of inference engineering: careful scoring, ensembling, prompting, and cleanup can turn strong VLMs into reliable competition systems.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
FAU at ImageCLEF 2026 Task on Multimodal Reasoning:
Robust Candidate Scoring and Concise Multilingual Visual
Answering
Mohamed Basem1, Vincent Christlein 1
1Friedrich-Alexander-Universität Erlangen-Nürnberg, Erlangen, Germany
Abstract
We present our ImageCLEF 2026 Multimodal Reasoning system for the Visual Multiple Choice Question Answering
(Visual MCQ) and Visual Open Question Answering (Visual OpenQA) subtasks. The challenge requires reliable
reasoning over multilingual educational and scientific images with dense text, diagrams, charts, tables, formulas,
and units, while enforcing strict answer formats. Our central finding is that robust output control is as important
as model choice. For Visual MCQ, we replace fragile free-form generation with direct candidate label scoring from
vision-language model logits, then combine complementary runs through score fusion and voting. For Visual
OpenQA, we use image enhancement, concise final answer prompting, deterministic decoding, and targeted
post-processing to remove reasoning traces and formatting artifacts. Without task-specific model training, our
official submissions achieved third place in Visual MCQ with 0.7108 accuracy and first place in Visual OpenQA
with 0.6488 COMET, 0.1391 BLEU, 0.2762 ROUGE L, and 0.2383 METEOR. The results highlight the practical
value of inference engineering: careful scoring, ensembling, prompting, and cleanup can turn strong VLMs into
reliable competition systems.
Keywords
ImageCLEF, visual QA, VL
