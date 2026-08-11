---
title: "Mind the Boundary: Stabilizing Gemini Enterprise A2A via a Cloud Run Hub Across Projects and Accounts"
authors:
  - "Takao Morita"
url: "http://arxiv.org/abs/2602.17675v1"
published: "2026-01-26"
citations: "0"
source: "arXiv"
id: "arxiv:2602.17675"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
# Mind the Boundary: Stabilizing Gemini Enterprise A2A via a Cloud Run Hub Across Projects and Accounts

**Authors**: Takao Morita
**Published**: 2026-01-26 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2602.17675v1

## Executive Summary & Abstract
Enterprise conversational UIs increasingly need to orchestrate heterogeneous backend agents and tools across project and account boundaries in a secure and reproducible way. Starting from Gemini Enterprise Agent-to-Agent (A2A) invocation, we implement an A2A Hub orchestrator on Cloud Run that routes queries to four paths: a public A2A agent deployed in a different project, an IAM-protected Cloud Run A2A agent in a different account, a retrieval-augmented generation path combining Discovery Engine and Vertex AI Search with direct retrieval of source text from Google Cloud Storage, and a general question answering path via Vertex AI. We show that practical interoperability is governed not only by protocol compliance but also by Gemini Enterprise UI constraints and boundary-dependent authentication. Real UI requests arrive as text-only inputs and include empty accepted output mode lists, so mixing structured data into JSON-RPC responses can trigger UI errors. To address this, we enforce a text-only compatibility mode on the JSON-RPC endpoint while separating structured outputs and debugging signals into a REST tool API. On a four-query benchmark spanning expense policy, project management assistance, general knowledge, and incident response deadline extraction, we confirm deterministic routing and stable UI responses. For the retrieval path, granting storage object read permissions enables evidence-backed extraction of the fifteen minute deadline. All experiments are reproducible using the repository snapshot tagged a2a-hub-gemini-ui-stable-paper.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Mind the Boundary: Stabilizing Gemini Enterprise A2A via a Cloud
Run Hub Across Projects and Accounts
Takao Morita (Takao Morita)
Independent Researcher
Abstract
Enterprise conversational UIs increasingly need to orchestrate heterogeneous backend agents
and tools across project and account boundaries in a secure and reproducible way. Starting from
Gemini Enterprise’s Agent-to-Agent (A2A) invocation, we implement an A2A Hub (orchestrator)
on Cloud Run that routes queries to: (i) a public A2A agent deployed in a different project, (ii)
an IAM-protected Cloud Run A2A agent in a different account, (iii) a RAG path combining
Discovery Engine / Vertex AI Search with direct retrieval of source text from Google Cloud
Storage (GCS), and (iv) a general QA path via Vertex AI. We show that practical interoperability
is governed not only by protocol compliance but also by Gemini Enterprise UI constraints and
boundary-dependent authentication. Real UI requests arrive in params.message.parts[].text and
include acceptedOutputModes=[], so mixing structured data into JSON-RPC responses can
trigger UI errors. To address this, we enforce a text-only compatibility mode on the JSON-RPC
endpoint while separating structured outputs and debugging signals into a REST tool API.
On a four-query benchmark spanning expense policy, PM assistance, general knowledge, and
incident-response deadline extraction, we confirm deterministic routing and stable UI responses;
for the RAG path, granting storage.objects
