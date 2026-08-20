---
title: "Exploring the Limits of Probes for Latent Representation Edits in GPT Models"
authors:
  - "Davis AL"
  - "Ferrer RV"
  - "Sukthankar G."
url: "https://doi.org/10.20944/preprints202601.2229.v1"
published: "2026"
citations: "0"
source: "EuropePMC & DOAJ"
id: "europepmc:PPR1148925"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Exploring the Limits of Probes for Latent Representation Edits in GPT Models

**Authors**: Davis AL, Ferrer RV, Sukthankar G.
**Published**: 2026 | **Citations**: 0 | **Source**: EuropePMC & DOAJ
**URL**: https://doi.org/10.20944/preprints202601.2229.v1

## Executive Summary & Abstract
This article evaluates the use of probing classifiers to modify the internal hidden state of a chess-playing transformer, which has been trained on sequences of chess moves and can generate new moves with prompted. Probing classifiers are a technique for understanding and modifying the operation of neural networks in which a smaller classifier is trained to use the model’s internal representation to learn a probing task. The aim of this research is to discover whether the learned model possesses an editable internal representation of the chess game, despite being trained without explicit information about the rules of chess. We contrast the performance of standard linear probes against Sparse Autoencoders (SAEs), a latent space interpretability technique designed to decompose polysemantic concepts into atomic features via an overcomplete basis. Our experiments demonstrate that linear probes trained directly on the residual stream significantly outperform probes based on SAE latents. When quantifying the success of interventions via the probability of legal moves, linear probe edits achieved an 88% success rate, whereas SAE-based edits yielded only 41%. These findings suggest that while SAEs are valuable for specific interpretability tasks, they do not enhance the controllability of hidden states compared to raw vectors. Finally, we show that the residual stream respects the Markovian property of chess, validating the feasibility of applying consistent edits across different time steps for the same board state.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
This article evaluates the use of probing classifiers to modify the internal hidden state of a chess-playing transformer, which has been trained on sequences of chess moves and can generate new moves with prompted. Probing classifiers are a technique for understanding and modifying the operation of neural networks in which a smaller classifier is trained to use the model’s internal representation to learn a probing task. The aim of this research is to discover whether the learned model possesses an editable internal representation of the chess game, despite being trained without explicit information about the rules of chess. We contrast the performance of standard linear probes against Sparse Autoencoders (SAEs), a latent space interpretability technique designed to decompose polysemantic concepts into atomic features via an overcomplete basis. Our experiments demonstrate that linear probes trained directly on the residual stream significantly outperform probes based on SAE latents. When quantifying the success of interventions via the probability of legal moves, linear probe edits achieved an 88% success rate, whereas SAE-based edits yielded only 41%. These findings suggest that while SAEs are valuable for specific interpretability tasks, they do not enhance the controllability of hidden states compared to raw vectors. Finally, we show that the residual stream respects the Markovian property of chess, validating the feasibility of applying consistent edits across different t
