---
title: "Language Models are Few-Shot Learners"
authors:
  - "Tom B. Brown"
  - "Benjamin Mann"
  - "Nick Ryder"
  - "Melanie Subbiah"
  - "Jared Kaplan"
  - "Prafulla Dhariwal"
  - "Arvind Neelakantan"
  - "Pranav Shyam"
  - "Girish Sastry"
  - "Amanda Askell"
  - "Sandhini Agarwal"
  - "Ariel Herbert-Voss"
  - "Gretchen Krueger"
  - "Tom Henighan"
  - "Rewon Child"
  - "Aditya Ramesh"
  - "Daniel M. Ziegler"
  - "Jeffrey Wu"
  - "Clemens Winter"
  - "Christopher Hesse"
  - "Mark Chen"
  - "Eric Sigler"
  - "Mateusz Litwin"
  - "Scott Gray"
  - "Benjamin Chess"
  - "Jack Clark"
  - "Christopher Berner"
  - "Sam McCandlish"
  - "Alec Radford"
  - "Ilya Sutskever"
  - "Dario Amodei"
url: "https://arxiv.org/abs/2005.14165"
published: "2020-05-28"
citations: "25400"
source: "arXiv & OpenAlex"
id: "arxiv:2005.14165"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "multimodal-alignment-in-vision-language-models:-contrastive-vs-generative"
---
# Language Models are Few-Shot Learners

**Authors**: Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, Dario Amodei
**Published**: 2020-05-28 | **Citations**: 25400 | **Source**: arXiv & OpenAlex
**URL**: https://arxiv.org/abs/2005.14165

## Executive Summary & Abstract
We demonstrate that scaling up language models greatly improves few-shot performance, sometimes even matching or exceeding prior state-of-the-art fine-tuning approaches. We train GPT-3, a 175-billion parameter autoregressive language model, and evaluate its performance on a wide variety of NLP tasks.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Language Models are Few-Shot Learners
Tom B. Brown∗ Benjamin Mann∗ Nick Ryder∗ Melanie Subbiah∗
Jared Kaplan† Prafulla Dhariwal Arvind Neelakantan Pranav Shyam Girish Sastry
Amanda Askell Sandhini Agarwal Ariel Herbert-Voss Gretchen Krueger Tom Henighan
Rewon Child Aditya Ramesh Daniel M. Ziegler Jeffrey Wu Clemens Winter
Christopher Hesse Mark Chen Eric Sigler Mateusz Litwin Scott Gray
Benjamin Chess Jack Clark Christopher Berner
Sam McCandlish Alec Radford Ilya Sutskever Dario Amodei
OpenAI
Abstract
Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training
on a large corpus of text followed by ﬁne-tuning on a speciﬁc task. While typically task-agnostic
in architecture, this method still requires task-speciﬁc ﬁne-tuning datasets of thousands or tens of
thousands of examples. By contrast, humans can generally perform a new language task from only
a few examples or from simple instructions – something which current NLP systems still largely
struggle to do. Here we show that scaling up language models greatly improves task-agnostic,
few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art ﬁnetuning approaches. Speciﬁcally, we train GPT-3, an autoregressive language model with 175 billion
parameters, 10x more than any previous non-sparse language model, and test its performance in
the few-shot setting. For all tasks, GPT-3 is applied without any gradient updates or ﬁne-tuning,
with tasks and few-shot demonstr
