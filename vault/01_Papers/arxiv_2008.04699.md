---
title: "Byzantine Fault-Tolerant Distributed Machine Learning Using Stochastic Gradient Descent (SGD) and Norm-Based Comparative Gradient Elimination (CGE)"
authors:
  - "Nirupam Gupta"
  - "Shuo Liu"
  - "Nitin H. Vaidya"
url: "http://arxiv.org/abs/2008.04699v2"
published: "2020-08-11"
citations: "0"
source: "arXiv"
id: "arxiv:2008.04699"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-trustworthy-multi-agent-systems-formal-verification"
---
# Byzantine Fault-Tolerant Distributed Machine Learning Using Stochastic Gradient Descent (SGD) and Norm-Based Comparative Gradient Elimination (CGE)

**Authors**: Nirupam Gupta, Shuo Liu, Nitin H. Vaidya
**Published**: 2020-08-11 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2008.04699v2

## Abstract
This paper considers the Byzantine fault-tolerance problem in distributed stochastic gradient descent (D-SGD) method - a popular algorithm for distributed multi-agent machine learning. In this problem, each agent samples data points independently from a certain data-generating distribution. In the fault-free case, the D-SGD method allows all the agents to learn a mathematical model best fitting the data collectively sampled by all agents. We consider the case when a fraction of agents may be Byzantine faulty. Such faulty agents may not follow a prescribed algorithm correctly, and may render traditional D-SGD method ineffective by sharing arbitrary incorrect stochastic gradients. We propose a norm-based gradient-filter, named comparative gradient elimination (CGE), that robustifies the D-SGD method against Byzantine agents. We show that the CGE gradient-filter guarantees fault-tolerance against a bounded fraction of Byzantine agents under standard stochastic assumptions, and is computationally simpler compared to many existing gradient-filters such as multi-KRUM, geometric median-of-means, and the spectral filters. We empirically show, by simulating distributed learning on neural networks, that the fault-tolerance of CGE is comparable to that of existing gradient-filters. We also empirically show that exponential averaging of stochastic gradients improves the fault-tolerance of a generic gradient-filter.
