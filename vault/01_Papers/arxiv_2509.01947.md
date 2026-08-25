---
title: "Automated Repair of C Programs Using Large Language Models"
authors:
  - "Mahdi Farzandway"
  - "Fatemeh Ghassemi"
url: "http://arxiv.org/abs/2509.01947v1"
published: "2025-09-02"
citations: "0"
source: "arXiv"
id: "arxiv:2509.01947"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Automated Repair of C Programs Using Large Language Models

**Authors**: Mahdi Farzandway, Fatemeh Ghassemi
**Published**: 2025-09-02 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2509.01947v1

## Abstract
This study explores the potential of Large Language Models (LLMs) in automating the repair of C programs. We present a framework that integrates spectrum-based fault localization (SBFL), runtime feedback, and Chain-of-Thought-structured prompting into an autonomous repair loop. Unlike prior approaches, our method explicitly combines statistical program analysis with LLM reasoning. The iterative repair cycle leverages a structured Chain-of-Thought (CoT) prompting approach, where the model reasons over failing tests, suspicious code regions, and prior patch outcomes, before generating new candidate patches. The model iteratively changes the code, evaluates the results, and incorporates reasoning from previous attempts into subsequent modifications, reducing repeated errors and clarifying why some bugs remain unresolved. Our evaluation spans 3,902 bugs from the Codeflaws benchmark, where our approach achieves 44.93% repair accuracy, representing a 3.61% absolute improvement over strong state-of-the-art APR baselines such as GPT-4 with CoT. This outcome highlights a practical pathway toward integrating statistical program analysis with generative AI in automated debugging.
