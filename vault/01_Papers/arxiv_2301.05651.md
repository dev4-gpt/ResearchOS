---
title: "Mutation Testing of Deep Reinforcement Learning Based on Real Faults"
authors:
  - "Florian Tambon"
  - "Vahid Majdinasab"
  - "Amin Nikanjam"
  - "Foutse Khomh"
  - "Giuliano Antonio"
url: "http://arxiv.org/abs/2301.05651v1"
published: "2023-01-13"
citations: "0"
source: "arXiv"
id: "arxiv:2301.05651"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Mutation Testing of Deep Reinforcement Learning Based on Real Faults

**Authors**: Florian Tambon, Vahid Majdinasab, Amin Nikanjam, Foutse Khomh, Giuliano Antonio
**Published**: 2023-01-13 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2301.05651v1

## Abstract
Testing Deep Learning (DL) systems is a complex task as they do not behave like traditional systems would, notably because of their stochastic nature. Nonetheless, being able to adapt existing testing techniques such as Mutation Testing (MT) to DL settings would greatly improve their potential verifiability. While some efforts have been made to extend MT to the Supervised Learning paradigm, little work has gone into extending it to Reinforcement Learning (RL) which is also an important component of the DL ecosystem but behaves very differently from SL. This paper builds on the existing approach of MT in order to propose a framework, RLMutation, for MT applied to RL. Notably, we use existing taxonomies of faults to build a set of mutation operators relevant to RL and use a simple heuristic to generate test cases for RL. This allows us to compare different mutation killing definitions based on existing approaches, as well as to analyze the behavior of the obtained mutation operators and their potential combinations called Higher Order Mutation(s) (HOM). We show that the design choice of the mutation killing definition can affect whether or not a mutation is killed as well as the generated test cases. Moreover, we found that even with a relatively small number of test cases and operators we manage to generate HOM with interesting properties which can enhance testing capability in RL systems.
