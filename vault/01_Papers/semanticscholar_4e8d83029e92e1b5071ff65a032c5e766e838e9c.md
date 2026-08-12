---
title: "Unlocking Reasoning Capability on Machine Translation in Large Language Models"
authors:
  - "Sara Rajaee"
  - "Sebastian Vincent"
  - "Alexandre Berard"
  - "Marzieh Fadaee"
  - "Kelly Marchisio"
  - "Tom Kocmi"
url: "https://www.semanticscholar.org/paper/4e8d83029e92e1b5071ff65a032c5e766e838e9c"
published: "2026-02-16"
citations: "1"
source: "Semantic Scholar"
id: "semanticscholar:4e8d83029e92e1b5071ff65a032c5e766e838e9c"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "self-correcting-reasoning-loops-in-mathematical-llms"
---
# Unlocking Reasoning Capability on Machine Translation in Large Language Models

**Authors**: Sara Rajaee, Sebastian Vincent, Alexandre Berard, Marzieh Fadaee, Kelly Marchisio, Tom Kocmi
**Published**: 2026-02-16 | **Citations**: 1 | **Source**: Semantic Scholar
**URL**: https://www.semanticscholar.org/paper/4e8d83029e92e1b5071ff65a032c5e766e838e9c

## Executive Summary & Abstract
Reasoning-oriented large language models (RLMs) achieve strong gains on tasks such as mathematics and coding by generating explicit intermediate reasoning. However, their impact on machine translation (MT) remains underexplored. We systematically evaluate several open- and closed-weights RLMs on the WMT24++ benchmark and find that enabling explicit reasoning consistently degrades translation quality across languages and models. Analysis reveals that MT reasoning traces are highly linear, lacking revision, self-correction and exploration of alternative translations, which limits their usefulness. Furthermore, injecting higher-quality reasoning traces from stronger models does not reliably improve weaker models'performance. To address this mismatch, we propose a structured reasoning framework tailored to translation, based on multi-step drafting, adequacy refinement, fluency improvement, and selective iterative revision. We curate a synthetic dataset of dynamic structured reasoning traces and post-train a large reasoning model on this data. Experiments show significant improvements over standard translation fine-tuning and injected generic reasoning baselines. Our findings demonstrate that reasoning must be task-structured to benefit MT.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Reasoning-oriented large language models (RLMs) achieve strong gains on tasks such as mathematics and coding by generating explicit intermediate reasoning. However, their impact on machine translation (MT) remains underexplored. We systematically evaluate several open- and closed-weights RLMs on the WMT24++ benchmark and find that enabling explicit reasoning consistently degrades translation quality across languages and models. Analysis reveals that MT reasoning traces are highly linear, lacking revision, self-correction and exploration of alternative translations, which limits their usefulness. Furthermore, injecting higher-quality reasoning traces from stronger models does not reliably improve weaker models'performance. To address this mismatch, we propose a structured reasoning framework tailored to translation, based on multi-step drafting, adequacy refinement, fluency improvement, and selective iterative revision. We curate a synthetic dataset of dynamic structured reasoning traces and post-train a large reasoning model on this data. Experiments show significant improvements over standard translation fine-tuning and injected generic reasoning baselines. Our findings demonstrate that reasoning must be task-structured to benefit MT.
