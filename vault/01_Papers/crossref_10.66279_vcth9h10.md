---
title: "A Comparative Analysis of Contrastive and Generative Vision-Language Models for Zero-Shot Behavior Recognition in Surveillance Videos"
authors:
  - "Ayman Mohamed"
  - "Saeed Hamouda"
  - "Abdelrahman Elsayed"
  - "Mohamed M. Reda Ali"
url: "https://doi.org/10.66279/vcth9h10"
published: "2026-6-29"
citations: "0"
source: "Crossref"
id: "crossref:10.66279/vcth9h10"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "title:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target-venues:-cvpr-2026-workshop-/-ieee-tpami-core-research-question:-does-contrastive-alignment-(clip/siglip)-or-autoregressive-generative-alignment-(lmms/chameleon/llama-vision)-provide-superior-out-of-distribution-transferability-and-lower-hallucination-rates?-why-it's-high-impact:-resolves-the-central-architectural-debate-in-modern-multimodal-ai.-corpus-target:-25-papers"
---
# A Comparative Analysis of Contrastive and Generative Vision-Language Models for Zero-Shot Behavior Recognition in Surveillance Videos

**Authors**: Ayman Mohamed, Saeed Hamouda, Abdelrahman Elsayed, Mohamed M. Reda Ali
**Published**: 2026-6-29 | **Citations**: 0 | **Source**: Crossref
**URL**: https://doi.org/10.66279/vcth9h10

## Executive Summary & Abstract
Vision-language models (VLMs) have recently demonstrated strong zero-shot capability for object recognition and scene classification, yet their suitability for modeling covert human behaviors, such as theft, remains largely unexamined. This paper presents a case study comparing two zero-shot VLM paradigms for cashier theft detection in surveillance footage: a contrastive embedding model (CLIP) and a generative vision-language model (a Llama-3.2-11B-Vision-based pipeline operating in the BLIP/BLIP-2 family of generative architectures). On a set of real cashier-counter recordings, the contrastive model produced near-tied confidence scores between theft and normal-activity prompts (theft confidence 0.504, normal-activity confidence 0.496), indicating weak discriminative margin when intent and temporal context are required. The generative pipeline, in contrast, produced confident and structured binary outcomes (theft confidence 1.000, normal-activity confidence 0.000) accompanied by interpretable natural-language descriptions of the suspect and the event. These results, while drawn from a small, non-benchmarked sample rather than a large annotated corpus, suggest that contrastive similarity scoring is better suited to fast object-level screening, whereas generative reasoning is better suited to behavior-level interpretation. A hybrid pipeline that couples a fast contrastive pre-filter with a generative reasoning stage is proposed as a practical direction for zero-shot surveillance systems that require both efficiency and interpretability

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Vision-language models (VLMs) have recently demonstrated strong zero-shot capability for object recognition and scene classification, yet their suitability for modeling covert human behaviors, such as theft, remains largely unexamined. This paper presents a case study comparing two zero-shot VLM paradigms for cashier theft detection in surveillance footage: a contrastive embedding model (CLIP) and a generative vision-language model (a Llama-3.2-11B-Vision-based pipeline operating in the BLIP/BLIP-2 family of generative architectures). On a set of real cashier-counter recordings, the contrastive model produced near-tied confidence scores between theft and normal-activity prompts (theft confidence 0.504, normal-activity confidence 0.496), indicating weak discriminative margin when intent and temporal context are required. The generative pipeline, in contrast, produced confident and structured binary outcomes (theft confidence 1.000, normal-activity confidence 0.000) accompanied by interpretable natural-language descriptions of the suspect and the event. These results, while drawn from a small, non-benchmarked sample rather than a large annotated corpus, suggest that contrastive similarity scoring is better suited to fast object-level screening, whereas generative reasoning is better suited to behavior-level interpretation. A hybrid pipeline that couples a fast contrastive pre-filter with a generative reasoning stage is proposed as a practical direction for zero-shot surveillanc
