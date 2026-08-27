---
title: "Sigmoid Attention as a Better Substrate for Learned KV Cache Eviction"
authors:
  - " Isaac"
  - " Li"
url: "http://arxiv.org/abs/2608.23296v1"
published: "2026-08-24"
citations: "0"
source: "arXiv"
id: "arxiv:2608.23296"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Sigmoid Attention as a Better Substrate for Learned KV Cache Eviction

**Authors**:  Isaac,  Li
**Published**: 2026-08-24 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2608.23296v1

## Abstract
Learned KV-cache eviction often faces a soft-to-hard mismatch: during training, differentiable gates typically attenuate token contributions, whereas inference saves memory only when KV entries are physically removed. We ask whether the attention substrate affects this soft-to-hard transition. Using GPT-2-scale Transformers trained on OpenWebText, we run a controlled $2\times2\times2$ comparison over attention type, learned gating, and positional encoding. Although sigmoid attention is worse as a dense language model, learned hard eviction changes the useful operating points: sigmoid-gated models delete KV entries with negligible PPL change relative to their own no-eviction references. Under a matched live-cache protocol on the same dense backbones, learned sigmoid gates obtain lower PPL than our H$_2$O and KeyDiff implementations, whereas softmax gates do not uniformly beat these post-hoc methods. The results suggest that attention normalization can substantially affect whether a training-time soft gate transfers cleanly to hard KV deletion.
