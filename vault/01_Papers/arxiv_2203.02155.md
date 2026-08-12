---
title: "Training language models to follow instructions with human feedback"
authors:
  - "Long Ouyang"
  - "Jeff Wu"
  - "Xu Jiang"
  - "Diogo Almeida"
  - "Carroll L. Wainwright"
  - "Pamela Mishkin"
  - "Chong Zhang"
  - "Sandhini Agarwal"
  - "Katarina Slama"
  - "Alex Ray"
  - "John Schulman"
  - "Jacob Hilton"
  - "Fraser Kelton"
  - "Luke Miller"
  - "Maddie Simens"
  - "Amanda Askell"
  - "Peter Welinder"
  - "Paul Christiano"
  - "Jan Leike"
  - "Ryan Lowe"
url: "https://arxiv.org/abs/2203.02155"
published: "2022-03-04"
citations: "4350"
source: "arXiv & OpenAlex"
id: "arxiv:2203.02155"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "multimodal-alignment-in-vision-language-models:-contrastive-vs-generative"
---
# Training language models to follow instructions with human feedback

**Authors**: Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe
**Published**: 2022-03-04 | **Citations**: 4350 | **Source**: arXiv & OpenAlex
**URL**: https://arxiv.org/abs/2203.02155

## Executive Summary & Abstract
We show how to fine-tune language models on a wide range of tasks to align them with user intent. By using reinforcement learning from human feedback (RLHF), we fine-tune GPT-3 to follow instructions. We call the resulting models InstructGPT.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Training language models to follow instructions
with human feedback
Long Ouyang∗ Jeff Wu∗ Xu Jiang∗ Diogo Almeida∗ Carroll L. Wainwright∗
Pamela Mishkin∗ Chong Zhang Sandhini Agarwal Katarina Slama Alex Ray
John Schulman Jacob Hilton Fraser Kelton Luke Miller Maddie Simens
Amanda Askell† Peter Welinder Paul Christiano ∗†
Jan Leike∗ Ryan Lowe∗
OpenAI
Abstract
Making language models bigger does not inherently make them better at following
a user’s intent. For example, large language models can generate outputs that
are untruthful, toxic, or simply not helpful to the user. In other words, these
models are not aligned with their users. In this paper, we show an avenue for
aligning language models with user intent on a wide range of tasks by ﬁne-tuning
with human feedback. Starting with a set of labeler-written prompts and prompts
submitted through the OpenAI API, we collect a dataset of labeler demonstrations
of the desired model behavior, which we use to ﬁne-tune GPT-3 using supervised
learning. We then collect a dataset of rankings of model outputs, which we use to
further ﬁne-tune this supervised model using reinforcement learning from human
feedback. We call the resulting models InstructGPT. In human evaluations on
our prompt distribution, outputs from the 1.3B parameter InstructGPT model are
preferred to outputs from the 175B GPT-3, despite having 100x fewer parameters.
Moreover, InstructGPT models show improvements in truthfulness and reductions
in toxic output generation w
