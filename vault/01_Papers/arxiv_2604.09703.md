---
title: "Cayley Graph Optimization for Scalable Multi-Agent Communication Topologies"
authors:
  - "Jingkai Luo"
  - "Yulin Shao"
url: "http://arxiv.org/abs/2604.09703v1"
published: "2026-04-07"
citations: "0"
source: "arXiv"
id: "arxiv:2604.09703"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# Cayley Graph Optimization for Scalable Multi-Agent Communication Topologies

**Authors**: Jingkai Luo, Yulin Shao
**Published**: 2026-04-07 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2604.09703v1

## Abstract
Large-scale multi-agent communication has long faced a scalability bottleneck: fully connected networks require quadratic complexity, yet existing sparse topologies rely on hand-crafted rules. This paper treats the communication graph itself as a design variable and proposes CayleyTopo, a family of circulant Cayley graphs whose generator sets are optimized to minimize diameter, directly targeting worst-case information propagation speed. To navigate the enormous search space of possible generator sets, we develop a lightweight reinforcement learning framework that injects a number-theoretic prior to favor structurally rich generators, alongside a message-propagation score that provides dense connectivity feedback during construction. The resulting CayleyTopo consistently outperforms existing hand-crafted topologies, achieving faster information dissemination, greater resilience to link failures, and lower communication load, all while approaching the theoretical Moore bound. Our study opens the door to scalable, robust, and efficient communication foundations for future multi-agent systems, where the graph itself becomes optimizable rather than a fixed constraint.
