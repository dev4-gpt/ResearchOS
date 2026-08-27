---
title: "Saving SWE-Bench: A Benchmark Mutation Approach for Realistic Agent Evaluation"
authors:
  - "Spandan Garg"
  - "Benjamin Steenhoek"
  - "Yufan Huang"
url: "http://arxiv.org/abs/2510.08996v4"
published: "2025-10-10"
citations: "0"
source: "arXiv"
id: "arxiv:2510.08996"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# Saving SWE-Bench: A Benchmark Mutation Approach for Realistic Agent Evaluation

**Authors**: Spandan Garg, Benjamin Steenhoek, Yufan Huang
**Published**: 2025-10-10 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2510.08996v4

## Abstract
Current benchmarks for evaluating software engineering agents, such as SWE-Bench Verified, are predominantly derived from GitHub issues and fail to accurately reflect how developers interact with chat-based coding assistants in integrated development environments (IDEs). We posit that this mismatch leads to a systematic overestimation of agent's capabilities in real-world scenarios, especially bug fixing. We introduce a novel benchmarking framework that transforms existing formal benchmarks into realistic user queries through systematic analysis of developer interaction patterns with chat-based agents. Our methodology is flexible and can be easily extended to existing benchmarks. In this paper, we apply our testing framework to SWE-Bench Verified, the TypeScript subset of Multi-SWE-Bench and a private benchmark, SWE-Bench C# and transform formal GitHub issue descriptions into realistic user-style queries based on telemetry analysis of a popular chat-based agent interactions. Our findings reveal that existing benchmarks significantly overestimate agent capabilities for some models by >50% over baseline performance for public benchmarks and ~10-16% for our internal benchmark. This work establishes a new paradigm for evaluating interactive chat-based software engineering agents through benchmark mutation techniques.
