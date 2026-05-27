---
title: "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
authors:
  - "Xuezhi Wang"
  - "Jason Wei"
  - "Dale Schuurmans"
  - "Quoc Le"
  - "Ed Chi"
  - "Sharan Narang"
  - "Aakanksha Chowdhery"
  - "Denny Zhou"
url: "http://arxiv.org/abs/2203.11171v4"
published: "2022-03-21"
citations: "0"
source: "arXiv"
id: "arxiv:2203.11171"
tags:
  - "research-paper"
  - ""research-and-extract-key-insights,-methodologies,-and-findings-from-two-papers:-1)-'self-consistency-improves-chain-of-thought-reasoning'-(https://arxiv.org/abs/2203.11171)-and-2)-'llm-as-a-judge'-(https://arxiv.org/pdf/2411.15594).-please-evaluate-their-approaches-and-store-the-most-important-concepts-and-summaries-in-the-knowledge-vault.""
---
---
title: "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
authors: [Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou]
date: 2022-03-21
url: "http://arxiv.org/abs/2203.11171v4"
citations: 0
category: Research Paper
tags: [nlp, large-language-models, decoding-strategies, chain-of-thought, reasoning]
---

# Self-Consistency Improves Chain of Thought Reasoning in Language Models

## Quick Summary
This paper introduces **Self-Consistency**, a novel decoding strategy that replaces traditional greedy decoding in [[Chain-of-Thought Prompting]] (CoT). By sampling a diverse set of reasoning paths instead of a single deterministic path, and then selecting the most consistent final answer (marginalizing over the reasoning paths), the authors significantly boost LLM performance on complex arithmetic and commonsense reasoning tasks.

---

## Core Hypotheses & Claims

1. **The Multiplicity of Reasoning Paths**: For any complex reasoning problem, there are typically multiple different, valid ways of thinking that lead to the same unique correct answer.
2. **Greedy Decoding Limitation**: Naive greedy decoding in [[Chain-of-Thought Prompting]] is suboptimal because it commits to a single local path, which might contain a minor error even if the overall reasoning capability of the model is high.
3. **Consistency Implies Correctness**: If multiple independently sampled reasoning paths converge on the same final answer, that answer is highly likely to be correct.

---

## Methodology & Algorithm

The **Self-Consistency** mechanism operates as a post-processing decoding strategy:

```
                  ┌─── Reasoning Path 1 ───> Answer A ──┐
                  ├─── Reasoning Path 2 ───> Answer B ──┼──> [Majority Vote] ──> Winner: Answer A
Prompt + Query ───┼─── Reasoning Path 3 ───> Answer A ──┤
                  └─── Reasoning Path 4 ───> Answer A ──┘
```

1. **Prompting**: Prompt the Large Language Model using standard [[Chain-of-Thought Prompting]].
2. **Sampling**: Instead of greedy decoding, generate a diverse set of $N$ candidate reasoning paths $\{r_1, r_2, ..., r_N\}$ and their corresponding final answers $\{a_1, a_2, ..., a_N\}$ using a sampling decoder (e.g., temperature sampling).
3. **Marginalization (Majority Voting)**: Collect all final answers and select the most frequent output:
   $$\text{argmax}_{a} \sum_{i=1}^{N} \mathbb{I}(a_i = a)$$
   *(Note: This marginalizes out the reasoning paths $r_i$ to find the most consistent final answer $a$.)*

---

## Experimental Design & Quantitative Results

The authors evaluated the self-consistency method against baseline chain-of-thought prompting (with greedy decoding) across five popular benchmarks:

### Performance Boost Summary

| Dataset | Task Category | Accuracy Improvement (Absolute % Gain) |
| :--- | :--- | :--- |
| **[[GSM8K]]** | Grade school math word problems | **+17.9%** |
| **[[SVAMP]]** | Adversarial math word problems | **+11.0%** |
| **[[AQuA]]** | Algebraic word problems | **+12.2%** |
| **[[StrategyQA]]** | Multi-step commonsense reasoning | **+6.4%** |
| **[[ARC-Challenge]]** | Science question-answering | **+3.9%** |

---

## Limitations (Acknowledged & Inferred)

* **Computational Cost**: Sampling $N$ different reasoning paths requires $N$ times more computational resources (FLOPs, latency, token generation cost) compared to standard greedy decoding.
* **Closed-Ended Answer Dependency**: The strategy relies on being able to group outputs into identical final answers (e.g., a specific number or multiple-choice letter). It is more challenging to apply directly to open-ended, subjective generation tasks where "exact match" grouping is not feasible.
* **Calibration on Hard Tasks**: If the model is highly confident but consistently wrong across most reasoning paths (systematic bias/hallucination), self-consistency will reinforce the incorrect consensus answer.

---

## Related Concepts & Internal Links
* [[Chain-of-Thought Prompting]]
* [[Decoding Strategies]]
* [[Large Language Models]]
* [[Reasoning in LLMs]]
* [[Ensemble Methods]]