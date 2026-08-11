---
title: "Contractual Skills: A GovernSpec Design Framework for Enterprise AI Agents"
authors:
  - "Ting Liu"
url: "http://arxiv.org/abs/2605.22634v2"
published: "2026-05-21"
citations: "0"
source: "arXiv"
id: "arxiv:2605.22634"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
# Contractual Skills: A GovernSpec Design Framework for Enterprise AI Agents

**Authors**: Ting Liu
**Published**: 2026-05-21 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2605.22634v2

## Executive Summary & Abstract
Skills have become a practical packaging mechanism for agent instructions, workflows, scripts, and reference materials. In enterprise settings, however, a skill often needs to express more than task guidance: goals, input boundaries, permissions, human approval points, evidence requirements, output contracts, quality criteria, verification steps, and handoff rules. This paper proposes contractual skills, a GovernSpec-inspired design framework for organizing SKILL.md files as readable task contracts while preserving lightweight skill discovery and progressive loading. The framework clarifies the boundary between contractual skills, GovernSpec YAML contracts, Model Context Protocol (MCP) surfaces, tool adapters, runtime guardrails, tracing, and evaluation systems.   We evaluate the framework with three offline empirical studies. The first text-generation experiment covers three enterprise skills, fifteen synthetic tasks, four instruction conditions, and eight generation models, producing 960 outputs and 1680 cross-judge score records. The second study is a public-skill A/B expansion: eight public skills are compared with contractual rewrites across forty-eight synthetic tasks, six generation models, two repeats, 1152 outputs, and two complete judge files. In this setting, contractual skills raise mean quality from 4.692 to 4.914 and reduce critical-error rate from 0.083 to 0.013. The third study is an offline tool-calling challenge with eight models and 192 simulated tool-call records. The results suggest that contractual skills are best understood as a governance layer that makes task intent, boundaries, and acceptance criteria explicit, not as a standalone safety mechanism.

## Methodological Insights & System Architectures

## Key Quantitative Findings & Benchmarks

## Content Snippet
Contractual Skills: A GovernSpec Design Framework for Enterprise
AI Agents
Ting Liu
SymbolicLight Research
Foshan, Guangdong, China
research@symboliclight.com
May 2026
Abstract
Skills have become a practical packaging mechanism for agent instructions, workflows, scripts,
and reference materials. In enterprise settings, however, a skill is often expected to do more than
trigger relevant context. It must also express input boundaries, permissions, human approval
points, evidence requirements, output contracts, quality criteria, verification steps, and handoff
rules. When these controls are written as informal prose, they are diﬀicult to review, reuse, test,
or connect to runtime guardrails. This paper proposes contractual skills , a design framework
that organizes SKILL.md files with GovernSpec-style task contract fields while preserving the
lightweight discovery and progressive-loading properties of skills. The framework positions a
skill as a readable task contract rather than as a free-form prompt fragment. It also clarifies
the boundary between contractual skills, GovernSpec YAML contracts, Model Context Protocol
(MCP) surfaces, tool adapters, runtime guardrails, tracing, and evaluation systems.
We evaluate the framework with three offline empirical studies. The first text-generation
experiment covers three enterprise skills, fifteen synthetic tasks, four instruction conditions, and
eight generation models, producing 960 outputs and 1680 cross-judge score records. Contractu