---
title: "Learning Interpretable Features in Audio Latent Spaces via Sparse Autoencoders"
authors:
  - "Nathan Paek"
  - "Yongyi Zang"
  - "Qihui Yang"
  - "Randal Leistikow"
url: "http://arxiv.org/abs/2510.23802v1"
published: "2025-10-27"
citations: "0"
source: "arXiv"
id: "arxiv:2510.23802"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Learning Interpretable Features in Audio Latent Spaces via Sparse Autoencoders

**Authors**: Nathan Paek, Yongyi Zang, Qihui Yang, Randal Leistikow
**Published**: 2025-10-27 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2510.23802v1

## Executive Summary & Abstract
While sparse autoencoders (SAEs) successfully extract interpretable features from language models, applying them to audio generation faces unique challenges: audio's dense nature requires compression that obscures semantic meaning, and automatic feature characterization remains limited. We propose a framework for interpreting audio generative models by mapping their latent representations to human-interpretable acoustic concepts. We train SAEs on audio autoencoder latents, then learn linear mappings from SAE features to discretized acoustic properties (pitch, amplitude, and timbre). This enables both controllable manipulation and analysis of the AI music generation process, revealing how acoustic properties emerge during synthesis. We validate our approach on continuous (DiffRhythm-VAE) and discrete (EnCodec, WavTokenizer) audio latent spaces, and analyze DiffRhythm, a state-of-the-art text-to-music model, to demonstrate how pitch, timbre, and loudness evolve throughout generation. While our work is only done on audio modality, our framework can be extended to interpretable analysis of visual latent space generation models.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Learning Interpretable Features in Audio Latent
Spaces via Sparse Autoencoders
Nathan Paek3†‡,Yongyi Zang 1‡,Qihui Yang 2†‡,Randal Leistikow 1
1Smule Labs 2University of California, San Diego 3Stanford University
†Work done during internship at Smule, ‡These authors contributed equally.
While sparse autoencoders (SAEs) successfully extract interpretable features from language models, applying
them to audio generation faces unique challenges: audio’s dense nature requires compression that obscures
semantic meaning, and automatic feature characterization remains limited. We propose a framework for
interpreting audio generative models by mapping their latent representations to human-interpretable acoustic
concepts. We train SAEs on audio autoencoder latents, then learn linear mappings from SAE features to
discretized acoustic properties (pitch, amplitude, and timbre). This enables both controllable manipulation and
analysis of the AI music generation process, revealing how acoustic properties emerge during synthesis. We
validate our approach on continuous (DiffRhythm-VAE) and discrete (EnCodec, WavTokenizer) audio latent
spaces, and analyze DiffRhythm, a state-of-the-art text-to-music model, to demonstrate how pitch, timbre, and
loudness evolve throughout generation. While our work is only done on audio modality, our framework can be
extended to interpretable analysis of visual latent space generation models.
1 Introduction
As powerful neural networks become more integrated into
