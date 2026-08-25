---
title: "Adequate Losses via Quantitative Linear Logic"
authors:
  - "Matteo Capucci"
  - "Robert Atkey"
  - "Charles Grellois"
  - "Ekaterina Komendantskaya"
  - "Matthew Daggitt"
url: "http://arxiv.org/abs/2605.13348v3"
published: "2026-05-13"
citations: "0"
source: "arXiv"
id: "arxiv:2605.13348"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-trustworthy-multi-agent-systems-formal-verification"
---
# Adequate Losses via Quantitative Linear Logic

**Authors**: Matteo Capucci, Robert Atkey, Charles Grellois, Ekaterina Komendantskaya, Matthew Daggitt
**Published**: 2026-05-13 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2605.13348v3

## Abstract
As neural components are increasingly embedded in existing symbolic software -- including safety-critical systems -- the question arises of how to specify and enforce the safety of the newly introduced neural parts. Unlike traditional logical specifications, these must be amenable not only to the standard Boolean interpretation, but also to training and optimisation. The latter calls for a quantitative interpretation of the logical syntax, subject to further requirements such as smoothness and differentiability. Moreover, the qualitative and quantitative sides of the logic must share a unifying proof-theoretic and categorical semantics. Finally, the new logic should link cleanly to the substructural and program logics that underpin the verification of existing symbolic programs. In this paper, we present a logic that ticks all of these boxes. We introduce a family of calculi, pQLL, indexed by a hardness degree $p$, prove a cut-elimination theorem for them, and establish completeness with respect to enriched residuated `soft' lattices. At $p = \infty$, \pQLL reduces to multiplicative additive linear logic (MALL), and provability in pQLL converges to provability in MALL as $p \to \infty$. We express optimisation objectives in the syntax of this logic and prove the quantitative adequacy of neuro-symbolic loss functions -- a result that has eluded the neuro-symbolic machine learning community for nearly a decade.
