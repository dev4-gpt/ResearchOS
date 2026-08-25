---
title: "GraphRAG under Fire"
authors:
  - "Jiacheng Liang"
  - "Yuhui Wang"
  - "Changjiang Li"
  - "Rongyi Zhu"
  - "Tanqiu Jiang"
  - "Neil Gong"
  - "Ting Wang"
url: "http://arxiv.org/abs/2501.14050v4"
published: "2025-01-23"
citations: "0"
source: "arXiv"
id: "arxiv:2501.14050"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# GraphRAG under Fire

**Authors**: Jiacheng Liang, Yuhui Wang, Changjiang Li, Rongyi Zhu, Tanqiu Jiang, Neil Gong, Ting Wang
**Published**: 2025-01-23 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2501.14050v4

## Abstract
GraphRAG advances retrieval-augmented generation (RAG) by structuring external knowledge as multi-scale knowledge graphs, enabling language models to integrate both broad context and granular details in their generation. While GraphRAG has demonstrated success across domains, its security implications remain largely unexplored. To bridge this gap, this work examines GraphRAG's vulnerability to poisoning attacks, uncovering an intriguing security paradox: existing RAG poisoning attacks are less effective under GraphRAG than conventional RAG, due to GraphRAG's graph-based indexing and retrieval; yet, the same features also create new attack surfaces. We present GragPoison, a novel attack that exploits shared relations in the underlying knowledge graph to craft poisoning text capable of compromising multiple queries simultaneously. GragPoison employs three key strategies: (i) relation injection to introduce false knowledge, (ii) relation enhancement to amplify poisoning influence, and (iii) narrative generation to embed malicious content within coherent text. Empirical evaluation across diverse datasets and models shows that GragPoison substantially outperforms existing attacks in terms of effectiveness (up to 98% success rate) and scalability (using less than 68% poisoning text) on multiple variations of GraphRAG. We also explore potential defensive measures and their limitations, identifying promising directions for future research.
