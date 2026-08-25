---
title: "Learning From Failure: Integrating Negative Examples when Fine-tuning Large Language Models as Agents"
authors:
  - "Renxi Wang"
  - "Haonan Li"
  - "Xudong Han"
  - "Yixuan Zhang"
  - "Timothy Baldwin"
url: "http://arxiv.org/abs/2402.11651v2"
published: "2024-02-18"
citations: "0"
source: "arXiv"
id: "arxiv:2402.11651"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Learning From Failure: Integrating Negative Examples when Fine-tuning Large Language Models as Agents

**Authors**: Renxi Wang, Haonan Li, Xudong Han, Yixuan Zhang, Timothy Baldwin
**Published**: 2024-02-18 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2402.11651v2

## Abstract
Large language models (LLMs) have achieved success in acting as agents, which interact with environments through tools such as search engines. However, LLMs are optimized for language generation instead of tool use during training or alignment, limiting their effectiveness as agents. To resolve this problem, previous work has first collected interaction trajectories between LLMs and environments, using only trajectories that successfully finished the task to fine-tune smaller models, making fine-tuning data scarce and acquiring it both difficult and costly. Discarding failed trajectories also leads to significant wastage of data and resources and limits the possible optimization paths during fine-tuning. In this paper, we argue that unsuccessful trajectories offer valuable insights, and LLMs can learn from these trajectories through appropriate quality control and fine-tuning strategies. By simply adding a prefix or suffix that tells the model whether to generate a successful trajectory during training, we improve model performance by a large margin on mathematical reasoning, multi-hop question answering, and strategic question answering tasks. We further analyze the inference results and find that our method provides a better trade-off between valuable information and errors in unsuccessful trajectories. To our knowledge, we are the first to demonstrate the value of negative trajectories and their application in agent-tunning scenarios. Our findings offer guidance for developing better agent-tuning methods and low-resource data usage techniques.
