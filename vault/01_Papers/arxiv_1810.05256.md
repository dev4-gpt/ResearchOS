---
title: "Aleph: A Leaderless, Asynchronous, Byzantine Fault Tolerant Consensus Protocol"
authors:
  - "Adam Gągol"
  - "Michał Świętek"
url: "http://arxiv.org/abs/1810.05256v2"
published: "2018-10-11"
citations: "0"
source: "arXiv"
id: "arxiv:1810.05256"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-trustworthy-multi-agent-systems-formal-verification"
---
# Aleph: A Leaderless, Asynchronous, Byzantine Fault Tolerant Consensus Protocol

**Authors**: Adam Gągol, Michał Świętek
**Published**: 2018-10-11 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1810.05256v2

## Abstract
In this paper we propose Aleph, a leaderless, fully asynchronous, Byzantine fault tolerant consensus protocol for ordering messages exchanged among processes. It is based on a distributed construction of a partially ordered set and the algorithm for reaching a consensus on its extension to a total order. To achieve the consensus, the processes perform computations based only on a local copy of the data structure, however, they are bound to end with the same results. Our algorithm uses a dual-threshold coin-tossing scheme as a randomization strategy and establishes the agreement in an expected constant number of rounds. In addition, we introduce a fast way of validating messages that can occur prior to determining the total ordering. This version of the protocol is deprecated. For current version see arXiv:1908.05156.
