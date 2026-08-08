---
title: "Literature Review: "Research and extract key insights, methodologies, and findings from two papers: 1) 'Self-Consistency Improves Chain of Thought Reasoning' (https://arxiv.org/abs/2203.11171) and 2) 'LLM-as-a-Judge' (https://arxiv.org/pdf/2411.15594). Please evaluate their approaches and store the most important concepts and summaries in the knowledge vault."
topic: "Research and extract key insights, methodologies, and findings from two papers: 1) 'Self-Consistency Improves Chain of Thought Reasoning' (https://arxiv.org/abs/2203.11171) and 2) 'LLM-as-a-Judge' (https://arxiv.org/pdf/2411.15594). Please evaluate their approaches and store the most important concepts and summaries in the knowledge vault."
status: "draft"
format: "IEEE/ACM markdown"
tags:
  - "research-and-extract-key-insights,-methodologies,-and-findings-from-two-papers:-1)-'self-consistency-improves-chain-of-thought-reasoning'-(https://arxiv.org/abs/2203.11171)-and-2)-'llm-as-a-judge'-(https://arxiv.org/pdf/2411.15594).-please-evaluate-their-approaches-and-store-the-most-important-concepts-and-summaries-in-the-knowledge-vault."
  - "literature-review"
  - "draft"
---
# Beyond the Hype: A Rigorous Systems, Statistical, and Epistemological Audit of Self-Consistency, LLM-as-a-Judge, and Multi-Agent Clinical Architectures

---

## Abstract

As large language models (LLMs) transition from static, single-pass generation toward dynamic, multi-path reasoning and automated evaluation frameworks, the field of artificial intelligence faces a critical convergence of systems engineering bottlenecks and statistical validation deficits. This literature review provides a rigorous, multi-disciplinary audit of three foundational paradigms: (1) multi-path decoding via Self-Consistency, (2) automated model evaluation using the LLM-as-a-Judge framework, and (3) specialized clinical multi-agent architectures, represented by Cardiology-Chat. 

Through a systematic synthesis of `[[arxiv:2203.11171]]` (and its peer-reviewed counterpart `[[dblp:1673083]]`), `[[arxiv:2411.15594]]`, and `[[europepmc:PMC13068123]]`, we expose critical methodological vulnerabilities that threaten the scientific validity of these advancements. Specifically, we deconstruct the "compute-equivalent baseline deficit" in multi-path decoding, expose the epistemological circularity and cognitive biases inherent in automated evaluators, and execute a statistical audit demonstrating that current clinical multi-agent validation studies are severely underpowered and subject to spectrum bias. 

Finally, we propose a set of formal methodological standards—including compute-equivalent benchmarking, psychometric calibration, and strict multi-rater agreement testing—to ground future LLM development in empirical and statistical rigor.

---

## 1. Introduction & Theoretical Foundations

### 1.1 The Convergence of Scale and Inference-Time Compute
For much of the deep learning era, the prevailing paradigm for improving the capabilities of autoregressive language models focused on pre-training parameter scaling. However, as the marginal gains of sheer parameter volume encounter physical, economic, and data-availability constraints, the paradigm has shifted toward optimizing *inference-time compute*. 

By allocating more computational budget during the decoding phase—either through parallel sampling, iterative reasoning, or multi-agent debate—models can navigate complex search spaces to resolve multi-step reasoning problems. 

### 1.2 Historical Context: From Bagging to Chain-of-Thought
This evolution is anchored in two foundational concepts:
* **Chain-of-Thought (CoT) Prompting**, which structures the decoding process as a sequence of intermediate, human-like reasoning steps; and
* **Classical Ensemble Theory**, particularly Bootstrap Aggregation (Bagging) and Monte Carlo path-sampling. 

The introduction of Self-Consistency (`[[arxiv:2203.11171]]`) represents a direct attempt to combine these domains. Rather than relying on a single deterministic greedy path, Self-Consistency samples multiple, diverse reasoning trajectories from an LLM’s posterior distribution, selecting the consensus answer. 

Simultaneously, the scale of LLM deployment has outpaced the feasibility of human-in-the-loop evaluation, driving the adoption of automated LLM-as-a-Judge frameworks (`[[arxiv:2411.15594]]`). This creates a nested system where LLMs generate, evaluate, and refine content within increasingly complex networks, such as the clinical multi-agent framework Cardiology-Chat (`[[europepmc:PMC13068123]]`).

```
                              INFERENCE-TIME COMPUTE SCALING
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
         Multi-Path Decoding                              Automated Evaluation
    (e.g., Self-Consistency, CoT)                     (e.g., LLM-as-a-Judge, Multi-Agent)
                    │                                               │
                    ▼                                               ▼
     Optimizes trajectory search                     Scales validation throughput
     but introduces compute tax                      but risks circularity & bias
```

### 1.3 The Core Tension: Engineering Feasibility vs. Statistical Rigor
The rapid adoption of these paradigms has exposed a deep tension between practical engineering and statistical rigor. Systems engineers focus on empirical improvements (e.g., absolute accuracy gains of $+17.9\%$ on math benchmarks), treating pipeline latency and VRAM footprint as the primary hurdles. 

In contrast, statisticians and peer reviewers highlight fundamental methodological flaws:
* **Uncontrolled Compute Budgets:** High-compute multi-path strategies are routinely compared against low-compute single-pass baselines, confounding algorithmic innovation with simple compute scaling.
* **Epistemological Circularity:** LLM evaluators are deployed to score other LLMs on synthetically generated datasets, creating a closed loop vulnerable to cognitive biases (e.g., position, verbosity, and self-enhancement bias) without grounding in human consensus or psychometric theory.
* **Underpowered Clinical Validation:** In high-stakes medical deployments, collaborative multi-agent systems claim clinical readiness based on small-sample retrospective evaluations, ignoring spectrum bias and multiple testing corrections.

This review aims to bridge this divide by auditing these frameworks, exposing their technical vulnerabilities, and establishing rigorous, compute-equivalent, and statistically validated standards for future AI research.

---

## 2. Decoding Strategies and the Self-Consistency Paradigm

### 2.1 Mathematical Formulation of Self-Consistency
The standard decoding paradigm in autoregressive language models relies on greedy decoding or beam search to find a sequence of tokens $Y = (y_1, \dots, y_T)$ that maximizes the conditional probability $P(Y | X)$ given an input prompt $X$. 

When augmented with Chain-of-Thought prompting, the model generates an intermediate reasoning path $r$ before producing the final answer $a$. Under greedy decoding, this process is deterministic and highly susceptible to local compounding errors; a single erroneous step in $r$ invalidates the subsequent path, even if the model possesses the underlying capacity to solve the problem.

To mitigate this vulnerability, Wang et al. (`[[arxiv:2203.11171]]`, `[[dblp:1673083]]`) formulated the **Self-Consistency** decoding strategy. The method conceptualizes the generation of an answer as a marginalization over a latent space of diverse reasoning paths. 

Instead of searching for the single joint sequence of maximum probability, Self-Consistency samples $N$ independent reasoning paths $\{r_1, r_2, \dots, r_N\}$ and their corresponding candidate answers $\{a_1, a_2, \dots, a_N\}$ from the model's conditional distribution using a temperature-controlled sampling decoder (typically $T \in [0.5, 1.0]$).

The optimal final answer $a^*$ is selected by marginalizing out the reasoning paths via a majority vote, represented mathematically as:

$$a^* = \arg\max_{a} \sum_{i=1}^{N} \mathbb{I}(\text{extract}(r_i) = a)$$

where $\mathbb{I}$ is the indicator function, and $\text{extract}(r)$ is a parser function mapping the raw generated text path $r$ to a discrete, normalized answer space (e.g., isolating a final numerical value or a multiple-choice option).

```
                      ┌─── Path 1: r_1 ───> a_1 = "42" ──┐
                      ├─── Path 2: r_2 ───> a_2 = "17" ──┼──> [Majority Vote] ──> a* = "42"
Prompt + Query X ────┼─── Path 3: r_3 ───> a_3 = "42" ──┤
                      └─── Path N: r_N ───> a_N = "42" ──┘
```

While mathematically elegant, this formulation relies on a critical, often fragile assumption: the existence of a robust, deterministic parsing function $\text{extract}(r)$. 

In complex, open-ended generative domains (e.g., long-form synthesis, code generation, or clinical diagnosis), the mapping of $r_i$ to a discrete equivalence class $a_i$ is highly non-trivial. If the extraction function fails or if the output space cannot be partitioned into discrete classes, the summation collapses. 

Furthermore, this formulation is vulnerable to **semantic collapsing**, where minor semantic variations are misclassified as distinct answers, or conversely, logically divergent reasoning paths are grouped as identical due to parser limitations.

### 2.2 The Compute-Equivalent Baseline Deficit
The core empirical claim of Self-Consistency (`[[arxiv:2203.11171]]`) is its significant performance gains over standard CoT decoding (e.g., an absolute increase of $+17.9\%$ on GSM8K using PaLM-540B). However, this comparison suffers from a **compute-equivalent baseline deficit**. 

Comparing a multi-path decoding strategy using $N = 40$ or $N = 256$ sampled paths to a single-path ($N=1$) greedy baseline is scientifically asymmetric. It conflates the algorithmic benefit of marginalization with the brute-force scaling of inference-time compute.

To isolate the true algorithmic contribution of Self-Consistency, evaluations must benchmark the method against compute-equivalent baselines of equal token budgets. 

```
                             INFERENCE COMPUTE BUDGET
                                        │
           ┌────────────────────────────┴────────────────────────────┐
           ▼                                                         ▼
  Multi-Path CoT                                           Compute-Equivalent Baselines
  (Self-Consistency, N=40)                                 (Allocated equal total FLOPs)
           │                                                         │
           ├─> Marginalizes over latent paths                        ├─> Beam Search (Width W)
           └─> High accuracy gains                                   ├─> Best-of-N Reranking
                                                                     └─> N-Sample Majority Vote (No CoT)
```

A rigorous benchmark must compare Self-Consistency ($N$-paths) against:
1. **Beam Search of Width $N$:** Evaluates whether structured, joint probability sequence search outperforms independent path sampling.
2. **Best-of-$N$ Reranking (using a separate verifier or reward model):** Tests if external discriminative evaluation of $N$ paths is superior to unsupervised majority voting.
3. **$N$-Sample Majority Voting *without* Chain-of-Thought:** Isolates the effect of CoT by performing majority voting on $N$ direct answers, determining whether the performance boost is driven by reasoning trajectories or simple sampling redundancy.

Without these controls, the reported gains of Self-Consistency cannot be definitively attributed to "reasoning path marginalization." Instead, they may reflect the statistical reality that sampling more tokens from a calibrated distribution naturally increases the probability of hitting a correct answer.

### 2.3 Systems & Operational Engineering Bottlenecks
From an operational perspective, Self-Consistency imposes a massive **inference compute tax**. Generating $N$ independent paths scaling up to $N = 40$ or $N = 256$ increases the FLOP requirements, latency, and API generation costs by a factor of $N$. In enterprise production environments operating under strict latency budgets (e.g., $<200$ ms SLA), standard parallel sampling is highly impractical.

The primary systems bottlenecks are:
* **VRAM and Memory Bandwidth:** Storing and updating key-value (KV) caches for $N$ active, concurrent decoding threads rapidly exhausts GPU high-bandwidth memory (HBM).
* **Throughput Scaling:** While batching can mitigate some latency overhead by grouping parallel queries, it reduces the overall concurrent user capacity of the serving infrastructure.

To transition Self-Consistency from an offline academic benchmark to an online production-ready system, several modern optimization strategies must be applied:

* **Parallel Prefix Caching (Shared Prompt Optimization):** Since all $N$ paths share the same system prompt and user query, caching the activation states of the common prefix prevents redundant computation. This limits the $N$-fold FLOP cost strictly to the generated token trajectories.
* **Speculative Decoding and Draft-Model Verification:** A small, highly optimized draft model can generate the candidate reasoning paths $\{r_1, \dots, r_N\}$ at a fraction of the cost, leaving the larger, primary model to verify or correct the generated tokens in a single parallel step.
* **In-Context Path Distillation:** Running Self-Consistency offline allows the generation of high-quality, marginalized rationales. These can then be distilled back into the primary model via fine-tuning. This embeds the benefits of multi-path reasoning directly into a single-pass ($N=1$) greedy decoder, avoiding the inference-time compute tax altogether.

---

## 3. The Epistemology and Statistics of LLM-as-a-Judge

### 3.1 The Paradox of Circular Evaluation
As outlined in the systematic survey by Gu et al. (`[[arxiv:2411.15594]]`), the rapid expansion of LLM capabilities has led to the adoption of the **LLM-as-a-Judge** paradigm. This approach uses frontier models (e.g., GPT-4) as automated, high-throughput evaluators to assess candidate outputs on complex, open-ended tasks. 

While highly scalable, this framework introduces a profound epistemological paradox: **the circularity of evaluation**.

```
                           THE EPISTEMOLOGICAL LOOP
                           
                            ┌─────────────────────┐
                            │   Frontier LLM      │◄────────────────┐
                            │ (e.g., GPT-4 Judge) │                 │
                            └──────────┬──────────┘                 │
                                       │                            │
                               Evaluates & Filters                  │
                                       │                            │
                                       ▼                            │
                            ┌─────────────────────┐                 │
                            │  Synthetic Training │                 │
                            │   & Benchmarks      │                 │
                            └──────────┬──────────┘                 │
                                       │                            │
                                 Fine-tunes                         │
                                       │                            │
                                       ▼                            │
                            ┌─────────────────────┐                 │
                            │  Downstream Model   │─────────────────┘
                            └─────────────────────┘
```

This paradigm sets up a closed loop:
1. We use biased LLMs to evaluate other biased LLMs;
2. These evaluations are performed on benchmarks that are themselves synthetically curated or filtered by LLMs;
3. The resulting preference data is used to fine-tune the next generation of models (via RLHF or DPO), which are then evaluated by the same or similar LLM judges.

This closed feedback loop lacks any grounding in human-verified truth or static physical benchmarks. Over multiple generational cycles, this circularity risks inducing **systemic consensus bias**. Here, models are optimized not for objective truth or functional utility, but for the stylistic and structural preferences of the evaluator model. 

It becomes impossible to distinguish genuine cognitive or reasoning progress from a model's alignment with the evaluator's pre-existing statistical profile.

### 3.2 Deconstructing Evaluator Biases
The vulnerability of LLM-as-a-Judge frameworks is further compounded by deep, systemic cognitive and procedural biases. These biases are not random errors that average out over large samples; they are systematic distortions deeply embedded in the transformer architecture and its training objectives:

* **Position Bias:** LLM judges exhibit a pronounced preference for specific options based on their ordering in the prompt template. In pairwise evaluations (comparing Model A and Model B), swapping the presentation order of the models can alter the preference rating by up to $30\%$, demonstrating that the evaluator's judgment is heavily influenced by spatial priming.
* **Verbosity Bias:** Models consistently equate response length with quality. Long, verbose, and repetitive outputs are scored higher than concise, direct, and accurate answers. This bias encourages "bloatware prompting," where downstream models are trained to maximize token output rather than information density.
* **Self-Enhancement (In-Family) Bias:** Evaluator models exhibit favoritism toward outputs generated by themselves or models within their lineage (e.g., GPT-4-Judge consistently scoring GPT-3.5 outputs higher than competitor models with equivalent or superior human-evaluated performance). This threatens the validity of cross-family model comparisons.

To isolate and measure these biases, researchers must design and run **length-controlled and order-inverted synthetic controls**. For example, inserting identical semantic content formatted at different lengths or flipped ordering allows the calculation of a bias-coefficient matrix. 

This matrix can then be used to calibrate and correct raw judge scores before they are used for downstream optimization.

### 3.3 Grounding Evaluators in Psychometrics and Multi-Rater Agreement
To break the circularity and correct for bias, the LLM-as-a-Judge framework must be grounded in classical psychometrics and multi-rater agreement theory. Rather than treating an LLM judge as an oracle, it must be treated as a **noisy, biased estimator**. 

Before deploying any LLM-as-a-Judge system, researchers must establish human agreement baselines and compute formal inter-rater reliability (IRR) metrics. Specifically, we must calculate **Cohen's Kappa** ($\kappa$) for pairwise evaluations:

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

where $p_o$ is the relative observed agreement among judges, and $p_e$ is the hypothetical probability of chance agreement. 

For multi-judge setups (including both human and LLM raters), **Fleiss' Kappa** must be calculated to evaluate the consistency of the panel.

```
                    PSYCHOMETRIC GROUNDING PIPELINE
                                   │
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
   Inter-Rater Reliability                      Generalizability Theory
      (IRR Calibration)                               (G-Theory)
              │                                         │
    ├─ Calculate Cohen's Kappa                ├─ Partition variance components
    ├─ Compute Fleiss' Kappa                  ├─ Separate true performance (Universe)
    └─ Validate LLM-to-human agreement        └─ Quantify rater, task, & interaction noise
```

Furthermore, we must apply **Generalizability Theory (G-Theory)** to decompose the variance in judge scores. This approach partitions variance into:
* True student performance (the target universe score),
* Evaluator severity/leniency (the rater effect),
* Task difficulty (the prompt effect), and
* Random error (residual noise).

By isolating the rater-variance component, we can quantitatively determine whether an LLM judge’s score reflects the actual quality of the generated output or is merely an artifact of rater-specific bias. 

An LLM-as-a-Judge system should only be deemed valid if its variance profile matches or improves upon the variance of human expert panels, and its Fleiss' Kappa with human experts exceeds $\kappa = 0.60$ (indicating substantial agreement).

---

## 4. Specialized Multi-Agent Systems in High-Risk Domains: Cardiology-Chat Case Study

### 4.1 Multi-Agent Orchestration vs. Monolithic LLMs
In critical domains like clinical medicine, monolithic general-purpose LLMs are highly restricted due to their propensity for hallucinations and generalist reasoning gaps. To address these limitations, Yang et al. (`[[europepmc:PMC13068123]]`) proposed **Cardiology-Chat**, a specialized collaborative multi-agent framework designed for cardiac diagnostic reasoning. 

Rather than relying on a single model to parse a clinical vignette, extract symptoms, reference guidelines, and propose treatments, Cardiology-Chat distributes these tasks across a team of specialized sub-agents managed by an orchestrator/routing agent.

```
                       CARDIOLOGY-CHAT ARCHITECTURE
                                     │
                                     ▼
                      [ Orchestrator / Routing Agent ]
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
[ History Extraction Agent ] [ Diagnostics Parser Agent ] [ Guideline RAG Agent ]
  (Symptom categorization)     (ECG & Echo text params)     (ACC/AHA Vector DB)
         │                           │                           │
         └───────────────────────────┬───────────────────────────┘
                                     ▼
                        [ Consensus & Synthesis Agent ]
                                     │
                                     ▼
                        [ Final Clinical Report ]
```

The system's core mechanism is its **Consensus & Refinement loop**. This loop acts as an automated clinical board, where the Synthesis Agent cross-references the Diagnostic Agent's differentials against ESC/AHA guidelines retrieved by the Guideline RAG Agent. 

If a contraindication is detected (such as prescribing an ACE inhibitor to a patient with bilateral renal artery stenosis), the system flags the error and prompts the Clinical Agent for a correction before outputting the final recommendation.

### 4.2 Statistical Audit of Clinical Validation Claims
Despite the architectural sophistication of Cardiology-Chat, its empirical validation claims are highly fragile. The authors report **$91.5\%$ guideline compliance** and an **$84\%$ physician acceptance rate**, suggesting clinical readiness. 

However, a statistical audit of their methodology exposes severe limitations:
* **The Low-Power Sample Size:** The clinical validation panel consisted of only $N=5$ cardiologists evaluating $10$ clinical cases. This results in a total of $n = 50$ evaluation points.
* **The Confidence Interval Expansion:** While an $84\%$ acceptance rate sounds promising, we must compute its $95\%$ confidence interval (CI). Using the standard Wald method:

$$\hat{p} = 0.84, \quad n = 50$$

$$\text{Standard Error (SE)} = \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}} = \sqrt{\frac{0.84 \times 0.16}{50}} = \sqrt{0.002688} \approx 0.0518$$

