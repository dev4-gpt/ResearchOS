---
title: "The Jagged Global Economy: Frontier AI Unevenly Exposes National Economies"
authors:
  - "Arul Murugan"
  - "Tomás Aguirre"
  - "Abhishek Nagaraj"
  - "Rishi Bommasani"
url: "http://arxiv.org/abs/2607.05404v1"
published: "2026-06-08"
citations: "0"
source: "arXiv"
id: "arxiv:2607.05404"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
---
title: "The Jagged Global Economy: Frontier AI Unevenly Exposes National Economies"
authors: [Arul Murugan, Tomás Aguirre, Abhishek Nagaraj, Rishi Bommasani]
date: 2026-06-08
arxiv_id: "2607.05404v1"
url: "http://arxiv.org/abs/2607.05404v1"
citations: 0
tags: [artificial-intelligence, economics, global-labor, labor-exposure, remittances]
---

# The Jagged Global Economy: Frontier AI Unevenly Exposes National Economies

## Executive Summary
This paper introduces a **National AI Exposure** metric designed to evaluate how frontier Artificial Intelligence ([[Frontier AI]]) unevenly impacts labor markets across the globe. By linking international employment statistics across 141 countries with occupation-level exposure scores, the authors show that high-income nations and white-collar-dominant economies face significantly greater direct exposure than low-income and agriculture-dependent nations. Additionally, the paper identifies a pervasive **gender gap** in AI exposure and reveals a novel **indirect exposure** mechanism driven by cross-country [[Remittance]] dependencies (e.g., Tajikistan's exposure via Russia, and Central American exposure via the United States).

---

## 1. Core Concepts & Definitions

*   **National AI Exposure ($Exposure_c$)**: A comparable country-level metric quantifying how strongly a national economy's current labor allocation aligns with the tasks that frontier AI can accelerate or transform.
*   **Jagged Capabilities**: The phenomenon where AI capabilities vary significantly across highly specific tasks within the same occupation (as defined in [[Dell'Acqua et al., 2026]]).
*   **Direct Exposure**: Exposure driven purely by the domestic composition of a country's labor market.
*   **Indirect Exposure (Remittance-Accounted)**: Exposure resulting from economic reliance on foreign workers sending remittances from highly exposed nations back to their home countries.

---

## 2. Mathematical Formulation

The direct National AI Exposure for a given country $c$ is calculated by combining occupational employment shares with occupational exposure scores:

$$Exposure_c = \sum_{o \in O} \theta_{c,o} \cdot E_o$$

Where:
*   $O$ represents the set of occupational categories.
*   $\theta_{c,o}$ is the proportion of total employment allocated to occupation $o$ in country $c$ (i.e., $\frac{\text{Employment}_{c,o}}{\text{Total Employment}_c}$), or wage-weighted equivalents where available.
*   $E_o$ is the technological exposure score of occupation $o$ derived from [[Gmyrek et al., 2026]] / [[Eloundou et al., 2024]], representing the share of tasks within occupation $o$ that can be accelerated/saved by current frontier AI capabilities.

---

## 3. Methodology & Data Sources

### 3.1 Occupational Employment Data
*   **Source**: International Labour Organization ([[ILO]]) database using the **ISCO-08** (International Standard Classification of Occupations) classification.
*   **Granularity**: 2-digit (sub-major group) ISCO-08 occupational categories.
*   **Coverage**: Initially 43 categories, filtered down to **40 occupational categories** after excluding armed forces, aggregate, and residual rows.
*   **Sample Size**: **141 countries** with complete, mature labor market data.

### 3.2 Occupational Exposure Metrics
*   Based on methodology from [[Eloundou et al., 2024]] and [[Gmyrek et al., 2026]], which leverages human and GPT-4 annotations to evaluate task-level impact (criteria: saving at least 50% of the time spent on a task while preserving quality).

---

## 4. Empirical Results & Quantitative Benchmarks

### 4.1 Global Disparities in Exposure
*   **Highest vs. Lowest**: The most exposed nation (**Luxembourg**) is **$2.6\times$** more exposed to frontier AI than the least exposed nation (**Burundi**).
*   **Regional Variance**: Europe & Central Asia, alongside North America, are at least **50% more exposed** than Sub-Saharan Africa.
*   **Labor Composition Drivers**: Office- and knowledge-intensive work (ISCO major groups 1-4) accounts for **61%** of employment in the United States, compared to **14%** in India and **5%** in Mozambique.

| Country | Office & Knowledge Work (ISCO 1–4) | Agriculture (ISCO 6) |
| :--- | :--- | :--- |
| **United States** | 61% | 0.4% |
| **India** | 14% | 35% |
| **Mozambique** | 5% | 73% |

### 4.2 The Gender Exposure Gap
*   In **91% of countries**, women are more exposed to frontier AI than men.
*   **Driver**: High concentration of female employment in clerical, white-collar, and sales occupations.
*   **Exceptions**: Countries where women's employment remains heavily concentrated in agriculture and household enterprises.

### 4.3 Validation against Real-World Adoption
The authors validated the predictive validity of their National AI Exposure metric by comparing it to usage and adoption statistics from Anthropic, Microsoft, and OpenAI.
*   **Quantitative Scaling**: A **0.10 increase** in national AI exposure predicts:
    *   **$12\times$ growth** in national per-capita Claude (Anthropic) usage.
    *   A **19 percentage-point increase** in the national generative AI adoption rate.

### 4.4 Indirect Exposure via Remittances
Several nations with low domestic direct exposure have high economic vulnerability to AI due to their reliance on remittances from highly exposed nations:

```
[Highly Exposed Country (e.g., Russia / US)] 
       |
       | (Remittance Flows)
       v
[Low Direct Exposure Country (e.g., Tajikistan / Honduras)]
       |
       +--> High Indirect Economic Exposure
```

*   **Tajikistan**: Direct exposure is below average, but **37% of Tajikistan’s GDP** is derived from Russian remittances. Because Russia's labor market is highly exposed, Tajikistan’s remittance-adjusted exposure shifts to above-average.
*   **Central America (Honduras, Guatemala, El Salvador)**: Remittances account for **25% of domestic GDP**, with more than **80%** of these remittances originating from the United States. High AI exposure in the US labor market implicitly exposes these source nations to severe economic shocks.

---

## 5. Limitations Acknowledged by the Authors

1.  **Data Gaps**: The study lacks 2-digit ISCO-08 employment data for several major economies, notably **China, Canada, and Saudi Arabia**.
2.  **Not a Direct Forecast**: The metric measures *exposure* (potential task automation/augmentation) and does not represent a direct forecast of immediate adoption rates, wage changes, or net job losses.
3.  **Remittance Channel Incompleteness**: The remittance model focuses heavily on major bilateral corridors (e.g., US-Central America, Russia-Tajikistan) but does not map out all multi-lateral or indirect trade and supply-chain exposure networks globally.