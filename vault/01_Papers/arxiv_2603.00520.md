---
title: "SWE-ABS: Adversarial Benchmark Strengthening Exposes Inflated Success Rates on Test-based Benchmark"
authors:
  - "Boxi Yu"
  - "Yang Cao"
  - "Yuzhong Zhang"
  - "Liting Lin"
  - "Junjielong Xu"
  - "Zhiqing Zhong"
  - "Qinghua Xu"
  - "Guancheng Wang"
  - "Jialun Cao"
  - "Shing-Chi Cheung"
  - "Pinjia He"
  - "Lionel Briand"
url: "http://arxiv.org/abs/2603.00520v1"
published: "2026-02-28"
citations: "0"
source: "arXiv"
id: "arxiv:2603.00520"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# SWE-ABS: Adversarial Benchmark Strengthening Exposes Inflated Success Rates on Test-based Benchmark

**Authors**: Boxi Yu, Yang Cao, Yuzhong Zhang, Liting Lin, Junjielong Xu, Zhiqing Zhong, Qinghua Xu, Guancheng Wang, Jialun Cao, Shing-Chi Cheung, Pinjia He, Lionel Briand
**Published**: 2026-02-28 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2603.00520v1

## Abstract
The SWE-Bench Verified leaderboard is approaching saturation, with the top system achieving 78.80%. However, we show that this performance is inflated. Our re-evaluation reveals that one in five "solved" patches from the top-30 agents are semantically incorrect, passing only because weak test suites fail to expose their errors. We present SWE-ABS, an adversarial framework that strengthens test suites through a two-stage pipeline: (1) coverage-driven augmentation using program slicing to target untested code regions, and (2) mutation-driven adversarial testing that synthesizes plausible but incorrect patches to expose semantic blind spots. On SWE-Bench Verified (500 instances), SWE-ABS strengthens 50.2% of instances, a 25.1x improvement over prior work, and rejects 19.71% of previously passing patches. As a result, the top agent's score decreases from 78.80% to 62.20%, leading to significant leaderboard reshuffling, with the previous top-ranked agent dropping to fifth place.
