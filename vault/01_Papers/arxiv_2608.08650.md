---
title: "The Evolution of Mixture-of-Experts Architectures in Large Language Models: Routing, Topology, Load Balancing, and Expert Parallelism"
authors:
  - "Jiguo Li"
url: "http://arxiv.org/abs/2608.08650v1"
published: "2026-08-09"
citations: "0"
source: "arXiv"
id: "arxiv:2608.08650"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# The Evolution of Mixture-of-Experts Architectures in Large Language Models: Routing, Topology, Load Balancing, and Expert Parallelism

**Authors**: Jiguo Li
**Published**: 2026-08-09 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2608.08650v1

## Abstract
Mixture-of-Experts models increase parameter capacity while keeping the computation activated by each token bounded, but their architectural evolution cannot be explained by a chronological list of model releases alone. This technical survey synthesizes primary papers, official technical reports, and prior surveys to organize modern Mixture-of-Experts systems along five coupled dimensions: expert granularity, expert topology, routing freedom, the scope of load balancing, and execution structure. We describe eight architectural milestones as a dependency graph with six mainline developments and two orthogonal branches, rather than as eight successive generations. We then analyze individual systems through four control planes: Expert Topology, Routing, Balance, and Expert Parallelism. These planes specify which experts exist, which experts process each token, how aggregate load is controlled, and how selected computation is mapped onto physical devices. The framework connects algorithmic choices such as Top-k routing, shared experts, fine-grained experts, and dynamic expert composition with systems concerns including token dispatch, device placement, all-to-all communication, and communication-computation overlap. We conclude with equal-budget pretraining experiments, quality and systems metrics, and open research questions. The main trend is a shift from merely activating more sparse parameters toward decoupling semantic routing, computational budgets, and physical execution.
