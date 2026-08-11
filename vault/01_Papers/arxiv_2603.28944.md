---
title: "Faith in AI can narrow the futures individuals consider"
authors:
  - "Aoi Naito"
  - "Hirokazu Shirado"
url: "http://arxiv.org/abs/2603.28944v2"
published: "2026-03-30"
citations: "0"
source: "arXiv"
id: "arxiv:2603.28944"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
## Introduction

[[Artificial intelligence]] (AI) predictions are increasingly integrated into human decision-making processes. This paper investigates how [[AI predictions]] can not only inform decisions but also fundamentally reshape the reasoning people employ, potentially leading them to forgo guaranteed rewards. The study uses a behavioral implementation of [[Newcomb's paradox]] to explore how perceived predictive authority influences individuals' future actions.

## Key Claims & Hypotheses

*   **Main Claim:** [[AI predictions]] can shape the reasoning people use to make a decision, leading them to forgo a guaranteed reward.
*   **Hypothesis:** When people perceive AI as capable of predicting their personal behavior, the mere presence of AI predictions may shape their decision-making, narrowing the futures they consider.
*   **Reasoning Framework:**
    *   **[[Causal reasoning]]:** Individuals treat their action as affecting the payoff outcome independently of a predetermined prediction.
        *   **Equation:** `1 + X > X` (where `X` is the content of Box B, `X ∈ {0, 3}`). This logic always favors two-boxing as it guarantees an additional US$1 regardless of Box B's content.
    *   **[[Evidential reasoning]]:** Individuals treat whichever action they ultimately take as evidence of what has already been predicted. This is supported by perceived predictiveness and internal coherence.
        *   **Logic:** If one-boxing is associated with a full Box B (US$3) and two-boxing with an empty Box B (US$0), then `1 + 0 < 3`, making one-boxing appear reasonable.

## Experimental Setup

The core experimental setup is a behavioral adaptation of [[Newcomb's paradox]]:
*   **Decision Task:** Participants choose between:
    *   **Two-boxing:** Take Box A (guaranteed US$1) and Box B (contains US$0 or US$3).
    *   **One-boxing:** Take only Box B.
*   **Payoff Structure:**
    *   Box A: Always contains US$1.
    *   Box B: Contains either US$0 or US$3.
*   **Prediction Mechanism:** Participants are informed that an [[AI system]] has predicted their choice **before** they make it.
    *   If AI predicts one-boxing, Box B contains US$3.
    *   If AI predicts two-boxing, Box B contains US$0.
*   **Information Withholding:** Participants are NOT told the AI's prediction or the content of Box B at the time of choice. They are only told Box B's content is already determined by the AI's prediction.
*   **AI System:** In Study 2, the interactive AI system was powered by [[OpenAI's GPT-4.1]].

## Results

### AI Prediction Increases Forgoing Guaranteed Rewards (Studies 1 & 2)

*   **Study 1 (N=200):**
    *   **AI Condition:** 41 out of 100 participants (41.0%) chose one-boxing.
    *   **Random Condition:** 26 out of 100 participants (26.0%) chose one-boxing.
    *   **Statistical Significance:** p=0.025, indicating a significant increase in one-boxing in the AI condition.
*   **Study 2 (N=601):**
    *   **Random Framing:** One-boxing remained uncommon (15.3% in both interactive and non-interactive random conditions).
    *   **AI Framing:** One-boxing was substantially more frequent (45.0% in non-interactive AI, 42.0% in interactive AI).
    *   **Statistical Significance:** Overall increase in one-boxing under [[AI prediction]] was statistically significant (p <0.001).
    *   **Interaction Effect:** Interaction with the system (interactive vs. non-interactive) did not significantly moderate the effect (p=1.0 for both random and AI conditions).
*   **Fixed-Effect Meta-Analysis (Studies 1 & 2):**
    *   [[AI prediction]] increased the odds of forgoing the guaranteed reward by a factor of **3.39** (95% CI: 2.45–4.70; p <0.001).
    *   This shift reduced realized earnings by **10.7–42.9%** relative to the two-boxing baseline.

### Generalization Beyond Economic Task (Study 3)

*   **Study 3 (N=303):** Explored effects in vignette scenarios (job interview, mobile data coupon, task application).
    *   **AI Prediction:** 26.7% one-box-type choices.
    *   **Human-Expert Prediction:** 36.6% one-box-type choices.
    *   **No Prediction (Control):** 10.6% one-box-type choices.
    *   **Statistical Significance:** [[AI predictions]] significantly increased one-box-type choices relative to control (p <00.001).
    *   **Comparison:** [[Human-expert predictions]] produced a somewhat larger effect than [[AI predictions]] (odds ratio = 1.67, p=0.032). Both sources shifted choices in the same direction.

### Causal and Evidential Reasoning about AI Prediction

*   **Perceived Predictiveness (Study 2):**
    *   Participants in AI conditions perceived the system's predictions as significantly more accurate than chance (non-interactive AI: 62.1%, p <0.001; interactive AI: 62.9%, p <0.001).
    *   Participants in random conditions perceived chance-level accuracy (non-interactive random: 50.4%, p=0.322; interactive random: 49.7%, p=0.639).
    *   These beliefs formed despite no explicit information about accuracy.
*   **Perceived Predictiveness vs. Choice:** Perceived predictiveness alone was insufficient to explain one-boxing. Participants who one-boxed and two-boxed held similar beliefs about the AI’s predictive accuracy (non-interactive AI: p=0.080; interactive AI: p=0.634).
*   **Role of [[Internal coherence]]:** The findings suggest that one-boxing depends on both perceived predictiveness and internal coherence—the tendency to act consistently with anticipated actions. A [[computational model]] (detailed in Supplementary Text) supports that [[AI prediction]] shifts participants toward [[evidential reasoning]] over [[causal reasoning]].
*   **Qualitative Responses:** One-boxers often described decisions in relation to AI's prediction; two-boxers described choices as independent. Rarely did participants explain choices based on preferences for one option over another, supporting differences in reasoning.

## Limitations

*   **Magnitude Variation:** While the direction of the effect was consistent across scenarios in Study 3, its magnitude varied (Extended Data Fig. 1), suggesting context-dependency in the strength of AI's influence.
*   **Computational Model Details:** The full details of the computational model formalizing behavior as a mixture of [[causal reasoning]] and [[evidential reasoning]] are referenced as being in the Supplementary Text, and thus not fully elaborated within the main paper provided.