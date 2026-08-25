---
title: "SWE-Exp: Experience-Driven Software Issue Resolution"
authors:
  - "Silin Chen"
  - "Shaoxin Lin"
  - "Yuling Shi"
  - "Heng Lian"
  - "Xiaodong Gu"
  - "Longfei Yun"
  - "Dong Chen"
  - "Lin Cao"
  - "Jiyang Liu"
  - "Nu Xia"
  - "Qianxiang Wang"
url: "http://arxiv.org/abs/2507.23361v2"
published: "2025-07-31"
citations: "0"
source: "arXiv"
id: "arxiv:2507.23361"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# SWE-Exp: Experience-Driven Software Issue Resolution

**Authors**: Silin Chen, Shaoxin Lin, Yuling Shi, Heng Lian, Xiaodong Gu, Longfei Yun, Dong Chen, Lin Cao, Jiyang Liu, Nu Xia, Qianxiang Wang
**Published**: 2025-07-31 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2507.23361v2

## Abstract
Recent advances in large language model (LLM) agents have shown remarkable progress in software issue resolution, leveraging advanced techniques such as multi-agent collaboration and Monte Carlo Tree Search (MCTS). However, current agents act as memoryless explorers - treating each problem separately without retaining or reusing knowledge from previous repair experiences. This leads to redundant exploration of failed trajectories and missed chances to adapt successful issue resolution methods to similar problems. To address this problem, we introduce SWE-Exp, an experience-enhanced approach that distills concise and actionable experience from prior agent trajectories, enabling continuous learning across issues. Our method introduces a multi-faceted experience bank that captures both successful and failed repair attempts. Specifically, it extracts reusable issue resolution knowledge at different levels - from high-level problem comprehension to specific code changes. Experiments show that SWE-Exp achieves a Pass@1 resolution rate of 73.0% on SWE-Bench Verified using the state-of-the-art LLM Claude 4 Sonnet, significantly outperforming prior results under other agent frameworks. Our approach establishes a new paradigm in which automated software engineering agents systematically accumulate and leverage repair expertise, fundamentally shifting from trial-and-error exploration to strategic, experience-driven issue resolution.
