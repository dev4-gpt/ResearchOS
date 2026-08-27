---
title: "Speeding Up SMT-Based Quantitative Program Analysis"
authors:
  - "Daniel J. Fremont"
  - "Sanjit A. Seshia"
url: "http://arxiv.org/abs/1405.7320v1"
published: "2014-05-28"
citations: "0"
source: "arXiv"
id: "arxiv:1405.7320"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Speeding Up SMT-Based Quantitative Program Analysis

**Authors**: Daniel J. Fremont, Sanjit A. Seshia
**Published**: 2014-05-28 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1405.7320v1

## Abstract
Quantitative program analysis involves computing numerical quantities about individual or collections of program executions. An example of such a computation is quantitative information flow analysis, where one estimates the amount of information leaked about secret data through a program's output channels. Such information can be quantified in several ways, including channel capacity and (Shannon) entropy. In this paper, we formalize a class of quantitative analysis problems defined over a weighted control flow graph of a loop-free program. These problems can be solved using a combination of path enumeration, SMT solving, and model counting. However, existing methods can only handle very small programs, primarily because the number of execution paths can be exponential in the program size. We show how path explosion can be mitigated in some practical cases by taking advantage of special branching structure and by novel algorithm design. We demonstrate our techniques by computing the channel capacities of the timing side-channels of two programs with extremely large numbers of paths.
