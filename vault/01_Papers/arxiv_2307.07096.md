---
title: "Low Rank Properties for Estimating Microphones Start Time and Sources Emission Time"
authors:
  - "Faxian Cao"
  - "Yongqiang Cheng"
  - "Adil Mehmood Khan"
  - "Zhijing Yang"
  - "S. M. Ahsan Kazmiand Yingxiu Chang"
url: "http://arxiv.org/abs/2307.07096v2"
published: "2023-07-14"
citations: "0"
source: "arXiv"
id: "arxiv:2307.07096"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Low Rank Properties for Estimating Microphones Start Time and Sources Emission Time

**Authors**: Faxian Cao, Yongqiang Cheng, Adil Mehmood Khan, Zhijing Yang, S. M. Ahsan Kazmiand Yingxiu Chang
**Published**: 2023-07-14 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2307.07096v2

## Abstract
Uncertainty in timing information pertaining to the start time of microphone recordings and sources' emission time pose significant challenges in various applications, such as joint microphones and sources localization. Traditional optimization methods, which directly estimate this unknown timing information (UTIm), often fall short compared to approaches exploiting the low-rank property (LRP). LRP encompasses an additional low-rank structure, facilitating a linear constraint on UTIm to help formulate related low-rank structure information. This method allows us to attain globally optimal solutions for UTIm, given proper initialization. However, the initialization process often involves randomness, leading to suboptimal, local minimum values. This paper presents a novel, combined low-rank approximation (CLRA) method designed to mitigate the effects of this random initialization. We introduce three new LRP variants, underpinned by mathematical proof, which allow the UTIm to draw on a richer pool of low-rank structural information. Utilizing this augmented low-rank structural information from both LRP and the proposed variants, we formulate four linear constraints on the UTIm. Employing the proposed CLRA algorithm, we derive global optimal solutions for the UTIm via these four linear constraints.Experimental results highlight the superior performance of our method over existing state-of-the-art approaches, measured in terms of both the recovery number and reduced estimation errors of UTIm.
