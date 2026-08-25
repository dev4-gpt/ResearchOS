---
title: "Empirical Evaluation of Large Language Models in Automated Program Repair"
authors:
  - "Jiajun Sun"
  - "Fengjie Li"
  - "Xinzhu Qi"
  - "Hongyu Zhang"
  - "Jiajun Jiang"
url: "http://arxiv.org/abs/2506.13186v1"
published: "2025-06-16"
citations: "0"
source: "arXiv"
id: "arxiv:2506.13186"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Empirical Evaluation of Large Language Models in Automated Program Repair

**Authors**: Jiajun Sun, Fengjie Li, Xinzhu Qi, Hongyu Zhang, Jiajun Jiang
**Published**: 2025-06-16 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2506.13186v1

## Abstract
The increasing prevalence of software bugs has made automated program repair (APR) a key research focus. Large language models (LLMs) offer new opportunities for APR, but existing studies mostly rely on smaller, earlier-generation models and Java benchmarks. The repair capabilities of modern, large-scale LLMs across diverse languages and scenarios remain underexplored. To address this, we conduct a comprehensive empirical study of four open-source LLMs, CodeLlama, LLaMA, StarCoder, and DeepSeek-Coder, spanning 7B to 33B parameters, diverse architectures, and purposes. We evaluate them across two bug scenarios (enterprise-grades and algorithmic), three languages (Java, C/C++, Python), and four prompting strategies, analyzing over 600K generated patches on six benchmarks. Key findings include: (1) model specialization (e.g., CodeLlama) can outperform larger general-purpose models (e.g., LLaMA); (2) repair performance does not scale linearly with model size; (3) correct patches often appear early in generation; and (4) prompts significantly affect results. These insights offer practical guidance for designing effective and efficient LLM-based APR systems.
