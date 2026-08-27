---
title: "Input-Sparsity Low Rank Approximation in Schatten Norm"
authors:
  - "Yi Li"
  - "David Woodruff"
url: "http://arxiv.org/abs/2004.12646v3"
published: "2020-04-27"
citations: "0"
source: "arXiv"
id: "arxiv:2004.12646"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# Input-Sparsity Low Rank Approximation in Schatten Norm

**Authors**: Yi Li, David Woodruff
**Published**: 2020-04-27 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2004.12646v3

## Abstract
We give the first input-sparsity time algorithms for the rank-$k$ low rank approximation problem in every Schatten norm. Specifically, for a given $n\times n$ matrix $A$, our algorithm computes $Y,Z\in \mathbb{R}^{n\times k}$, which, with high probability, satisfy $\|A-YZ^T\|_p \leq (1+ε)\|A-A_k\|_p$, where $\|M\|_p = \left (\sum_{i=1}^n σ_i(M)^p \right )^{1/p}$ is the Schatten $p$-norm of a matrix $M$ with singular values $σ_1(M), \ldots, σ_n(M)$, and where $A_k$ is the best rank-$k$ approximation to $A$. Our algorithm runs in time $\tilde{O}(\operatorname{nnz}(A) + mn^{α_p}\operatorname{poly}(k/ε))$, where $α_p = 0$ for $p\in [1,2)$ and $α_p = (ω-1)(1-2/p)$ for $p>2$ and $ω\approx 2.374$ is the exponent of matrix multiplication. For the important case of $p = 1$, which corresponds to the more "robust" nuclear norm, we obtain $\tilde{O}(\operatorname{nnz}(A) + m \cdot \operatorname{poly}(k/ε))$ time, which was previously only known for the Frobenius norm ($p = 2$). Moreover, since $α_p < ω- 1$ for every $p$, our algorithm has a better dependence on $n$ than that in the singular value decomposition for every $p$. Crucial to our analysis is the use of dimensionality reduction for Ky-Fan $p$-norms.
