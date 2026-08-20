---
title: "Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure"
authors:
  - "Krti Tallam"
url: "http://arxiv.org/abs/2605.05440v1"
published: "2026-05-06"
citations: "0"
source: "arXiv"
id: "arxiv:2605.05440"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "multi-agent-orchestration-security"
---
# Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure

**Authors**: Krti Tallam
**Published**: 2026-05-06 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2605.05440v1

## Executive Summary & Abstract
The security discussion around agentic AI focuses heavily on prompt injection. This paper argues that multi-agent systems also create a distinct authorization problem: maintaining authorization invariants as non-human principals retrieve data, delegate tasks, and synthesize results across changing boundaries. We call this problem authorization propagation. It is not reducible to prompt injection and is not fully addressed by classical access-control models such as RBAC, ABAC, or ReBAC. The paper formalizes authorization propagation as a workflow-level property, identifies three sub-problems (transitive delegation, aggregation inference, and temporal validity), and derives seven structural requirements for authorization architectures in multi-agent AI systems. Recent work on invocation-bound capability tokens, task-scoped authorization envelopes, dependency-graph policy enforcement, and execution-count revocation demonstrates that the field is converging on the problem, but not yet on a complete architecture. The central claim is that identity governance must be treated as infrastructure: evaluated continuously, enforced at every interaction boundary, and designed into the system before orchestration logic is allowed to scale. Preliminary implementation evidence from a production enterprise AI platform shows that ordinary system behavior, not only adversarial action, already produces the failures this model predicts.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Authorization Propagation in Multi-Agent AI Systems:
Identity Governance as Infrastructure
Krti Tallam
Kamiwaza AI
krti@kamiwaza.ai
May 2026
Abstract
The security discussion around agentic AI focuses heavily on prompt injection. This paper argues that multi-agent systems also create a distinct authorization problem: maintaining
authorization invariants as non-human principals retrieve data, delegate tasks, and synthesize
results across changing boundaries. We call this problemauthorization propagation. It is not
reducible to prompt injection and is not fully addressed by classical access-control models such
as RBAC, ABAC, or ReBAC. The paper formalizes authorization propagation as a workflowlevel property, identifies three sub-problems (transitive delegation, aggregation inference, and
temporal validity), and derives seven structural requirements for authorization architectures in
multi-agent AI systems. Recent work on invocation-bound capability tokens [Prakash, 2026],
task-scoped authorization envelopes [Sharma et al., 2026], dependency-graph policy enforcement
[Palumbo et al., 2026], and execution-count revocation [Parakhin, 2026] demonstrates that the
field is converging on the problem, but not yet on a complete architecture. The central claim is
that identity governance must be treated as infrastructure: evaluated continuously, enforced at
every interaction boundary, and designed into the system before orchestration logic is allowed
to scale. Preliminary implementation e
