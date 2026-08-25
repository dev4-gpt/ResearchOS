---
title: "The Impact of Fine-tuning Large Language Models on Automated Program Repair"
authors:
  - "Roman Macháček"
  - "Anastasiia Grishina"
  - "Max Hort"
  - "Leon Moonen"
url: "http://arxiv.org/abs/2507.19909v1"
published: "2025-07-26"
citations: "0"
source: "arXiv"
id: "arxiv:2507.19909"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# The Impact of Fine-tuning Large Language Models on Automated Program Repair

**Authors**: Roman Macháček, Anastasiia Grishina, Max Hort, Leon Moonen
**Published**: 2025-07-26 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2507.19909v1

## Abstract
Automated Program Repair (APR) uses various tools and techniques to help developers achieve functional and error-free code faster. In recent years, Large Language Models (LLMs) have gained popularity as components in APR tool chains because of their performance and flexibility. However, training such models requires a significant amount of resources. Fine-tuning techniques have been developed to adapt pre-trained LLMs to specific tasks, such as APR, and enhance their performance at far lower computational costs than training from scratch. In this study, we empirically investigate the impact of various fine-tuning techniques on the performance of LLMs used for APR. Our experiments provide insights into the performance of a selection of state-of-the-art LLMs pre-trained on code. The evaluation is done on three popular APR benchmarks (i.e., QuixBugs, Defects4J and HumanEval-Java) and considers six different LLMs with varying parameter sizes (resp. CodeGen, CodeT5, StarCoder, DeepSeekCoder, Bloom, and CodeLlama-2). We consider three training regimens: no fine-tuning, full fine-tuning, and parameter-efficient fine-tuning (PEFT) using LoRA and IA3. We observe that full fine-tuning techniques decrease the benchmarking performance of various models due to different data distributions and overfitting. By using parameter-efficient fine-tuning methods, we restrict models in the amount of trainable parameters and achieve better results. Keywords: large language models, automated program repair, parameter-efficient fine-tuning, AI4Code, AI4SE, ML4SE.
