---
title: "Assessing the Latent Automated Program Repair Capabilities of Large Language Models using Round-Trip Translation"
authors:
  - "Fernando Vallecillos Ruiz"
  - "Anastasiia Grishina"
  - "Max Hort"
  - "Leon Moonen"
url: "http://arxiv.org/abs/2401.07994v2"
published: "2024-01-15"
citations: "0"
source: "arXiv"
id: "arxiv:2401.07994"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Assessing the Latent Automated Program Repair Capabilities of Large Language Models using Round-Trip Translation

**Authors**: Fernando Vallecillos Ruiz, Anastasiia Grishina, Max Hort, Leon Moonen
**Published**: 2024-01-15 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2401.07994v2

## Abstract
Research shows that errors in natural language can be corrected by translating texts to another language and back using language models. We explore to what extent this latent correction capability extends to Automated Program Repair (APR) by investigating Round-Trip Translation (RTT): translating code from one programming language into another programming or natural language and back, using Large Language Models (LLMs). We hypothesize that RTT restores patterns most commonly seen in the LLM's training corpora through regression toward the mean, replacing infrequent bugs with more frequent, natural, bug-free code. To test this hypothesis, we employ nine LLMs and four common APR benchmarks in Java, and perform a detailed quantitative and qualitative analysis of RTT-generated patches. We find that RTT through English generates plausible patches for 100 of 164 bugs with GPT-4 on the HumanEval-Java benchmark, and 97 are found to be correct in our manual assessment. Moreover, RTT uniquely generates plausible patches for 46 bugs that were missed by LLMs specifically fine-tuned for APR. While this demonstrates the viability of RTT for APR, we also observe limitations, such as a lower overall bug fix rate than the state-of-the-art and diluting the original coding style. We analyze the impact of these limitations and discuss the potential of using RTT as a complementary component in APR frameworks. A replication package is available for download from https://doi.org/10.5281/zenodo.10500593. Keywords: automated program repair, large language model, machine translation
