---
title: "Cost-of-Pass: An Economic Framework for Evaluating Language Models"
authors:
  - "Mehmet Hamza Erol"
  - "Batu El"
  - "Mirac Suzgun"
  - "Mert Yuksekgonul"
  - "James Zou"
url: "http://arxiv.org/abs/2504.13359v2"
published: "2025-04-17"
citations: "0"
source: "arXiv"
id: "arxiv:2504.13359"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-genai-roi"
---
# Cost-of-Pass: An Economic Framework for Evaluating Language Models

**Authors**: Mehmet Hamza Erol, Batu El, Mirac Suzgun, Mert Yuksekgonul, James Zou
**Published**: 2025-04-17 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2504.13359v2

## Abstract
Widespread adoption of AI systems hinges on their ability to generate economic value that outweighs their inference costs. Evaluating this tradeoff requires metrics accounting for both performance and costs. Building on production theory, we develop an economically grounded framework to evaluate language models' productivity by combining accuracy and inference cost. We formalize cost-of-pass: the expected monetary cost of generating a correct solution. We then define the frontier cost-of-pass: the minimum cost-of-pass achievable across available models or the human-expert(s), using the approx. cost of hiring an expert. Our analysis reveals distinct economic insights. First, lightweight models are most cost-effective for basic quantitative tasks, large models for knowledge-intensive ones, and reasoning models for complex quantitative problems, despite higher per-token costs. Second, tracking the frontier cost-of-pass over the past year reveals significant progress, particularly for complex quant. tasks where the cost roughly halved every few months. Third, to trace key innovations driving this progress, we examine counterfactual frontiers -- estimates of cost-efficiency without specific model classes. We find that innovations in lightweight, large, and reasoning models have been essential for pushing the frontier in basic quant., knowledge-intensive, and complex quant. tasks, respectively. Finally, we assess the cost-reductions from common inference-time techniques (majority voting and self-refinement), and a budget-aware technique (TALE-EP). We find that performance-oriented methods with marginal performance gains rarely justify the costs, while TALE-EP shows some promise. Overall, our findings underscore that complementary model-level innovations are the primary drivers of cost-efficiency and our framework provides a principled tool for measuring this progress and guiding deployment.
