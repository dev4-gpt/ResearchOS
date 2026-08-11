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
```yml

publication_date: 2026-01-26

sample_size: 4 (number of queries in the benchmark)
p_value: Not reported
methodology:

algorithms:

system_architecture:

experimental_results:

datasets:

quantitative_benchmarks:

limitations:

```

## Introduction
The paper discusses the implementation of an A2A Hub (orchestrator) on Cloud Run to route queries to different downstream agents and tool paths, ensuring cross-boundary agent interoperability and UI stability. The authors identify practical issues with Gemini Enterprise UI and A2A implementations, including UI compatibility, authentication design, and permission design.

## Methodology
The authors use the A2A protocol, Cloud Run, JSON-RPC, and REST tool API to implement the A2A Hub. They employ deterministic routing, input normalization, and a Hub-based approach to improve UI stability and error containment.

## System Architecture
The system comprises the Gemini Enterprise UI, the A2A Hub, and multiple downstream agents and tool paths. The A2A Hub normalizes input, performs routing, and forwards requests to the appropriate downstream path.

## Experimental Results
The authors evaluate the proposed Hub using a four-query benchmark, covering expense policy, project management assistance, general knowledge, and incident response deadline extraction. They confirm deterministic routing, UI compatibility, and cross-boundary connectivity.

## Limitations
The authors acknowledge limitations, including UI compatibility issues due to mixing structured data with text, authentication design across project and account boundaries, and permission design for Retrieval-Augmented Generation (RAG).

## Conclusion
The paper presents a Hub-based approach to stabilize Gemini Enterprise A2A across projects and accounts, ensuring UI stability and error containment. The authors demonstrate the effectiveness of their approach using a four-query benchmark and discuss limitations and future work.

### References
[[A2A Protocol]]: The A2A protocol specifies a loosely coupled mechanism for agent-to-agent communication.
[[Cloud Run]]: A fully managed platform for containerized web applications and APIs.
[[JSON-RPC]]: A lightweight remote procedure call protocol.
[[REST Tool API]]: A RESTful API for debugging and inspection.
[[Retrieval-Augmented Generation (RAG)]]: A technique that combines retrieval and generation models for improved performance.
[[Vertex AI Search]]: A managed service for building, deploying, and managing machine learning models.
[[Discovery Engine]]: A managed service for building, deploying, and managing machine learning models.