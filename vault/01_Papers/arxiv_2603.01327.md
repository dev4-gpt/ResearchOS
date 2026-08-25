---
title: "SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution"
authors:
  - "Kang He"
  - "Kaushik Roy"
url: "http://arxiv.org/abs/2603.01327v2"
published: "2026-03-01"
citations: "0"
source: "arXiv"
id: "arxiv:2603.01327"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution

**Authors**: Kang He, Kaushik Roy
**Published**: 2026-03-01 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2603.01327v2

## Abstract
Large language models (LLMs) exhibit strong performance on self-contained programming tasks. However, they still struggle with repository-level software engineering (SWE), which demands (1) deep codebase navigation with effective context management for accurate localization, and (2) systematic approaches for iterative, test-driven code modification to resolve issues. To address these challenges, we propose SWE-Adept, an LLM-based two-agent framework where a localization agent identifies issue-relevant code locations and a resolution agent implements the corresponding fixes. For issue localization, we introduce agent-directed depth-first search that selectively traverses code dependencies. This minimizes issue-irrelevant content in the agent's context window and improves localization accuracy. For issue resolution, we employ adaptive planning and structured problem solving. We equip the agent with specialized tools for progress tracking and Git-based version control. These tools interface with a shared working memory that stores code-state checkpoints indexed by execution steps, facilitating precise checkpoint retrieval. This design enables reliable agent-driven version-control operations for systematic issue resolution, including branching to explore alternative solutions and reverting failed edits. Experiments on SWE-Bench Lite and SWE-Bench Pro demonstrate that SWE-Adept consistently outperforms prior approaches in both issue localization and resolution, improving the end-to-end resolve rate by up to 4.3%.
