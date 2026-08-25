---
title: "SignSGD: Fault-Tolerance to Blind and Byzantine Adversaries"
authors:
  - "Jason Akoun"
  - "Sebastien Meyer"
url: "http://arxiv.org/abs/2202.02085v2"
published: "2022-02-04"
citations: "0"
source: "arXiv"
id: "arxiv:2202.02085"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# SignSGD: Fault-Tolerance to Blind and Byzantine Adversaries

**Authors**: Jason Akoun, Sebastien Meyer
**Published**: 2022-02-04 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2202.02085v2

## Abstract
Distributed learning has become a necessity for training ever-growing models by sharing calculation among several devices. However, some of the devices can be faulty, deliberately or not, preventing the proper convergence. As a matter of fact, the baseline distributed SGD algorithm does not converge in the presence of one Byzantine adversary. In this article we focus on the more robust SignSGD algorithm derived from SGD. We provide an upper bound for the convergence rate of SignSGD proving that this new version is robust to Byzantine adversaries. We implemented SignSGD along with Byzantine strategies attempting to crush the learning process. Therefore, we provide empirical observations from our experiments to support our theory. Our code is available on GitHub https://github.com/jasonakoun/signsgd-fault-tolerance and our experiments are reproducible by using the provided parameters.