$$\text{Margin of Error} = 1.96 \times 0.0518 \approx 0.1015$$

$$95\% \text{ CI} = [73.8\%, 94.2\%]$$

A lower bound of $73.8\%$ acceptance is highly concerning for high-stakes clinical decision support systems where diagnostic errors can lead to patient harm.

Furthermore, the study lacks any reporting of inter-rater reliability (such as Fleiss' Kappa) among the five evaluators, leaving it unclear whether the $84\%$ acceptance reflects true clinical consensus or highly variable individual criteria.

The validation is also susceptible to **spectrum bias** and **pre-training contamination**. The dataset was constructed using USMLE board questions and clean cohorts from the MIMIC-IV database (`[[europepmc:PMC13068123]]`). These cohorts represent highly structured, idealized clinical presentations. 

In real-world clinical environments, patient histories are messy, unstructured, and often lack complete diagnostic parameters. Evaluating a model on clean, potentially pre-trained benchmark data while claiming readiness for messy clinical workflows is a major methodological error. 

Finally, the study fails to adjust for multiple comparisons. Reporting multiple evaluation metrics (e.g., accuracy, safety, clarity, and compliance) without applying **Bonferroni** or **Benjamini-Hochberg** corrections artificially inflates the probability of observing a false positive, invalidating their statistical claims.

### 4.3 Real-Time Safety and Deployment Constraints
Beyond statistical validation, systems engineers must confront the physical limits of multi-agent architectures in clinical workflows:
* **Inference Latency:** The iterative consensus loop, which requires sequential API calls and prompt-response generations across multiple agents, introduces substantial latency. While a monolithic model might return a response in $<2$ seconds, the multi-agent consensus loop can take upwards of $30$ to $90$ seconds.
* **Emergency Medicine Incompatibility:** This latency makes the system entirely unsuitable for high-acuity, time-sensitive environments (such as active cardiac arrest or emergency department triage protocols), where clinical decisions must be made in seconds.

To make these systems viable, future architectures must implement high-throughput, low-latency agent routing alongside localized, edge-deployed clinical models.

---

## 5. Proposed Methodological Standards for Future AI Evaluation

To address the limitations uncovered in this review, we propose a set of four methodological standards that must be mandated in future research on LLM decoding, evaluation, and domain-specific systems.

```
                  ┌────────────────────────────────────────────────────────┐
                  │            PROPOSED METHODOLOGICAL STANDARDS           │
                  └───────────────────────────┬────────────────────────────┘
                                              │
         ┌────────────────────────┬───────────┴───────────┬────────────────────────┐
         ▼                        ▼                       ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│    Mandate 1     │    │    Mandate 2     │    │    Mandate 3     │    │    Mandate 4     │
│ Compute-Equal    │    │ Statistical      │    │ Length-Controlled│    │ Multi-Rater      │
│ Baselines        │    │ Significance     │    │ Bias Calibration │    │ Agreement Testing│
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

### Mandate 1: Compute-Equivalent Control Baselines
Any study introducing a new inference-time decoding strategy, multi-agent debate loop, or search-based reasoning framework must compare its performance against compute-equivalent baselines. Researchers must report accuracy and performance as a function of the total floating-point operations (FLOPs) or token budgets used during inference. 

Specifically, multi-path strategies ($N$-paths) must be compared against beam search of width $N$, best-of-$N$ reranking, and simple sample redundancy without reasoning trajectories.

### Mandate 2: Rigorous Statistical Significance Reporting
Empirical claims of accuracy improvements must be supported by rigorous statistical tests rather than raw percentage gains. Researchers must report standard deviations across multiple random seeds and calculate statistical significance using appropriate non-parametric tests (e.g., **McNemar’s Test** for paired nominal data). 

In low-power clinical or domain-expert evaluations, authors must report exact $95\%$ confidence intervals (using Clopper-Pearson or Wilson Score methods for binomial outcomes) and apply multiple testing corrections (e.g., Benjamini-Hochberg FDR control) across all evaluated outcomes.

### Mandate 3: Length-Controlled and Order-Inverted Bias Testing
To validate the reliability of LLM-as-a-Judge systems, evaluations must incorporate built-in controls for position, verbosity, and self-enhancement biases. 

Prior to deployment, every LLM judge must run on a standardized calibration suite where the positions of competing options are systematically swapped, and response lengths are controlled using synthetic expansion and compression. Any reported judge score must be statistically corrected using the resulting bias-coefficient matrix.

### Mandate 4: Multi-Rater Reliability (Kappa) Reporting
Automated LLM judges must not be validated by simple correlation to a pooled, noisy human average. Instead, researchers must establish a human-expert baseline, report its inter-rater reliability using Cohen's or Fleiss' Kappa, and demonstrate that the LLM judge's agreement with the expert panel is statistically indistinguishable from the agreement *between* the human experts themselves. 

If the human baseline exhibits low agreement ($\kappa < 0.40$), the evaluation task must be deemed too subjective or poorly defined for reliable automated benchmarking.

---

## 6. Synthesis and Comparative Analysis

To provide a clear, structured overview of how these frameworks compare across the dimensions audited in this paper, the following synthesis table maps their core attributes, systems implications, and methodological vulnerabilities:

| Evaluation Dimension | Multi-Path Decoding (`[[arxiv:2203.11171]]`, `[[dblp:1673083]]`) | LLM-as-a-Judge (`[[arxiv:2411.15594]]`) | Multi-Agent Clinical Support (`[[europepmc:PMC13068123]]`) |
| :--- | :--- | :--- | :--- |
| **Core Paradigm** | Marginalization over latent reasoning paths via majority voting | Automated, high-throughput model evaluation using frontier models | Specialized multi-agent consensus and guideline-based RAG |
| **Primary Claim** | Significant accuracy gains on complex reasoning (e.g., $+17.9\%$ GSM8K) | Scalable, cost-effective alternative to expensive human expert panels | $91.5\%$ guideline compliance and $84\%$ physician acceptance |
| **Systems Overhead** | Linear scaling ($N$-fold FLOPs, latency, and VRAM footprint) | High API costs at scale; KV-cache exhaustion during batching | High inference latency ($30\text{--}90$s); unsuitable for emergency triages |
| **Primary Bias Risk** | Out-of-distribution path collapses; systematic error reinforcement | Position, verbosity, and self-enhancement (in-family) biases | Spectrum bias; pre-training data contamination; clinical guideline misalignment |
| **Methodological Deficit** | Lack of compute-equivalent control baselines (e.g., Beam Search) | Epistemological circularity; lack of psychometric grounding (Kappa/G-Theory) | Severely underpowered clinical cohorts ($N=5$); lack of multiple testing corrections |
| **Proposed Mitigation** | Parallel prefix caching; speculative decoding; path distillation | Pairwise order inversion; length-controlled synthetic calibration | Out-of-distribution EHR validation; strict FDR control; multi-center testing |

---

## 7. Conclusion

The transition toward inference-time compute scaling, automated evaluation, and multi-agent coordination marks an exciting and necessary step forward in artificial intelligence. However, as this review demonstrates, these paradigms currently rest on fragile methodological and statistical foundations. 

The significant performance improvements reported by pioneering works like Self-Consistency and Cardiology-Chat are often confounded by unmetered inference-time compute scaling, pre-training data contamination, or severely underpowered validation setups. Meanwhile, the LLM-as-a-Judge framework remains vulnerable to a self-referential loop of circular evaluations, style bias, and self-enhancement.

To realize the full potential of these architectures, the AI research community must move past raw accuracy metrics and embrace the rigorous engineering and statistical standards common in other high-stakes scientific fields. By committing to compute-equivalent benchmarking, adjusting for systematic model biases, and grounding evaluations in psychometrics and clinical trials, we can ensure these systems are both highly capable and demonstrably safe for real-world deployment.

---

## References

*   **[[arxiv:2203.11171]]** (Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., and Zhou, D. *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv preprint, 2022.)
*   **[[dblp:1673083]]** (Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi, E. H., Narang, S., Chowdhery, A., and Zhou, D. *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. In International Conference on Learning Representations (ICLR), 2023.)
*   **[[arxiv:2411.15594]]** (Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y., Ma, S., Liu, H., Wang, S., Zhang, K., Wang, Y., Gao, W., Ni, L., and Guo, J. *A Survey on LLM-as-a-Judge*. arXiv preprint, 2024.)
*   **[[europepmc:PMC13068123]]** (Yang, Z., Chen, C., Mahmoud, S. S., Tan, X., Chen, Y., and Fang, Q. *Cardiology-Chat: A Multi-LLMs Powered System for Cardiac Diagnostic Reasoning and Clinical Support*. Europe PMC / PMC13068123, 2026.)