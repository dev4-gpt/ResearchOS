---
title: "Model and Program Repair via SAT Solving"
authors:
  - "Paul C. Attie"
  - "Jad Saklawi"
url: "http://arxiv.org/abs/0710.3332v4"
published: "2007-10-17"
citations: "0"
source: "arXiv"
id: "arxiv:0710.3332"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Model and Program Repair via SAT Solving

**Authors**: Paul C. Attie, Jad Saklawi
**Published**: 2007-10-17 | **Source**: arXiv
**URL**: http://arxiv.org/abs/0710.3332v4

## Abstract
We consider the following \emph{model repair problem}: given a finite Kripke structure $M$ and a specification formula $η$ in some modal or temporal logic, determine if $M$ contains a substructure $M'$ (with the same initial state) that satisfies $η$. Thus, $M$ can be ``repaired'' to satisfy the specification $η$ by deleting some transitions. We map an instance $(M, η)$ of model repair to a boolean formula $\repfor(M,η)$ such that $(M, η)$ has a solution iff $\repfor(M,η)$ is satisfiable. Furthermore, a satisfying assignment determines which transitions must be removed from $M$ to generate a model $M'$ of $η$. Thus, we can use any SAT solver to repair Kripke structures. Furthermore, using a complete SAT solver yields a complete algorithm: it always finds a repair if one exists. We extend our method to repair finite-state shared memory concurrent programs, to solve the discrete event supervisory control problem \cite{RW87,RW89}, to check for the existence of symmettric solutions \cite{ES93}, and to accomodate any boolean constraint on the existence of states and transitions in the repaired model. Finally, we show that model repair is NP-complete for CTL, and logics with polynomial model checking algorithms to which CTL can be reduced in polynomial time. A notable example of such a logic is Alternating-Time Temporal Logic (ATL).
