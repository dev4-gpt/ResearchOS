---
title: "Automated C/C++ Program Repair for High-Level Synthesis via Large Language Models"
authors:
  - "Kangwei Xu"
  - "Grace Li Zhang"
  - "Xunzhao Yin"
  - "Cheng Zhuo"
  - "Ulf Schlichtmann"
  - "Bing Li"
url: "http://arxiv.org/abs/2407.03889v1"
published: "2024-07-04"
citations: "0"
source: "arXiv"
id: "arxiv:2407.03889"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Automated C/C++ Program Repair for High-Level Synthesis via Large Language Models

**Authors**: Kangwei Xu, Grace Li Zhang, Xunzhao Yin, Cheng Zhuo, Ulf Schlichtmann, Bing Li
**Published**: 2024-07-04 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2407.03889v1

## Abstract
In High-Level Synthesis (HLS), converting a regular C/C++ program into its HLS-compatible counterpart (HLS-C) still requires tremendous manual effort. Various program scripts have been introduced to automate this process. But the resulting codes usually contain many issues that should be manually repaired by developers. Since Large Language Models (LLMs) have the ability to automate code generation, they can also be used for automated program repair in HLS. However, due to the limited training of LLMs considering hardware and software simultaneously, hallucinations may occur during program repair using LLMs, leading to compilation failures. Besides, using LLMs for iterative repair also incurs a high cost. To address these challenges, we propose an LLM-driven program repair framework that takes regular C/C++ code as input and automatically generates its corresponding HLS-C code for synthesis while minimizing human repair effort. To mitigate the hallucinations in LLMs and enhance the prompt quality, a Retrieval-Augmented Generation (RAG) paradigm is introduced to guide the LLMs toward correct repair. In addition, we use LLMs to create a static bit width optimization program to identify the optimized bit widths for variables. Moreover, LLM-driven HLS optimization strategies are introduced to add/tune pragmas in HLS-C programs for circuit optimization. Experimental results demonstrate that the proposed LLM-driven automated framework can achieve much higher repair pass rates in 24 real-world applications compared with the traditional scripts and the direct application of LLMs for program repair.
