---
title: "Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use"
authors:
  - "Ziling Zhou"
url: "http://arxiv.org/abs/2603.14332v2"
published: "2026-03-15"
citations: "0"
source: "arXiv"
id: "arxiv:2603.14332"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "multi-agent-orchestration-security"
---
# Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use

**Authors**: Ziling Zhou
**Published**: 2026-03-15 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2603.14332v2

## Executive Summary & Abstract
AI agents dynamically acquire tools, orchestrate sub-agents, and transact across organizational boundaries, yet no existing security layer verifies what an agent can do, whether it executed what it claims, or what happened in a multi-agent interaction. We trace this gap to the capability-context separation: inside a transformer, tool definitions and user context are indistinguishable tokens, but at the orchestration layer they have fundamentally different security semantics. Existing frameworks conflate the two, enabling silent capability escalation and leaving interactions without verifiable provenance.   From this principle we derive three Agent Governance Requirements: capability integrity (G1), behavioral verifiability (G2), and interaction auditability (G3), defining what a governed agent ecosystem must enforce, independent of how. We prove two structural results: the Chain Verifiability Theorem (one unverifiable interior agent breaks end-to-end verification for all downstream nodes) and the Bounded Divergence Theorem (replay-based verification yields a probabilistic safety certificate, epsilon <= 1 - alpha^{1/n}). We validate with two crypto-agnostic instantiations -- basic (Ed25519, SHA-256; 97 us verify) and enhanced (BBS+ selective disclosure, Groth16 DV-SNARK; 13.8 ms) -- both satisfying nine security properties. A reproducibility study (9 models, 7 providers) reveals 5.8x variance in inference determinism, connecting model characteristics to governance architecture. End-to-end evaluation over 5-20 agent pipelines confirms <0.02% overhead and detection of all attack scenarios with zero false positives.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Governing Dynamic Capabilities: Cryptographic Binding
and
Reproducibility Verification for AI Agent Tool Use
Ziling Zhou
Genupixel Technology Pte. Ltd.
ziling@genupixel.com
Abstract
AI agents now dynamically acquire tools, orchestrate subagents, and transact across organizational boundaries—yet
no existing security layer can verifywhatan agent is capable of,whetherit executed what it claims, orwhat actually
happenedin a multi-agent interaction. We trace this governance vacuum to a missing architectural distinction: the
capability-context separation. Inside a transformer’s
forward pass, tool definitions and user context are indistinguishable token sequences; at the orchestration layer,
they have fundamentally different security semantics—
tool definitions determine which real-world actions are
possible(and change infrequently), while runtime context
determines which actions arechosen(and changes per
interaction). Existing frameworks conflate the two, enablingsilent capability escalation—agents acquiring tools
without invalidating credentials—and leaving cross-agent
interactions without verifiable provenance.
From this principle, we derive threeAgent Governance Requirements: capability integrity (G1) governs
the capability envelope, behavioral verifiability (G2) ensures agents executed their declared computational process, and interaction auditability (G3) provides tamperevident records for the runtime context—together definingwhatan agent ecosystem must enforce, independent
of
