---
title: "Intrinsic Low-Tucker-Rank Theory and Unified Tensor CUR Decomposition for High-Dimensional Hyperinterpolation"
authors:
  - "Maolin Che"
  - "Yimin Wei"
  - "Chong Wu"
url: "http://arxiv.org/abs/2607.19741v2"
published: "2026-07-22"
citations: "0"
source: "arXiv"
id: "arxiv:2607.19741"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Intrinsic Low-Tucker-Rank Theory and Unified Tensor CUR Decomposition for High-Dimensional Hyperinterpolation

**Authors**: Maolin Che, Yimin Wei, Chong Wu
**Published**: 2026-07-22 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2607.19741v2

## Abstract
High-dimensional hyperinterpolation is severely hampered by the curse of dimensionality, as its coefficient tensors grow exponentially with the ambient dimension. Existing research predominantly focuses on heuristic algorithmic optimizations, often overlooking the inherent structural properties of these tensors. This paper establishes a rigorous theory of intrinsic low-$ε$-Tucker-rank for hyperinterpolation coefficient tensors, delivering near-optimal low-rank approximations with error bounds that are nearly independent of the dimension. We further construct a unified, Tucker-compatible theoretical framework that integrates both Chidori-type and Fiber-type tensor CUR (TCUR) decompositions, deriving tight and stable Frobenius-norm error estimates that depend exclusively on tensor spectral properties and index set geometry. We mathematically verify the convergence and numerical stability of greedy adaptive index selection schemes and prove their near-optimality, enabling a fully tensor-free hyperinterpolation workflow that avoids constructing the full coefficient array. Three practical greedy TCUR algorithms and a lightweight TCUR-to-Tucker recompression pipeline are proposed as direct corollaries of our structural theory. Numerical experiments across three distinct families of high-dimensional test functions validate all theoretical predictions and confirm the intrinsic low-rank compressibility of hyperinterpolation coefficients. In contrast to prior algorithm-centric studies, this work prioritizes rigorous theoretical characterization over implementation tricks, establishing a unified structural and mathematical foundation for high-dimensional hyperinterpolation.
