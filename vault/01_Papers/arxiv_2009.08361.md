---
title: "Formulog: Datalog for SMT-Based Static Analysis (Extended Version)"
authors:
  - "Aaron Bembenek"
  - "Michael Greenberg"
  - "Stephen Chong"
url: "http://arxiv.org/abs/2009.08361v2"
published: "2020-09-17"
citations: "0"
source: "arXiv"
id: "arxiv:2009.08361"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Formulog: Datalog for SMT-Based Static Analysis (Extended Version)

**Authors**: Aaron Bembenek, Michael Greenberg, Stephen Chong
**Published**: 2020-09-17 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2009.08361v2

## Abstract
Satisfiability modulo theories (SMT) solving has become a critical part of many static analyses, including symbolic execution, refinement type checking, and model checking. We propose Formulog, a domain-specific language that makes it possible to write a range of SMT-based static analyses in a way that is both close to their formal specifications and amenable to high-level optimizations and efficient evaluation. Formulog extends the logic programming language Datalog with a first-order functional language and mechanisms for representing and reasoning about SMT formulas; a novel type system supports the construction of expressive formulas, while ensuring that neither normal evaluation nor SMT solving goes wrong. Our case studies demonstrate that a range of SMT-based analyses can naturally and concisely be encoded in Formulog, and that -- thanks to this encoding -- high-level Datalog-style optimizations can be automatically and advantageously applied to these analyses.
