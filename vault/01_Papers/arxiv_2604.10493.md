---
title: "SWE-Shepherd: Advancing PRMs for Reinforcing Code Agents"
authors:
  - "Mahir Labib Dihan"
  - "Md Ashrafur Rahman Khan"
url: "http://arxiv.org/abs/2604.10493v1"
published: "2026-04-12"
citations: "0"
source: "arXiv"
id: "arxiv:2604.10493"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# SWE-Shepherd: Advancing PRMs for Reinforcing Code Agents

**Authors**: Mahir Labib Dihan, Md Ashrafur Rahman Khan
**Published**: 2026-04-12 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2604.10493v1

## Abstract
Automating real-world software engineering tasks remains challenging for large language model (LLM)-based agents due to the need for long-horizon reasoning over large, evolving codebases and making consistent decisions across interdependent actions. Existing approaches typically rely on static prompting strategies or handcrafted heuristics to select actions such as code editing, file navigation, and test execution, but they lack fine-grained feedback on intermediate decisions. This leads to inefficient exploration, error propagation, and brittle solution trajectories. To address this limitation, we propose SWE-Shepherd, a framework that introduces Process Reward Models (PRMs) to provide dense, step-level supervision for repository-level code agents. Using trajectories from SWE-Bench, we construct an action-level reward dataset and train a lightweight reward model on a base LLM to estimate the usefulness of intermediate actions. During inference, the PRM evaluates candidate actions and guides the agent toward higher-reward decisions without requiring full reinforcement learning. Experiments on SWE-Bench Verified demonstrate improved interaction efficiency and action quality, while also highlighting challenges in aligning intermediate rewards with final task success.
