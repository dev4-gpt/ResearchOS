---
title: "Optimising distribution-aware GenAI infrastructure for enterprise knowledge services: supporting SECI knowledge flows, digital transformation, and organisational resilience"
authors:
  - "Yong-Jae Lee"
url: "https://doi.org/10.1108/jeim-12-2025-1269"
published: "2026-6-19"
citations: "0"
source: "Crossref"
id: "crossref:10.1108/jeim-12-2025-1269"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "enterprise-genai-roi"
---
# Optimising distribution-aware GenAI infrastructure for enterprise knowledge services: supporting SECI knowledge flows, digital transformation, and organisational resilience

**Authors**: Yong-Jae Lee
**Published**: 2026-6-19 | **Citations**: 0 | **Source**: Crossref
**URL**: https://doi.org/10.1108/jeim-12-2025-1269

## Executive Summary & Abstract
Purpose
                    This study investigates how micro-level GenAI infrastructure optimisation – specifically CPU thread tuning on NPU-accelerated inference – affects enterprise knowledge management, organisational resilience, and digital transformation outcomes.
                  
                  
                    Design/methodology/approach
                    We propose the Infrastructure-to-Knowledge Outcomes (I2KO) pathway as an infrastructure-level operationalisation linking service performance distributions to SECI knowledge flows, Kolb's learning cycle, and dynamic capabilities. Using Qwen2.5–3B on KT ATOM + NPUs, we benchmarked 70 workloads across eight categories, including n = 15 multiturn scenarios for socialisation-phase analysis. We introduce the Resilience Degradation Index (RDI = P95/P50) to capture tail-risk exposure invisible to average-centric metrics.
                  
                  
                    Findings
                    Optimal thread configurations improved average throughput (+8.8%) and mean latency (−1.6%) but increased P95 latency (+12.1%) and context scaling sensitivity (+30.4%). The multiturn analysis suggests that tail-latency degradation increases with conversational turn depth across the n = 15 workload set, with optimisation benefits concentrating in single-turn tasks while tail-risk accumulates in conversational and large-context workloads; This directional pattern (anchored by n = 13, five-turn) requires replication. Organisational implications are theoretically inferred and await field validation.
                  
                  
                    Practical implications
                    We propose a four-layer governance stack (Policy, Control, Monitoring, Review) and deployable design patterns – Lite Tier, Analytical Tier, Memory Broker, Context Pipeline – with illustrative SLO thresholds (e.g. P95 &amp;lt;30s for Socialisation; scaling factor &amp;lt;9.0 for Externalisation) derived from HCI response-time research and enterprise SLA precedents.
                  
                  
                    Originality/value
                    This study provides an initial empirical operationalisation of performance-distribution effects on enterprise knowledge capabilities, extending IT business value and dynamic capabilities theory by disaggregating infrastructure performance into efficiency-oriented (P50) and predictability-oriented (P95) dimensions.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Purpose
                    This study investigates how micro-level GenAI infrastructure optimisation – specifically CPU thread tuning on NPU-accelerated inference – affects enterprise knowledge management, organisational resilience, and digital transformation outcomes.
                  
                  
                    Design/methodology/approach
                    We propose the Infrastructure-to-Knowledge Outcomes (I2KO) pathway as an infrastructure-level operationalisation linking service performance distributions to SECI knowledge flows, Kolb's learning cycle, and dynamic capabilities. Using Qwen2.5–3B on KT ATOM + NPUs, we benchmarked 70 workloads across eight categories, including n = 15 multiturn scenarios for socialisation-phase analysis. We introduce the Resilience Degradation Index (RDI = P95/P50) to capture tail-risk exposure invisible to average-centric metrics.
                  
                  
                    Findings
                    Optimal thread configurations improved average throughput (+8.8%) and mean latency (−1.6%) but increased P95 latency (+12.1%) and context scaling sensitivity (+30.4%). The multiturn analysis suggests that tail-latency degradation increases with conversational turn depth across the n = 15 workload set, with optimisation benefits concentrating in single-turn tasks while tail-risk accumulates in conversational and large-context workloads; This directional pattern (anchored by n = 13, five-turn) requires replication
