---
title: "Monitoring Partially Synchronous Distributed Systems using SMT Solvers"
authors:
  - "Vidhya Tekken Valapil"
  - "Sorrachai Yingchareonthawornchai"
  - "Sandeep Kulkarni"
  - "Eric Torng"
  - "Murat Demirbas"
url: "http://arxiv.org/abs/1707.07699v1"
published: "2017-07-24"
citations: "0"
source: "arXiv"
id: "arxiv:1707.07699"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Monitoring Partially Synchronous Distributed Systems using SMT Solvers

**Authors**: Vidhya Tekken Valapil, Sorrachai Yingchareonthawornchai, Sandeep Kulkarni, Eric Torng, Murat Demirbas
**Published**: 2017-07-24 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1707.07699v1

## Abstract
In this paper, we discuss the feasibility of monitoring partially synchronous distributed systems to detect latent bugs, i.e., errors caused by concurrency and race conditions among concurrent processes. We present a monitoring framework where we model both system constraints and latent bugs as Satisfiability Modulo Theories (SMT) formulas, and we detect the presence of latent bugs using an SMT solver. We demonstrate the feasibility of our framework using both synthetic applications where latent bugs occur at any time with random probability and an application involving exclusive access to a shared resource with a subtle timing bug. We illustrate how the time required for verification is affected by parameters such as communication frequency, latency, and clock skew. Our results show that our framework can be used for real-life applications, and because our framework uses SMT solvers, the range of appropriate applications will increase as these solvers become more efficient over time.
