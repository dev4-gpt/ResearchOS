---
title: "Diffusion On Syntax Trees For Program Synthesis"
authors:
  - "Shreyas Kapur"
  - "Erik Jenner"
  - "Stuart Russell"
url: "http://arxiv.org/abs/2405.20519v1"
published: "2024-05-30"
citations: "0"
source: "arXiv"
id: "arxiv:2405.20519"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Diffusion On Syntax Trees For Program Synthesis

**Authors**: Shreyas Kapur, Erik Jenner, Stuart Russell
**Published**: 2024-05-30 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2405.20519v1

## Abstract
Large language models generate code one token at a time. Their autoregressive generation process lacks the feedback of observing the program's output. Training LLMs to suggest edits directly can be challenging due to the scarcity of rich edit data. To address these problems, we propose neural diffusion models that operate on syntax trees of any context-free grammar. Similar to image diffusion models, our method also inverts ``noise'' applied to syntax trees. Rather than generating code sequentially, we iteratively edit it while preserving syntactic validity, which makes it easy to combine this neural model with search. We apply our approach to inverse graphics tasks, where our model learns to convert images into programs that produce those images. Combined with search, our model is able to write graphics programs, see the execution result, and debug them to meet the required specifications. We additionally show how our system can write graphics programs for hand-drawn sketches.
