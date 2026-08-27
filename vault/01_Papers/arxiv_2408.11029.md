---
title: "Scaling Law with Learning Rate Annealing"
authors:
  - "Howe Tissue"
  - "Venus Wang"
  - "Lu Wang"
url: "http://arxiv.org/abs/2408.11029v2"
published: "2024-08-20"
citations: "0"
source: "arXiv"
id: "arxiv:2408.11029"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Scaling Law with Learning Rate Annealing

**Authors**: Howe Tissue, Venus Wang, Lu Wang
**Published**: 2024-08-20 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2408.11029v2

## Abstract
We find that the cross-entropy loss curves of neural language models empirically adhere to a scaling law with learning rate (LR) annealing over training steps: $$L(s) = L_0 + A\cdot S_1^{-α} - C\cdot S_2,$$ where $L(s)$ is the validation loss at step $s$, $S_1$ is the area under the LR curve, $S_2$ is the LR annealing area, and $L_0$, $A$, $C$, $α$ are constant parameters. This formulation takes into account two factors: (1) power-law scaling over data size, and (2) the additional loss reduction during LR annealing. Therefore, this formulation can describe the full loss curve at each step, rather than the single loss point at the end of training. Applying the scaling law with LR annealing and fitting only one or two training curves, we can accurately predict the loss at any given step across any learning rate scheduler (LRS). This approach significantly reduces computational cost in formulating scaling laws while providing more accuracy and expressiveness for training dynamics. Extensive experiments demonstrate that our findings hold across a range of hyper-parameters and model architectures, and our equation can extend to scaling effect of model sizes. Moreover, our formulation provides accurate theoretical verification and explanation for empirical results observed in numerous previous studies, particularly those focusing on LR schedule and annealing. We believe that this work is promising to enhance the understanding of LLM training dynamics while greatly democratizing scaling laws, and it can guide researchers in refining training strategies (e.g. critical LRS) for further LLMs.
