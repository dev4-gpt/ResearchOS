---
title: "Mirrored STDP Implements Autoencoder Learning in a Network of Spiking Neurons"
authors:
  - "Kendra S Burbank"
url: "https://doi.org/10.1371/journal.pcbi.1004566"
published: "2015-12-03"
citations: "0"
source: "PLOS"
id: "plos:10.1371/journal.pcbi.1004566"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Mirrored STDP Implements Autoencoder Learning in a Network of Spiking Neurons

**Authors**: Kendra S Burbank
**Published**: 2015-12-03 | **Citations**: 0 | **Source**: PLOS
**URL**: https://doi.org/10.1371/journal.pcbi.1004566

## Executive Summary & Abstract

The autoencoder algorithm is a simple but powerful unsupervised method for training neural networks. Autoencoder networks can learn sparse distributed codes similar to those seen in cortical sensory areas such as visual area V1, but they can also be stacked to learn increasingly abstract representations. Several computational neuroscience models of sensory areas, including Olshausen & Field’s Sparse Coding algorithm, can be seen as autoencoder variants, and autoencoders have seen extensive use in the machine learning community. Despite their power and versatility, autoencoders have been difficult to implement in a biologically realistic fashion. The challenges include their need to calculate differences between two neuronal activities and their requirement for learning rules which lead to identical changes at feedforward and feedback connections. Here, we study a biologically realistic network of integrate-and-fire neurons with anatomical connectivity and synaptic plasticity that closely matches that observed in cortical sensory areas. Our choice of synaptic plasticity rules is inspired by recent experimental and theoretical results suggesting that learning at feedback connections may have a different form from learning at feedforward connections, and our results depend critically on this novel choice of plasticity rules. Specifically, we propose that plasticity rules at feedforward versus feedback connections are temporally opposed versions of spike-timing dependent plasticity (STDP), leading to a symmetric combined rule we call Mirrored STDP (mSTDP). We show that with mSTDP, our network follows a learning rule that approximately minimizes an autoencoder loss function. When trained with whitened natural image patches, the learned synaptic weights resemble the receptive fields seen in V1. Our results use realistic synaptic plasticity rules to show that the powerful autoencoder learning algorithm could be within the reach of real biological networks.
Author Summary: In the brain areas responsible for sensory processing, neurons learn over time to respond to specific features in the external world. Here, we propose a new, biologically plausible model for how groups of neurons can learn which specific features to respond to. Our work connects theoretical arguments about the optimal forms of neuronal representations with experimental results showing how synaptic connections change in response to neuronal activity. Specifically, we show that biologically realistic neurons can implement an algorithm known as autoencoder learning, in which the neurons learn to form representations that can be used to reconstruct their inputs. Autoencoder networks can successfully model neuronal responses in early sensory areas, and they are also frequently used in machine learning for training deep neural networks. Despite their power and utility, autoencoder networks have not been previously implemented in a fully biological fashion. To perform the autoencoder algorithm, neurons must modify their incoming, feedforward synaptic connections as well as their outgoing, feedback synaptic connections—and the changes to both must depend on the errors the network makes when it tries to reconstruct its input. Here, we propose a model for activity in the network and show that the commonly used spike-timing-dependent plasticity paradigm will implement the desired changes to feedforward synaptic connection weights. Critically, we use recent experimental evidence to propose that feedback connections learn according to a temporally reversed plasticity rule. We show mathematically that the two rules combined can approximately implement autoencoder learning, and confirm our results using simulated networks of integrate-and-fire neurons. By showing that biological neurons can implement this powerful algorithm, our work opens the door for the modeling of many learning paradigms from both the fields of computational neuroscience and machine learning. 

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet

The autoencoder algorithm is a simple but powerful unsupervised method for training neural networks. Autoencoder networks can learn sparse distributed codes similar to those seen in cortical sensory areas such as visual area V1, but they can also be stacked to learn increasingly abstract representations. Several computational neuroscience models of sensory areas, including Olshausen & Field’s Sparse Coding algorithm, can be seen as autoencoder variants, and autoencoders have seen extensive use in the machine learning community. Despite their power and versatility, autoencoders have been difficult to implement in a biologically realistic fashion. The challenges include their need to calculate differences between two neuronal activities and their requirement for learning rules which lead to identical changes at feedforward and feedback connections. Here, we study a biologically realistic network of integrate-and-fire neurons with anatomical connectivity and synaptic plasticity that closely matches that observed in cortical sensory areas. Our choice of synaptic plasticity rules is inspired by recent experimental and theoretical results suggesting that learning at feedback connections may have a different form from learning at feedforward connections, and our results depend critically on this novel choice of plasticity rules. Specifically, we propose that plasticity rules at feedforward versus feedback connections are temporally opposed versions of spike-timing dependent plastic
