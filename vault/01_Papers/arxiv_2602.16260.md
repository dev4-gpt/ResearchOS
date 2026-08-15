---
title: "Autonomous and non-autonomous fixed-time leader-follower consensus for second-order multi-agent systems"
authors:
  - "Miguel A. Trujillo"
  - "Rodrigo Aldana-López"
  - "David Gomez Gutierrez"
  - "Michael Defoort"
  - "Javier Ruiz Leon"
  - "Hector M. Becerra"
url: "http://arxiv.org/abs/2602.16260v1"
published: "2026-02-18"
citations: "0"
source: "arXiv"
id: "arxiv:2602.16260"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems:-architectural-topologies,-empirical-benchmarks,-and-systemic-governance"
---
# Autonomous and non-autonomous fixed-time leader-follower consensus for second-order multi-agent systems

**Authors**: Miguel A. Trujillo, Rodrigo Aldana-López, David Gomez Gutierrez, Michael Defoort, Javier Ruiz Leon, Hector M. Becerra
**Published**: 2026-02-18 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2602.16260v1

## Executive Summary & Abstract
This paper addresses the problem of consensus tracking with fixed-time convergence, for leader-follower multi-agent systems with double-integrator dynamics, where only a subset of followers has access to the state of the leader. The control scheme is divided into two steps. The first one is dedicated to the estimation of the leader state by each follower in a distributed way and in a fixed-time. Then, based on the estimate of the leader state, each follower computes its control law to track the leader in a fixed-time. In this paper, two control strategies are investigated and compared to solve the two mentioned steps. The first one is an autonomous protocol which ensures a fixed-time convergence for the observer and for the controller parts where the Upper Bound of the Settling-Time (UBST) is set a priory by the user. Then, the previous strategy is redesigned using time-varying gains to obtain a non-autonomous protocol. This enables to obtain less conservative estimates of the UBST while guaranteeing that the time-varying gains remain bounded. Some numerical examples show the effectiveness of the proposed consensus protocols.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Autonomous and non-autonomous ﬁxed-time leader-follower
consensus for second-order multi-agent systems a
M. A. Trujillo b R. Aldana-L´ opezc D. G´ omez Guti´ errezd M. Defoort e
J. Ruiz Le´ ona H. M. Becerra f
Abstract
This paper addresses the problem of consensus tracking with ﬁxed -time convergence, for
leader-follower multi-agent systems with double-integrator dynam ics, where only a subset
of followers has access to the state of the leader. The control sc heme is divided into two
steps. The ﬁrst one is dedicated to the estimation of the leader sta te by each follower in a
distributed way and in a ﬁxed-time. Then, based on the estimate of t he leader state, each
follower computes its control law to track the leader in a ﬁxed-time. In this paper, two
control strategies are investigated and compared to solve the tw o mentioned steps. The ﬁrst
one is an autonomous protocol which ensures a ﬁxed-time converg ence for the observer and
for the controller parts where the Upper Bound of the Settling-Tim e (UBST ) is set a priory
by the user. Then, the previous strategy is redesigned using time- varying gains to obtain a
non-autonomous protocol. This enables to obtain less conservativ e estimates of the UBST
while guaranteeing that the time-varying gains remain bounded. Som e numerical examples
show the eﬀectiveness of the proposed consensus protocols.
1 Introduction
In the last years, the problems of coordination and control o f Multi-Agent System (MAS) have
been widely studied (se
