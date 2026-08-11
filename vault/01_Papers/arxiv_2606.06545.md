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
---
title: Queen-Bee Agents: A BeeSpec-Centered Architecture for Governed Enterprise MCP Orchestration
authors: Dutao Zhang, Liaotian
source: http://arxiv.org/abs/2606.06545v1
publication_date: 2026-06-04
sample_size: 59
p_value: Not reported
---

## Abstract
The paper presents Queen-Bee, a governed multi-agent architecture for enterprise Model Context Protocol (MCP) integration. The system separates planning and execution through a structured intermediate representation, BeeSpec. The Queen control plane retrieves capabilities, plans task-scoped execution, and compiles a BeeSpec, which is executed by specialized Bee agents under constrained tool access.

## Introduction
Enterprise agent systems require policy enforcement, tenant-scoped isolation, and execution within explicit operational boundaries. The authors argue that a single general agent with unrestricted tool access is not sufficient for enterprise deployment. Instead, they propose a system that can provision specialized execution units, assign bounded capabilities, and enforce execution-time policy constraints.

## Methodology
The Queen-Bee architecture consists of four layers:

1. **Queen control plane**: responsible for capability retrieval, blueprint planning, BeeSpec generation, and governance decisions.
2. **BeeSpec intermediate layer**: explicitly defines the execution boundary for each Bee.
3. **Bee execution plane**: specialized Bees execute only within the capabilities assigned by BeeSpec.
4. **Tenant-scoped MCP connector layer**: resolves tool invocations inside the active tenant scope.

The BeeSpec schema contains the following fields:

| Field | Meaning |
| --- | --- |
| bee_id | Unique execution-unit identifier for audit and trace linking |
| role | Natural-language role assigned by the Queen |
| domain | Operational domain, such as HR, IT, finance-sensitive, or chemistry |
| tenant_scope | Tenant boundary within which MCP calls must execute |
| memory_scope | Accessible memory namespace for the Bee |
| attached_skills | Retrieved skills that drive local execution planning |
| allowed_tools | MCP-backed tools authorized for this Bee |
| policy_profile | Guardrail profile used before each tool invocation |
| approval_gate | Optional human approval requirement before downstream execution |

## Experimental Design
The system is evaluated from three perspectives:

1. **Isolation and Governance**: measures whether the system blocks unsafe finance requests, rejects cross-tenant requests, and avoids unnecessary tool use while preserving normal task execution.
2. **Retrieval-Driven Provisioning**: measures whether the Queen can retrieve relevant capabilities and compile useful BeeSpecs.
3. **Scoped Bee Execution**: measures whether Bees can independently complete local tasks under BeeSpec constraints.

## Results
The retrieval-driven Queen-Bee variant achieves a task success rate of 0.964, zero governance failures, and substantially better scoped execution quality than both a static Queen-Bee baseline and a permissive single-agent baseline.

## Limitations
The authors acknowledge that the results provide prototype-level systems evidence rather than a production deployment study. They suggest that enterprise agent platforms should be evaluated not only by capability but also by governed provisioning, isolation behavior, scoped execution quality, and artifact-aware workflow coordination.

## References
[[Model Context Protocol]] 
[[BeeSpec]] 
[[Queen-Bee Architecture]] 
[[Tenant-Scoped MCP Connectors]] 
[[Retrieval-Driven Provisioning]] 
[[Scoped Bee Execution]] 

Note: The paper does not provide explicit mathematical formulas or hypotheses. The results are based on experimental evaluations of the Queen-Bee system.