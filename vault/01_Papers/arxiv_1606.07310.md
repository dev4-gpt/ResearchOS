---
title: "Fault-Tolerant Adaptive Parallel and Distributed Simulation"
authors:
  - "Gabriele D'Angelo"
  - "Stefano Ferretti"
  - "Moreno Marzolla"
  - "Lorenzo Armaroli"
url: "http://arxiv.org/abs/1606.07310v2"
published: "2016-06-23"
citations: "0"
source: "arXiv"
id: "arxiv:1606.07310"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# Fault-Tolerant Adaptive Parallel and Distributed Simulation

**Authors**: Gabriele D'Angelo, Stefano Ferretti, Moreno Marzolla, Lorenzo Armaroli
**Published**: 2016-06-23 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1606.07310v2

## Abstract
Discrete Event Simulation is a widely used technique that is used to model and analyze complex systems in many fields of science and engineering. The increasingly large size of simulation models poses a serious computational challenge, since the time needed to run a simulation can be prohibitively large. For this reason, Parallel and Distributes Simulation techniques have been proposed to take advantage of multiple execution units which are found in multicore processors, cluster of workstations or HPC systems. The current generation of HPC systems includes hundreds of thousands of computing nodes and a vast amount of ancillary components. Despite improvements in manufacturing processes, failures of some components are frequent, and the situation will get worse as larger systems are built. In this paper we describe FT-GAIA, a software-based fault-tolerant extension of the GAIA/ARTÌS parallel simulation middleware. FT-GAIA transparently replicates simulation entities and distributes them on multiple execution nodes. This allows the simulation to tolerate crash-failures of computing nodes; furthermore, FT-GAIA offers some protection against byzantine failures since synchronization messages are replicated as well, so that the receiving entity can identify and discard corrupted messages. We provide an experimental evaluation of FT-GAIA on a running prototype. Results show that a high degree of fault tolerance can be achieved, at the cost of a moderate increase in the computational load of the execution units.
