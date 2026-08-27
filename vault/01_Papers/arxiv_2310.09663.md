---
title: "VBFT: Veloce Byzantine Fault Tolerant Consensus for Blockchains"
authors:
  - "Mohammad M. Jalalzai"
  - "Chen Feng"
  - "Victoria Lemieux"
url: "http://arxiv.org/abs/2310.09663v5"
published: "2023-10-14"
citations: "0"
source: "arXiv"
id: "arxiv:2310.09663"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-trustworthy-multi-agent-systems-formal-verification"
---
# VBFT: Veloce Byzantine Fault Tolerant Consensus for Blockchains

**Authors**: Mohammad M. Jalalzai, Chen Feng, Victoria Lemieux
**Published**: 2023-10-14 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2310.09663v5

## Abstract
Low latency is one of the most desirable features of partially synchronous Byzantine consensus protocols. Existing low-latency protocols have achieved consensus with just two communication steps by reducing the maximum number of faults the protocol can tolerate (from $f = \frac{n-1}{3}$ to $f = \frac{n+1}{5}$), \textcolor{black}{by relaxing protocol safety guarantees}, or by using trusted hardware like Trusted Execution Environment. Furthermore, these two-step protocols don't support rotating leaders and low-cost view change (leader replacement), which are important features of many blockchain use cases. In this paper, we propose a protocol called VBFT which achieves consensus in just two communication steps without sacrificing desirable features. In particular, VBFT tolerates $f = \frac{n-1}{3}$ faults (which is the best possible), guarantees strong safety for honest leaders, and requires no trusted hardware. Moreover, VBFT supports leader rotation and low-cost view change, thereby improving prior art on multiple axes.
