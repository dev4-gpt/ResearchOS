---
title: "Leveraging large language models for data analysis automation"
authors:
  - "Jacqueline A Jansen"
  - "Artür Manukyan"
  - "Nour Al Khoury"
  - "Altuna Akalin"
url: "https://doi.org/10.1371/journal.pone.0317084"
published: "2025-02-21"
citations: "0"
source: "PLOS"
id: "plos:10.1371/journal.pone.0317084"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "self-correcting-reasoning-loops-in-mathematical-llms"
---
# Leveraging large language models for data analysis automation

**Authors**: Jacqueline A Jansen, Artür Manukyan, Nour Al Khoury, Altuna Akalin
**Published**: 2025-02-21 | **Citations**: 0 | **Source**: PLOS
**URL**: https://doi.org/10.1371/journal.pone.0317084

## Executive Summary & Abstract

Data analysis is constrained by a shortage of skilled experts, particularly in biology, where detailed data analysis and subsequent interpretation is vital for understanding complex biological processes and developing new treatments and diagnostics. One possible solution to this shortage in experts would be making use of Large Language Models (LLMs) for generating data analysis pipelines. However, although LLMs have shown great potential when used for code generation tasks, questions regarding the accuracy of LLMs when prompted with domain expert questions such as omics related data analysis questions, remain unanswered. To address this, we developed mergen, an R package that leverages LLMs for data analysis code generation and execution. We evaluated the performance of this data analysis system using various data analysis tasks for genomics. Our primary goal is to enable researchers to conduct data analysis by simply describing their objectives and the desired analyses for specific datasets through clear text. Our approach improves code generation via specialized prompt engineering and error feedback mechanisms. In addition, our system can execute the data analysis workflows prescribed by the LLM providing the results of the data analysis workflow for human review. Our evaluation of this system reveals that while LLMs effectively generate code for some data analysis tasks, challenges remain in executable code generation, especially for complex data analysis tasks. The best performance was seen with the self-correction mechanism, in which self-correct was able to increase the percentage of executable code when compared to the simple strategy by 22.5% for tasks of complexity 2. For tasks for complexity 3, 4 and 5, this increase was 52.5%, 27.5% and 15% respectively. Using a chi-squared test, it was shown that significant differences could be found using the different prompting strategies. Our study contributes to a better understanding of LLM capabilities and limitations, providing software infrastructure and practical insights for their effective integration into data analysis workflows.


## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet

Data analysis is constrained by a shortage of skilled experts, particularly in biology, where detailed data analysis and subsequent interpretation is vital for understanding complex biological processes and developing new treatments and diagnostics. One possible solution to this shortage in experts would be making use of Large Language Models (LLMs) for generating data analysis pipelines. However, although LLMs have shown great potential when used for code generation tasks, questions regarding the accuracy of LLMs when prompted with domain expert questions such as omics related data analysis questions, remain unanswered. To address this, we developed mergen, an R package that leverages LLMs for data analysis code generation and execution. We evaluated the performance of this data analysis system using various data analysis tasks for genomics. Our primary goal is to enable researchers to conduct data analysis by simply describing their objectives and the desired analyses for specific datasets through clear text. Our approach improves code generation via specialized prompt engineering and error feedback mechanisms. In addition, our system can execute the data analysis workflows prescribed by the LLM providing the results of the data analysis workflow for human review. Our evaluation of this system reveals that while LLMs effectively generate code for some data analysis tasks, challenges remain in executable code generation, especially for complex data analysis tasks. The best 
