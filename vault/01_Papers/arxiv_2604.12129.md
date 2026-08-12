---
title: "Aethon: A Reference-Based Replication Primitive for Constant-Time Instantiation of Stateful AI Agents"
authors:
  - "Swanand Rao"
  - "Kiran Kashalkar"
  - "Parvathi Somashekar"
  - "Priya Krishnan"
url: "http://arxiv.org/abs/2604.12129v1"
published: "2026-04-13"
citations: "0"
source: "arXiv"
id: "arxiv:2604.12129"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "enterprise-adoption-of-multi-agent-ai-systems:-infrastructure-architectures,-organizational-implementation,-and-labor-market-transformation"
---
# Aethon: A Reference-Based Replication Primitive for Constant-Time Instantiation of Stateful AI Agents

**Authors**: Swanand Rao, Kiran Kashalkar, Parvathi Somashekar, Priya Krishnan
**Published**: 2026-04-13 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2604.12129v1

## Executive Summary & Abstract
The transition from stateless model inference to stateful agentic execution is reshaping the systems assumptions underlying modern AI infrastructure. While large language models have made persistent, tool-using, and collaborative agents technically viable, existing runtime architectures remain constrained by materialization-heavy instantiation models that impose significant latency and memory overhead.   This paper introduces Aethon, a reference-based replication primitive for near-constant-time instantiation of stateful AI agents. Rather than reconstructing agents as fully materialized objects, Aethon represents each instance as a compositional view over stable definitions, layered memory, and local contextual overlays. By shifting instantiation from duplication to reference, Aethon decouples creation cost from inherited structure.   We present the conceptual framework, system architecture, and memory model underlying Aethon, including layered inheritance and copy-on-write semantics. We analyze its implications for complexity, scalability, multi-agent orchestration, and enterprise governance. We argue that reference-based instantiation is not merely an optimization, but a more appropriate systems abstraction for production-scale agentic software.   Aethon points toward a new class of AI infrastructure in which agents become lightweight, composable execution identities that can be spawned, specialized, and governed at scale.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Aethon: A Reference-Based Replication Primitive for
Constant-Time Instantiation of Stateful AI Agents
Swanand Rao, Kiran Kashalkar, Parvathi Somashekar, Priya Krishnan
Next Moca Global, Inc.
{swanand, kiran, paru, priya}@nextmoca.com
Abstract
The transition from stateless model inference to persistent
agent execution is beginning to reshape the systems assumptions that have governed applied artificial intelligence for
more than a decade. Modern AI agents [36] are expected to
do more than answer isolated prompts. They are expected to
preserve continuity across interactions, accumulate context,
invoke tools, collaborate with other components, and remain
operable inside production workflows.
As the capabilities of large language models [1, 2, 3] have
improved, these expectations have become technically plausible. What remains underdeveloped is the runtime substrate
required to create, manage, and scale such entities without
incurring severe latency, memory, and operational penalties.
This paper introduces Aethon, a reference-based replication
primitive for near-constant-time instantiation with respect to
inherited structure.
The central idea is that an instance should not be treated as
a fully materialized object that must be rebuilt from scratch
each time it is created. Instead, an instance can be represented
as a compositional view over a stable definition, layered memory, and local contextual overlays. By shifting instantiation
from duplication to reference, Aethon turns crea
