---
title: "Federated Sketching LoRA: A Flexible Framework for Heterogeneous Collaborative Fine-Tuning of LLMs"
authors:
  - "Wenzhi Fang"
  - "Dong-Jun Han"
  - "Liangqi Yuan"
  - "Seyyedali Hosseinalipour"
  - "Christopher G. Brinton"
url: "http://arxiv.org/abs/2501.19389v4"
published: "2025-01-31"
citations: "0"
source: "arXiv"
id: "arxiv:2501.19389"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# Federated Sketching LoRA: A Flexible Framework for Heterogeneous Collaborative Fine-Tuning of LLMs

**Authors**: Wenzhi Fang, Dong-Jun Han, Liangqi Yuan, Seyyedali Hosseinalipour, Christopher G. Brinton
**Published**: 2025-01-31 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2501.19389v4

## Abstract
Fine-tuning large language models (LLMs) on resource-constrained clients remains a challenging problem. Recent works have fused low-rank adaptation (LoRA) techniques with federated fine-tuning to mitigate challenges associated with client model sizes and data scarcity. Still, the heterogeneity of resources remains a critical bottleneck: while higher-rank modules generally enhance performance, varying client capabilities constrain LoRA's feasible rank range. Existing approaches attempting to resolve this issue either lack analytical justification or impose additional computational overhead, leaving a wide gap for efficient and theoretically-grounded solutions. To address these challenges, we propose federated sketching LoRA (FSLoRA), which leverages a sketching mechanism to enable clients to selectively update submatrices of global LoRA modules maintained by the server. By adjusting the sketching ratios, which determine the ranks of the submatrices on the clients, FSLoRA flexibly adapts to client-specific communication and computational constraints. We provide a rigorous convergence analysis of FSLoRA that characterizes how the sketching ratios affect the convergence rate. Through extensive experiments, we demonstrate that FSLoRA outperforms baselines and significantly improves training efficiency while preserving stable convergence.
