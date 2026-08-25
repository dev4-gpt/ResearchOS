---
title: "Byzantine Fault Tolerant Distributed Quickest Change Detection"
authors:
  - "Erhan Bayraktar"
  - "Lifeng Lai"
url: "http://arxiv.org/abs/1306.2086v2"
published: "2013-06-10"
citations: "0"
source: "arXiv"
id: "arxiv:1306.2086"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# Byzantine Fault Tolerant Distributed Quickest Change Detection

**Authors**: Erhan Bayraktar, Lifeng Lai
**Published**: 2013-06-10 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1306.2086v2

## Abstract
We introduce and solve the problem of Byzantine fault tolerant distributed quickest change detection in both continuous and discrete time setups. In this problem, multiple sensors sequentially observe random signals from the environment and send their observations to a control center that will determine whether there is a change in the statistical behavior of the observations. We assume that the signals are independent and identically distributed across sensors. An unknown subset of sensors are compromised and will send arbitrarily modified and even artificially generated signals to the control center. It is shown that the performance of the the so-called CUSUM statistic, which is optimal when all sensors are honest, will be significantly degraded in the presence of even a single dishonest sensor. In particular, instead of in a logarithmically the detection delay grows linearly with the average run length (ARL) to false alarm. To mitigate such a performance degradation, we propose a fully distributed low complexity detection scheme. We show that the proposed scheme can recover the log scaling. We also propose a centralized group-wise scheme that can further reduce the detection delay.
