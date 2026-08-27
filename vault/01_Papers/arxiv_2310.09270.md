---
title: "Retro-fallback: retrosynthetic planning in an uncertain world"
authors:
  - "Austin Tripp"
  - "Krzysztof Maziarz"
  - "Sarah Lewis"
  - "Marwin Segler"
  - "José Miguel Hernández-Lobato"
url: "http://arxiv.org/abs/2310.09270v3"
published: "2023-10-13"
citations: "0"
source: "arXiv"
id: "arxiv:2310.09270"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Retro-fallback: retrosynthetic planning in an uncertain world

**Authors**: Austin Tripp, Krzysztof Maziarz, Sarah Lewis, Marwin Segler, José Miguel Hernández-Lobato
**Published**: 2023-10-13 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2310.09270v3

## Abstract
Retrosynthesis is the task of planning a series of chemical reactions to create a desired molecule from simpler, buyable molecules. While previous works have proposed algorithms to find optimal solutions for a range of metrics (e.g. shortest, lowest-cost), these works generally overlook the fact that we have imperfect knowledge of the space of possible reactions, meaning plans created by algorithms may not work in a laboratory. In this paper we propose a novel formulation of retrosynthesis in terms of stochastic processes to account for this uncertainty. We then propose a novel greedy algorithm called retro-fallback which maximizes the probability that at least one synthesis plan can be executed in the lab. Using in-silico benchmarks we demonstrate that retro-fallback generally produces better sets of synthesis plans than the popular MCTS and retro* algorithms.
