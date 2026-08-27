---
title: "Constraint Solving for Finite Model Finding in SMT Solvers"
authors:
  - "Andrew Reynolds"
  - "Cesare Tinelli"
  - "Clark Barrett"
url: "http://arxiv.org/abs/1706.00096v1"
published: "2017-05-31"
citations: "0"
source: "arXiv"
id: "arxiv:1706.00096"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Constraint Solving for Finite Model Finding in SMT Solvers

**Authors**: Andrew Reynolds, Cesare Tinelli, Clark Barrett
**Published**: 2017-05-31 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1706.00096v1

## Abstract
SMT solvers have been used successfully as reasoning engines for automated verification and other applications based on automated reasoning. Current techniques for dealing with quantified formulas in SMT are generally incomplete, forcing SMT solvers to report "unknown" when they fail to prove the unsatisfiability of a formula with quantifiers. This inability to return counter-models limits their usefulness in applications that produce queries involving quantified formulas. In this paper, we reduce these limitations by integrating finite model finding techniques based on constraint solving into the architecture used by modern SMT solvers. This approach is made possible by a novel solver for cardinality constraints, as well as techniques for on-demand instantiation of quantified formulas. Experiments show that our approach is competitive with the state of the art in SMT, and orthogonal to approaches in automated theorem proving.
