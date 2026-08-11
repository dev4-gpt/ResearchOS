---
title: "Economic policy uncertainty and common prosperity within the enterprise: Evidence from the Chinese market"
authors:
  - "Linjing Yang"
  - "Xiaoke Tan"
  - "Guifang Tan"
url: "https://doi.org/10.1371/journal.pone.0309370"
published: "2024-10-21"
citations: "0"
source: "PLOS"
id: "plos:10.1371/journal.pone.0309370"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
# Economic Policy Uncertainty and Common Prosperity Within the Enterprise

## Executive Summary
This study investigates the relationship between [[Economic Policy Uncertainty]] (EPU) and [[Common Prosperity]] within enterprises. Using a sample of non-financial listed companies on the Shanghai and Shenzhen stock exchanges spanning 2011 to 2020, the paper demonstrates that EPU exerts a significant negative effect on intra-enterprise common prosperity. This adverse relationship is heterogeneous across ownership structures, life-cycle stages, innovation levels, and external financing/support conditions. Furthermore, the paper identifies [[Corporate Social Responsibility]] (CSR) and [[Total Factor Productivity]] (TFP) as critical buffering mechanisms that mitigate these negative effects.

## Theoretical Framework & Core Hypotheses

Based on the research findings, the core theoretical mechanisms can be formalized into the following hypotheses:

*   **Hypothesis 1 (Direct Effect):** High levels of [[Economic Policy Uncertainty]] (EPU) exert a significant negative impact on the level of [[Common Prosperity]] within enterprises.
*   **Hypothesis 2 (Mitigation - CSR):** Active engagement in [[Corporate Social Responsibility]] (CSR) mitigates the adverse effects of EPU on intra-enterprise common prosperity.
*   **Hypothesis 3 (Mitigation - TFP):** Superior [[Total Factor Productivity]] (TFP) buffers the firm against policy shocks, preserving intra-enterprise common prosperity.

```
[Economic Policy Uncertainty (EPU)] ──(Negative Impact)──> [Intra-Enterprise Common Prosperity]
                                          ▲
                                          │ (Mitigating Buffers)
                                 ┌────────┴────────┐
                                 │  - High CSR     │
                                 │  - High TFP     │
                                 └─────────────────┘
```

## Empirical Methodology

### Data & Sample Selection
*   **Target Population:** Non-financial listed companies.
*   **Exchanges:** Shanghai Stock Exchange (SSE) and Shenzhen Stock Exchange (SZSE).
*   **Temporal Scope:** 2011 – 2020.
*   **Exclusions:** Financial sector firms (due to distinct accounting standards and capital structures).

### Model Specifications (Implied Econometric Design)

While the explicit math equations were not written out in the provided abstract text, the standard panel data framework used for analyzing these effects is structured as follows:

$$\text{CommonProsperity}_{i,t} = \alpha_0 + \beta_1 \text{EPU}_{t} + \sum \gamma_k \text{Controls}_{i,t} + \mu_i + \lambda_t + \epsilon_{i,t}$$

Where:
*   $\text{CommonProsperity}_{i,t}$ represents the level of common prosperity within enterprise $i$ at time $t$.
*   $\text{EPU}_{t}$ is the Economic Policy Uncertainty index in year $t$.
*   $\text{Controls}_{i,t}$ represents firm-level control variables.
*   $\mu_i$ represents firm fixed effects.
*   $\lambda_t$ represents industry/province or time fixed effects.
*   $\epsilon_{i,t}$ is the idiosyncratic error term.

#### Moderation/Mitigation Model
To test the mitigating roles of [[Corporate Social Responsibility]] ($CSR$) and [[Total Factor Productivity]] ($TFP$):

$$\text{CommonProsperity}_{i,t} = \alpha_0 + \beta_1 \text{EPU}_{t} + \beta_2 \text{Moderator}_{i,t} + \beta_3 (\text{EPU}_{t} \times \text{Moderator}_{i,t}) + \sum \gamma_k \text{Controls}_{i,t} + \mu_i + \epsilon_{i,t}$$

*Where $\text{Moderator}_{i,t} \in \{CSR_{i,t}, TFP_{i,t}\}$*. A positive coefficient on the interaction term ($\beta_3 > 0$) confirms a mitigating effect.

## Empirical Results & Heterogeneity

The paper confirms several distinct patterns regarding where and how EPU degrades common prosperity:

### 1. Heterogeneity Analysis
The negative impact of EPU on intra-enterprise common prosperity is **more pronounced** under the following conditions:

| Heterogeneity Dimension | Vulnerable Group | Resilient Group | Theoretical Rationale |
| :--- | :--- | :--- | :--- |
| **Ownership Structure** | [[State-Owned Enterprises]] (SOEs) | Non-SOEs (Private) | SOEs often carry heavier social/policy burdens making them more sensitive to macroeconomic policy shifts. |
| **Life Cycle Stage** | Growth Stage | Mature/Decline Stages | Growth-stage firms have higher cash-flow volatility and investment needs, making them vulnerable to policy shocks. |
| **Innovation Capability** | Low Innovation | High Innovation | Low-innovation firms lack competitive moats to absorb external shocks. |
| **External Support** | Limited External Support | Strong External Support | Lack of government subsidies or credit access exacerbates resource constraints under uncertainty. |

### 2. Mitigation Mechanisms
The adverse effects of EPU are significantly **weakened** if the firm exhibits:
1.  **Higher overall factor productivity (TFP):** Allows the firm to optimize resource allocation during policy fluctuations.
2.  **Enhanced Corporate Social Responsibility (CSR):** Builds reputational capital and stakeholder trust, acting as an organizational insurance policy.

### 3. Dynamic Features (Quantile Regression Insights)
As the baseline level of intra-enterprise common prosperity **increases**:
*   The negative impact of EPU **gradually diminishes**.
*   The positive buffering effects of TFP and CSR **become more evident**.

## Limitations & Scope Constraints
*   **Geographic Focus:** The study is strictly limited to the **Chinese market** (Shanghai and Shenzhen Stock Exchanges), which exhibits unique institutional settings (e.g., state-owned enterprise dynamics, government-driven common prosperity initiatives) that may limit generalizability to market economies with different regulatory regimes.
*   **Sector Constraint:** Non-financial listed companies are analyzed; the financial sector is entirely excluded.
*   **Time Horizon:** Data is capped up to **2020**, omitting long-term post-pandemic adjustments and subsequent regulatory changes in China's corporate landscape.