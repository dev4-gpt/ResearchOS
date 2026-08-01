# Layer Specification: Topic Ideation & Recommender Engine

## 1. Overview

The **Topic Recommender Service** (`backend/services/topic_recommender.py`) provides curated, high-impact research topics optimized for journal publication (IEEE TKDE, ACM CSUR, Nature MI, NeurIPS/ICML Survey Tracks).

---

## 2. Topic Scoring & Impact Criteria

Topics are evaluated across four quantitative dimensions:

$$\text{Impact Score} = 0.35 \cdot S_{\text{novelty}} + 0.30 \cdot S_{\text{readership}} + 0.20 \cdot S_{\text{empirical}} + 0.15 \cdot S_{\text{timeliness}}$$

1. **Novelty & Unique Angle ($S_{\text{novelty}}$)**: Addresses emerging paradigms (e.g. test-time compute scaling, monosemantic feature extraction, jagged capability frontiers) rather than re-hashing baseline models.
2. **Readership & Citation Potential ($S_{\text{readership}}$)**: High relevance for both computer science systems researchers and C-suite enterprise technology officers.
3. **Empirical Data Availability ($S_{\text{empirical}}$)**: Abundant randomized controlled trials ($N > 1,000$) and telemetry-backed datasets across open repositories.
4. **Timeliness ($S_{\text{timeliness}}$)**: Aligns with 2024–2026 conference tracks and journal calls.

---

## 3. High-Impact Curated Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   HIGH-IMPACT RESEARCH PUBLISHING TAXONOMY                             │
├───────────────────┬───────────────────┬───────────────────┬────────────────────────────┤
│ 1. Enterprise GenAI│ 2. Test-Time     │ 3. Mechanistic    │ 4. Autonomous Agentic      │
│    ROI & Limits   │    Compute & CoT  │    Interpretability│   Workflows & TRiSM Security│
│   (Impact: 98/100)│   (Impact: 96/100)│   (Impact: 95/100)│   (Impact: 94/100)         │
└───────────────────┴───────────────────┴───────────────────┴────────────────────────────┘
```

### 3.1 Topic 1: Enterprise Generative AI ROI & Limits
- **Title**: *Systematic Review & Meta-Taxonomy of Generative AI in Enterprise Workflows: Empirical Evidence, Economic Limits, Skill Equalization, and Task Boundary Frontiers*
- **Target Venues**: IEEE TKDE / MIS Quarterly
- **Impact Score**: **98/100**

### 3.2 Topic 2: Test-Time Compute & Reasoning-Time Optimization
- **Title**: *Test-Time Compute, Inference Scaling Laws, and Search-Guided Reasoning in Large Language Models: A Systematic Survey*
- **Target Venues**: ACM CSUR / NeurIPS Survey Track
- **Impact Score**: **96/100**

### 3.3 Topic 3: Mechanistic Interpretability via Sparse Autoencoders
- **Title**: *Mechanistic Interpretability via Sparse Autoencoders: Feature Extraction, Circuit Discovery, and Safety Steering in Frontier Models*
- **Target Venues**: Nature Machine Intelligence / ICML
- **Impact Score**: **95/100**

### 3.4 Topic 4: Autonomous Agentic Systems & TRiSM Security
- **Title**: *Architectures, Communication Protocols, and Rejection Vulnerabilities of Autonomous Multi-Agent Systems in Regulated Enterprise Domains*
- **Target Venues**: IEEE Transactions on Autonomous Mental Development
- **Impact Score**: **94/100**

### 3.5 Topic 5: Quantized Small Language Models (SLMs) vs. Cloud APIs
- **Title**: *Quantized Small Language Models (SLMs) vs. Proprietary Cloud APIs: A Comparative Empirical Benchmark of Privacy, Latency, and Token OpEx*
- **Target Venues**: ACM Transactions on Computer Systems (TOCS)
- **Impact Score**: **92/100**
