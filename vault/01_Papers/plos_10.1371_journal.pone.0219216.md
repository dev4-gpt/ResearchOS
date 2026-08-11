---
title: "A bi-objective game-theoretic model for collaboration formation between software development firms"
authors:
  - "Muhammad Fahimullah"
  - "Yasir Faheem"
  - "Naveed Ahmad"
url: "https://doi.org/10.1371/journal.pone.0219216"
published: "2019-07-10"
citations: "0"
source: "PLOS"
id: "plos:10.1371/journal.pone.0219216"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
+------------------------------------------------------------+
| 1. Goal Formulation                                        |
|    - Define individual weights for Learning & Finance     |
+------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------+
| 2. Multi-Attribute Partner Evaluation                      |
|    - Measure Cost Contribution, Coop Ratio, Knowledge Gap  |
+------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------+
| 3. Two-Way Compatibility Filtering                         |
|    - Discard partners with incompatible minimum utility    |
+------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------+
| 4. Nash Bargaining Payoff Optimization                     |
|    - Compute stable payoff distribution (hybrid vector)    |
+------------------------------------------------------------+
```

1. **Strategic Goal Profiling:** Partner-seeking firms declare their individual goals ($G_i$) along the two axes (Learning vs. Revenue).
2. **Parameter Quantifying:** Estimates for cost contribution ($C_i$), cooperation ratio ($R_{\text{coop}}$), and knowledge difference ($\Delta K$) are gathered.
3. **Bargaining Strategy Execution:** The Nash Bargaining model computes the Pareto-optimal frontier, allowing firms to trade off monetary gains for learning gains based on their counterpart's profile.

## 4. Evaluative Scenarios & Analysis

The paper performs a comprehensive scenario analysis to validate the Nash Bargaining payoff distribution model under varying conditions:

| Scenario ID | Strategic Profile Firm A | Strategic Profile Firm B | Dominant Parametric Variable | Optimal Strategy / Payoff Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **S1: Balanced** | Equal focus (Learning & Revenue) | Equal focus (Learning & Revenue) | Symmetric Cost & Knowledge | Equal distribution of financial and knowledge assets. |
| **S2: Asymmetric Goals** | Purely Financial ($O_{A, F} \gg O_{A, L}$) | Purely Learning ($O_{B, L} \gg O_{B, F}$) | High $\Delta K$ (A possesses knowledge) | Firm B compensates Firm A financially in exchange for knowledge transfer (Learning). |
| **S3: High Cost Disparity** | Balanced | Balanced | High Cost Contribution ($C_A \gg C_B$) | Firm A receives a proportionally higher share of financial revenue to offset capital risks. |
| **S4: Cooperative Asymmetry** | Balanced | Balanced | Low Cooperation Ratio ($R_{\text{coop}, B} < R_{\text{coop}, A}$) | Payoff distribution penalizes Firm B's lack of cooperation, shifting utility to Firm A. |

## 5. Limitations & Future Work

### Limitations Acknowledged in the Study
* **Dimensionality Constraints:** The model is strictly bi-objective (Learning and Financial Revenue). It does not explicitly account for other strategic goals such as brand reputation, market share expansion, or risk diversification.
* **Information Symmetry Assumption:** The Nash Bargaining model assumes complete information symmetry during negotiation, whereas real-world software collaborations often feature hidden parameters or strategic misrepresentation of capabilities (information asymmetry).
* **Bilateral Restriction:** The model is structurally optimized for **bilateral alliances** (2-firm systems) and does not scale naturally to complex multi-firm consortia or network-level collaborations without exponential increases in coalition formulation complexity.