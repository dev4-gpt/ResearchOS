---
title: "OmniEgo-R$^2$: A Routed Reasoning Framework for the 1st Cross-Domain EgoCross Challenge at CVPR 2026"
authors:
  - "Zixu Li"
  - "Zhiwei Chen"
  - "Zhiheng Fu"
  - "Wenbo Wang"
  - "Yupeng Hu"
  - "Weili Guan"
  - "Liqiang Nie"
url: "http://arxiv.org/abs/2605.24481v3"
published: "2026-05-23"
citations: "0"
source: "arXiv"
id: "arxiv:2605.24481"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "topic:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target:-cvpr-2026-workshop-on-multimodal-learning-+-arxiv-pre-print"
---
# OmniEgo-R$^2$: A Routed Reasoning Framework for the 1st Cross-Domain EgoCross Challenge at CVPR 2026

**Authors**: Zixu Li, Zhiwei Chen, Zhiheng Fu, Wenbo Wang, Yupeng Hu, Weili Guan, Liqiang Nie
**Published**: 2026-05-23 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2605.24481v3

## Executive Summary & Abstract
The 1st Cross-Domain EgoCross Challenge at EgoVis, CVPR 2026 evaluates whether multimodal large language models can reason over egocentric videos across surgery, industry, extreme sports, and animal perspective. We achieved second place in both the Source-Limited and Open-Source tracks. In this report, we formulate EgoCross as a robust cross-domain embodied video reasoning problem rather than a simple multiple-choice visual question answering task. We identify three key challenges: (C1) temporal boundary ambiguity, where critical state transitions are sparsely sampled and often occur between frames; (C2) cross-domain semantic granularity mismatch, where the same capability requires different domain-specific visual grammar; and (C3) decision instability under close options, where long multimodal reasoning can select unsupported distractors or produce malformed outputs. To address them, we propose OmniEgo-R$^2$ (Omnidomain Egocentric Routed Reasoning), a unified routed reasoning pipeline consisting of temporal-evidence normalization, domain-agnostic capability routing, structured perception--dynamics--decision reasoning, boundary-aware option verification, and defensive answer calibration. OmniEgo-R$^2$ uses the Qwen3-VL-4B-SFT checkpoints on each EgoCross domain as the visual-language backbone, and wraps them with lightweight test-time reasoning and parsing programs. Our final submissions obtain 66.35% overall accuracy in the Source-Limited track and 66.77% in the Open-Source track, ranking second in both leaderboards. The codes are available on https://github.com/Lee-zixu/OmniEgo-R2

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
OmniEgo-R2: A Routed Reasoning Framework for the 1st Cross-Domain
EgoCross Challenge at CVPR 2026
Zixu Li1 Zhiwei Chen1 Zhiheng Fu1 Wenbo Wang1 Yupeng Hu1 Weili Guan2 Liqiang Nie2
1Shandong University 2Harbin Institute of Technology (Shenzhen)
{lizixu.cs,zivczw,fuzhiheng8,honeyguan,nieliqiang}@gmail.com;
wangwenbo@mail.sdu.edu.cn,huyupeng@sdu.edu.cn
Abstract
The 1st Cross-Domain EgoCross Challenge at EgoVis,
CVPR 2026 evaluates whether multimodal large language
models can reason over egocentric videos across surgery,
industry, extreme sports, and animal perspective. We
achieved second place in both the Source-Limited and
Open-Source tracks. In this report, we formulate EgoCross
as a robust cross-domain embodied video reasoning problem rather than a simple multiple-choice visual question
answering task. We identify three key challenges: (C1)
temporal boundary ambiguity, where critical state transitions are sparsely sampled and often occur between frames;
(C2) cross-domain semantic granularity mismatch, where
the same capability requires different domain-specific visual grammar; and (C3) decision instability under close
options, where long multimodal reasoning can select unsupported distractors or produce malformed outputs. To
address them, we propose OmniEgo-R 2 (Omnidomain
EgocentricRoutedReasoning), a unified routed reasoning pipeline consisting of temporal-evidence normalization,
domain-agnostic capability routing, structured perception–
dynamics–decision reasoning, boundar
