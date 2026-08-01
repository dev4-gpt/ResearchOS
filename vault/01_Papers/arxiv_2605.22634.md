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
```obsidian
---
title: "Contractual Skills: A GovernSpec Design Framework for Enterprise AI Agents"
authors:
  - Ting Liu
url: "http://arxiv.org/abs/2605.22634v2"
publication_date: 2026-05-21
citations: 0
tags:
  - AI_Agents
  - Enterprise_AI
  - Skill_Design
  - GovernSpec
  - Governance
  - LLM_Evaluation
  - Prompt_Engineering
---

# Contractual Skills: A GovernSpec Design Framework for Enterprise AI Agents

## Overview and Problem Statement

This paper introduces [[Contractual Skills]], a [[GovernSpec]]-inspired design framework aimed at improving the clarity, reviewability, and governance of [[AI Agent]] skills in enterprise settings. While traditional skills package instructions, workflows, and resources, they often lack explicit mechanisms to define critical enterprise requirements such as input boundaries, permissions, human approval points, evidence requirements, output contracts, quality criteria, verification steps, and handoff rules. When these controls are expressed as informal prose, they become difficult to review, reuse, test, or connect to runtime guardrails.

The core contribution is organizing `SKILL.md` files as readable "task contracts" with structured fields, preserving lightweight skill discovery and progressive loading. The framework also clarifies the boundaries between [[Contractual Skills]] and other components like [[GovernSpec YAML Contracts]], [[Model Context Protocol (MCP)]] surfaces, [[Tool Adapters]], [[Runtime Guardrails]], [[Tracing]], and [[Evaluation Systems]].

The central claim is that [[Contractual Skills]] do not inherently make a model safe or replace runtime permission checks. Instead, their value lies in making the task contract explicit and reviewable, helping the model, maintainer, and evaluator align on requirements.

## Core Concepts and Framework

### Definition of Contractual Skills

A [[Contractual Skill]] is a `SKILL.md` file whose body is organized as a task contract, influenced by the principles of [[GovernSpec]]. It transforms a skill from a free-form prompt fragment into a structured, readable contract.

### Proposed Field Model for Enterprise Skills

The framework proposes the following sections/fields for organizing a `SKILL.md` file to act as a task contract:
*   `goal`
*   `audience`
*   `inputs`
*   `context`
*   `workflow`
*   `permissions`
*   `human gates`
*   `constraints`
*   `evidence`
*   `output`
*   `quality bar`
*   `verification`
*   `handoff`

### GovernSpec Design Framework Integration

*   **Relationship with [[GovernSpec YAML Contracts]]**: [[GovernSpec YAML]] is presented as a structured source of truth for AI task governance that can be validated and compiled. [[Contractual Skills]] are human-readable instruction artifacts directly loaded by agents. While they can be used independently, the strongest workflow is to derive high-risk skills from or align them with a [[GovernSpec YAML Contract]].
*   **Boundary Clarification**:
    *   **[[Model Context Protocol (MCP)]]**: MCP is a runtime-facing protocol surface for exposing prompts, resources, and tools. [[Contractual Skills]] are an instruction and governance surface, describing *when* to use MCP tools, *what* inputs are required, and *when* a call should be blocked or escalated.
    *   **[[Tool Adapters]] / [[Runtime Guardrails]]**: A [[Contractual Skill]] states what *should* happen (e.g., discount approval requires human confirmation). The tool adapter and guardrail *enforce* what *can* happen.
    *   **[[Tracing]]**: Tracing records model generations, tool calls, handoffs, guardrails, and custom events. [[Contractual Skills]] inform the expected behavior that tracing monitors.
    *   **[[Evaluation Systems]]**: [[Contractual Skills]] provide explicit criteria (`quality bar`, `verification`, `output`) that can be used for multidimensional evaluation, moving beyond simple accuracy scores.

### System Architecture

The paper describes [[Contractual Skills]] as a "governance layer" rather than a standalone safety mechanism. They act as an explicit set of instructions and acceptance criteria loaded by an agent, which can then interface with runtime systems like tool adapters and guardrails that enforce the policies described in the skill.

## Experimental Results

The framework was evaluated with three offline empirical studies.

### Study 1: Text Generation Experiment

*   **Objective**: Compare [[Contractual Skills]] against various baselines in text generation tasks.
*   **Dataset/Sample Size**:
    *   3 enterprise skills
    *   15 synthetic tasks
    *   4 instruction conditions (presumably `no-skill`, `minimal-skill`, `plain expanded skill`, `contractual skill`)
    *   8 generation models
    *   Produced 960 outputs
    *   Resulted in 1680 cross-judge score records
*   **Quantitative Benchmarks**:
    *   [[Contractual Skills]] received higher mean model-judge scores than the [[No-skill]] and [[Minimal-skill]] baselines across all eight models.
    *   Compared with a [[Plain expanded skill]] (containing similar information but lacking contract fields):
        *   [[Contractual Skills]] were slightly higher on six models.
        *   [[Contractual Skills]] were slightly lower on two models, with small differences.

### Study 2: Public-Skill A/B Expansion

*   **Objective**: Compare public skills with [[Contractual Rewrites]] across a larger set of tasks and models.
*   **Dataset/Sample Size**:
    *   8 public skills (compared with contractual rewrites)
    *   48 synthetic tasks
    *   6 generation models
    *   2 repeats per task/model
    *   Produced 1152 outputs
    *   Evaluated with 2 complete judge files
*   **Quantitative Benchmarks**:
    *   Mean quality increased from **4.692 to 4.914**.
    *   Critical-error rate reduced from **0.083 to 0.013**.

### Study 3: Offline Tool-Calling Challenge

*   **Objective**: Investigate the impact of skills, particularly [[Contractual Skills]], on high-risk tool attempts.
*   **Dataset/Sample Size**:
    *   8 models
    *   192 simulated tool-call records
*   **Key Findings**:
    *   Skills generally reduced high-risk tool attempts, but the effect varied by model.
    *   [[Contractual Skills]] do not replace tool-level guardrails.

### Code and Data Availability

The public replication package, including synthetic tasks, skill variants, prompts, model outputs, tool-calling transcripts, scoring records, analysis scripts, and reusable templates, is available at `SymbolicLight-AGI/contractual-skill`.

## Limitations

The authors explicitly acknowledge the following limitations:

*   [[Contractual Skills]] do not make a model inherently safe.
*   [[Contractual Skills]] do not replace runtime permission checks.
*   [[Contractual Skills]] do not replace tool-level guardrails.
*   They are best understood as a governance layer for making task intent, boundaries, and acceptance criteria explicit, rather than as a standalone safety mechanism.

## Mathematical Equations, Loss Functions, and Architecture Hyper-parameters

The provided text does not contain any explicit mathematical equations, loss functions, or exact architecture hyper-parameters for models. The paper focuses on a design framework and empirical evaluation of its impact on agent behavior and output quality.
```