---
title: "Queen-Bee Agents: A BeeSpec-Centered Architecture for Governed Enterprise MCP Orchestration"
authors:
  - "Dutao Zhang"
  - "Liaotian"
url: "http://arxiv.org/abs/2606.06545v1"
published: "2026-06-04"
citations: "0"
source: "arXiv"
id: "arxiv:2606.06545"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
# Queen-Bee Agents: A BeeSpec-Centered Architecture for Governed Enterprise MCP Orchestration

**Authors**: Dutao Zhang, Liaotian
**Published**: 2026-06-04 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2606.06545v1

## Executive Summary & Abstract
Enterprise agent systems increasingly need to connect large language models to private tools, internal knowledge, and Model Context Protocol (MCP) interfaces. In this setting, raw task capability is insufficient: organizations also require policy enforcement, tenant-scoped isolation, and execution that remains within explicit operational boundaries. We present Queen-Bee, a governed multi-agent architecture in which a Queen control plane retrieves capabilities, plans task-scoped execution, and compiles a structured BeeSpec that is executed by specialized Bee agents under constrained tool access. We implement a working prototype with tenant-scoped MCP connectors, audit-backed execution-time governance, retrieval-driven weak incubation, and multiple provisioning backends. We evaluate the system on 59 enterprise-style tasks spanning governance-sensitive requests, retrieval-driven provisioning, scoped local execution, and chemistry workflow integration. The retrieval-driven Queen-Bee variant achieves a task success rate of 0.964, zero governance failures, and substantially better scoped execution quality than both a static Queen-Bee baseline and a permissive single-agent baseline. We further show a multi-Bee chemistry workflow with explicit approval gating and a concrete top-3 shortlist grounded in real upstream evidence and screening artifacts. Additional comparisons with hybrid retrieval and LLM-guided provisioning show that richer provisioning backends are viable but do not outperform the lightweight structured retriever on the current small, highly structured capability registry. The results provide prototype-level systems evidence rather than a production deployment study, and suggest that enterprise agent platforms should be evaluated not only by capability, but also by governed provisioning, isolation behavior, scoped execution quality, and artifact-aware workflow coordination.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Queen-Bee Agents: A BeeSpec-Centered Architecture for Governed
Enterprise MCP Orchestration
Dutao Zhang ∗and Liaotian
Macao Polytechnic University
p2527418@mpu.edu.mo
Technical Report / arXiv Preprint
Abstract
Enterprise agent systems increasingly need to connect large language models to private tools,
internal knowledge, and Model Context Protocol (MCP) interfaces. In this setting, raw task
capability is insufficient: organizations also require policy enforcement, tenant-scoped isolation,
and execution that remains within explicit operational boundaries. We presentQueen-Bee, a
governed multi-agent architecture in which a Queen control plane retrieves capabilities, plans
task-scoped execution, and compiles a structuredBeeSpecthat is executed by specialized Bee
agents under constrained tool access. We implement a working prototype with tenant-scoped
MCP connectors, audit-backed execution-time governance, retrieval-driven weak incubation, and
multiple provisioning backends. We evaluate the system on 59 enterprise-style tasks spanning
governance-sensitive requests, retrieval-driven provisioning, scoped local execution, and chemistry
workflow integration. The retrieval-driven Queen-Bee variant achieves a task success rate of
0.964, zero governance failures, and substantially better scoped execution quality than both a
static Queen-Bee baseline and a permissive single-agent baseline. We further show a multi-Bee
chemistry workflow with explicit approval gating and a concrete top-3 
