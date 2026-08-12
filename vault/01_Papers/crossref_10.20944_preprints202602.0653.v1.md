---
title: "Iterative Self-Questioning Supervision with Semantic Calibration for Stable Reasoning Chains in Large Language Models"
authors:
  - "Yaxuan Luan"
url: "https://doi.org/10.20944/preprints202602.0653.v1"
published: "2026-2-11"
citations: "3"
source: "Crossref"
id: "crossref:10.20944/preprints202602.0653.v1"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "self-correcting-reasoning-loops-in-mathematical-llms"
---
# Iterative Self-Questioning Supervision with Semantic Calibration for Stable Reasoning Chains in Large Language Models

**Authors**: Yaxuan Luan
**Published**: 2026-2-11 | **Citations**: 3 | **Source**: Crossref
**URL**: https://doi.org/10.20944/preprints202602.0653.v1

## Executive Summary & Abstract
This study addresses the inconsistency, semantic drift, and logical breaks that large language models often exhibit in complex reasoning tasks and proposes a unified cyclic self-questioning supervision framework that integrates information flow from questioning to reflection and renewed reasoning. The framework includes four core components, namely questioning generation, reflection modeling, semantic calibration, and renewed reasoning, and forms an iterative reasoning chain that allows the model to identify potential uncertainties and adjust its reasoning path based on internal feedback in each round. The method first uses the questioning module to produce structured queries about the initial reasoning result and to extract possible logical weaknesses from the generated content. The reflection module then interprets the questioning content, locates errors, and produces internal feedback signals that guide reasoning improvement. The semantic calibration mechanism converts the reflection output into intermediate states that influence the reasoning space and provide a more stable foundation for renewed reasoning. Through multiple iterations, the framework increases the internal consistency of the reasoning chain. Systematic experiments conducted on open reasoning datasets show significant gains in accuracy, explanation consistency, semantic alignment, and self-consistency, which confirms the importance of internal reflection and semantic calibration in improving reasoning quality. Sensitivity studies on learning rate, reflection length, reasoning temperature, and parallelism further reveal how the cyclic system depends on internal feedback absorption and semantic stability. The unified framework provides an extensible path for enhancing the structural quality of reasoning chains in large models and offers an interpretable foundation for high-reliability reasoning scenarios.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
This study addresses the inconsistency, semantic drift, and logical breaks that large language models often exhibit in complex reasoning tasks and proposes a unified cyclic self-questioning supervision framework that integrates information flow from questioning to reflection and renewed reasoning. The framework includes four core components, namely questioning generation, reflection modeling, semantic calibration, and renewed reasoning, and forms an iterative reasoning chain that allows the model to identify potential uncertainties and adjust its reasoning path based on internal feedback in each round. The method first uses the questioning module to produce structured queries about the initial reasoning result and to extract possible logical weaknesses from the generated content. The reflection module then interprets the questioning content, locates errors, and produces internal feedback signals that guide reasoning improvement. The semantic calibration mechanism converts the reflection output into intermediate states that influence the reasoning space and provide a more stable foundation for renewed reasoning. Through multiple iterations, the framework increases the internal consistency of the reasoning chain. Systematic experiments conducted on open reasoning datasets show significant gains in accuracy, explanation consistency, semantic alignment, and self-consistency, which confirms the importance of internal reflection and semantic calibration in improving reasoning quali
