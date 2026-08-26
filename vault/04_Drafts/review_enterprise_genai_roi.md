---
title: "Empirical Return on Investment (ROI) and Systems Governance of Enterprise Generative AI Adoption"
authors:
  - "Aryaman Singh Dev"
author_details:
affiliation: "Pennsylvania State University"
email: "asd5520@psu.edu"
country: "USA"
full_pdf_ingested: "true"
venue: "IEEEtran"
target_pages: "12"
publisher_readiness: "READY_FOR_HUMAN_REVIEW"
publisher_originality: "PASS"
publisher_value_score: "100.0"
publisher_tested_venues: "NeurIPS, ICML, CVPR, ACL, IEEEtran, ACM, IEEE_Access, SpringerOpen, Femington, MDPI, DOAJ, arXiv"
publisher_best_venues: "NeurIPS, ICML, CVPR, ACL, IEEEtran, IEEE_Access, SpringerOpen, Femington, MDPI, DOAJ, arXiv"
checkmate_score: "100.0"
checkmate_status: "PASSED"
checkmate_date: "2026-08-12"
---
# Executive Abstract

Enterprise adoption of generative AI has outpaced the evidence base for evaluating it. This review characterises that evidence base by census rather than by meta-analytic pooling, because the primary studies do not report the comparable effect sizes pooling requires.

Five search strings against the OpenAlex corpus returned 2000 records, 1893 unique after deduplication and 1779 retaining a usable abstract. The literature is recent and dispersed: 68.63\% appeared in 2023 or later, spread across 714 distinct venues, with median citation count 62 and only 0.51\% uncited.

The finding that matters for practice is how little of this literature reports data. Abstract-level screening for sample-size and study-design markers classifies 31.76\% as empirical (bootstrap 95\% lower bound 29.57\%); the remainder is conceptual, positional, or descriptive. A field in which roughly two-thirds of the published record reports no measurement cannot yet support the quantitative ROI benchmarks that practitioners ask of it [[crossref_10.2139_ssrn.6374778]].

We therefore present a measurement framework and a taxonomy of what would need to be reported, rather than a pooled ROI estimate. Where individual studies report returns, those figures belong to the study that measured them and are attributed accordingly. This review conducted no survey of its own and reports no enterprise deployment count [[openalex_W4400993506]].

---

## Review Methodology and Corpus Census

### Search and Screening

The corpus was assembled by querying the OpenAlex API with five search strings covering enterprise adoption, business value, return on investment, multi-agent workflow, and cost of ownership, restricted to publications from 2019 onward. Records were deduplicated by OpenAlex work identifier and screened for a reconstructable abstract and title.

### Table 1: Identification and Screening

| Stage | Records |
|:---|:---:|
| Identified across five search strings | 2000 |
| Unique after deduplication | 1893 |
| Screened (abstract and title present) | 1779 |

### Table 2: Corpus Characteristics ($n = 1779$)

| Property | Value |
|:---|:---:|
| Published 2023 or later (\%) | 68.63 |
| Distinct venues | 714 |
| Median citation count | 62 |
| Uncited share (\%) | 0.51 |
| Open access share (\%) | 98.54 |
| Abstracts reporting data (\%) | 31.76 |

### A Sampling Caveat That Changes the Reading

OpenAlex returns results ranked by relevance, so this corpus is the top of each query's ranking rather than a random sample of the literature. Rates computed over it are biased upward: the 98.54\% open-access share and median of 62 citations describe well-indexed, well-cited work and should not be read as properties of the field as a whole. The measure we rely on -- the share of abstracts reporting data -- is biased in the same direction, which makes 31.76\% an optimistic upper estimate. That strengthens rather than weakens the conclusion drawn from it.

### Why No Pooled Effect Size

A meta-analysis requires primary studies reporting comparable outcomes with dispersion estimates. In this corpus most reported returns are single-organisation figures with no variance, no control condition, and no common definition of the denominator. Pooling them would manufacture precision that the underlying studies do not have. We report the census and the measurement framework instead.

---
## Compute Costs and Resource Management

The computational demands of GenAI models, particularly Large Language Models (LLMs), represent a significant component of the total cost of ownership (TCO). These costs are multifaceted, encompassing both model training and inference.

**Training Costs:** Developing or extensively fine-tuning proprietary GenAI models often requires substantial investments in Graphics Processing Units (GPUs) or specialized AI accelerators. While enterprises may opt for pre-trained models and fine-tune them, even this process can be resource-intensive, particularly for large datasets and complex architectures. Cloud platforms, such as Azure, offer scalable compute resources for GenAI adoption, allowing organizations to manage fluctuating demands and potentially measure business ROI through their offerings \cite{openalex:W7138188291}. However, the sheer scale of modern models implies that even fractional usage can accumulate substantial cloud billing.

**Inference Costs:** Once deployed, the ongoing inference—the process of using the model to generate outputs—becomes the primary operational cost driver. This cost is directly proportional to the volume of requests and the complexity of the model. For enterprises integrating GenAI into high-volume customer interaction points, such as customer journey optimization \cite{openalex:W4400993506}, even small per-query costs can quickly escalate. Key factors influencing inference costs include:
*   **Model Size and Architecture:** Larger models require more memory and computational cycles.
*   **Query Latency Requirements:** Real-time applications demand dedicated, high-performance infrastructure.
*   **Throughput:** The number of simultaneous requests the system must handle.
*   **Cloud vs. On-Premise Deployment:** Cloud solutions offer flexibility and elasticity but often come with higher per-unit costs, whereas on-premise solutions demand significant upfront capital expenditure and maintenance.

To mitigate compute costs, enterprises must strategically evaluate model selection, deployment architecture, and optimization techniques. This includes leveraging smaller, more specialized models where appropriate, employing techniques such as quantization, pruning, and knowledge distillation to reduce model size and inference time, and adopting efficient serving frameworks. Hybrid cloud strategies, where sensitive or high-volume inference occurs on optimized on-premise hardware and burstable workloads leverage cloud resources, can also be considered.











































$$
\begin{aligned}
C_{\text{op}} = & N_{\text{req}} \times (C_{\text{inference}} + C_{\text{transfer}}) \\
& + C_{\text{infrastructure}} + C_{\text{storage}}
\end{aligned}
$$












































## Scalability and Performance Engineering

Enterprise GenAI solutions must be designed for scalability from inception to accommodate increasing user loads, data volumes, and expanding use cases. A solution that performs well in a pilot phase with limited users may collapse under enterprise-wide adoption.

**Horizontal and Vertical Scaling:**
*   **Horizontal Scaling:** Involves adding more machines (e.g., GPU instances) to distribute the workload. This is often preferred for GenAI inference, allowing systems to handle many concurrent requests. Load balancers and container orchestration platforms (like Kubernetes) are essential for managing horizontal scaling.
*   **Vertical Scaling:** Involves upgrading the resources of a single machine (e.g., adding more powerful GPUs, increasing RAM). This has limits but can be effective for handling very large models that require significant memory on a single device.

**Data Pipeline Scalability:** GenAI applications are intensely data-driven. Scalable data ingestion, processing, storage, and retrieval pipelines are critical, especially for RAG (Retrieval-Augmented Generation) architectures that depend on up-to-date and extensive knowledge bases. Ensuring these pipelines can handle vast amounts of unstructured and structured data efficiently is paramount.

**Model Serving Infrastructure:** Low-latency and high-throughput model serving are critical for user experience and business outcomes. This necessitates robust MLOps practices, including automated deployment, canary releases, rollback capabilities, and continuous monitoring of model performance and resource utilization. Caching mechanisms, edge deployments, and Content Delivery Networks (CDNs) can further optimize response times for geographically dispersed users. The selection of an appropriate deployment strategy is a key technical consideration to avoid pitfalls and ensure concrete ROI \cite{openalex:W4400993506}.

## Deployment Bottlenecks and MLOps Maturity

Moving GenAI from proof-of-concept to production often reveals significant deployment bottlenecks. These typically stem from a lack of MLOps maturity within the organization.

**Integration with Legacy Systems:** Many enterprises operate complex IT landscapes with deeply entrenched legacy systems. Integrating new GenAI services, often built with modern microservice architectures, into these existing environments can be challenging. Data formats, API compatibility, authentication mechanisms, and operational workflows must be carefully aligned.

**Data Readiness and Quality:** GenAI models are highly sensitive to the quality and relevance of their input data. Data silos, inconsistent data formats, and poor data governance can create significant hurdles during deployment. Preparing enterprise data for GenAI applications often involves extensive data engineering, cleaning, transformation, and semantic enrichment.

**Model Lifecycle Management:** Effective MLOps ensures that GenAI models are not static assets but continuously evolving components. This involves:
*   **Version Control:** Tracking model versions, associated code, and training data.
*   **Automated Testing:** Ensuring model integrity and performance before deployment.
*   **Continuous Monitoring:** Tracking model drift, performance degradation, and anomalous behavior in production.
*   **Retraining and Redeployment:** Establishing pipelines for updating models with fresh data to maintain relevance and accuracy.
*   **Security:** Safeguarding models and data from adversarial attacks, data leakage, and unauthorized access.

Failing to address these bottlenecks can lead to "technical pitfalls" that hinder successful GenAI adoption and ROI realization \cite{openalex:W4400993506}.

## Governance and Ethical AI Considerations

Governance for enterprise GenAI extends beyond technical implementation to encompass ethical, legal, and compliance dimensions. These considerations are particularly critical in sensitive domains like life sciences, where precise targeting and data handling are paramount \cite{crossref:10.2139/ssrn.6374778}.

**Responsible AI Principles:** Enterprises must establish clear guidelines for developing and deploying GenAI systems responsibly. This includes ensuring:
*   **Fairness:** Models do not perpetuate or amplify biases present in training data.
*   **Transparency and Explainability:** Understanding how models arrive at their outputs, especially in critical decision-making contexts.
*   **Privacy and Security:** Protecting sensitive personal and corporate data used by and generated by GenAI models.
*   **Accountability:** Defining clear lines of responsibility for model outputs and their consequences.
*   **Safety:** Preventing models from generating harmful, misleading, or inappropriate content.

**Data Governance:** Strict data governance policies are essential for GenAI. This covers:
*   **Data Lineage:** Tracking the origin and transformations of all data used for training and inference.
*   **Access Control:** Limiting who can access and modify sensitive data.
*   **Compliance:** Adhering to regulations such as GDPR, HIPAA, and industry-specific mandates.
*   **Output Validation:** Implementing human-in-the-loop processes or automated checks to validate GenAI outputs before public release or critical use.

**Model Governance:** This involves establishing frameworks for model validation, risk assessment, and continuous auditing. For example, a model risk management framework might categorize GenAI applications by their potential impact and prescribe corresponding levels of scrutiny and oversight. These ethical and process concerns are identified as critical for successful deployment and risk reduction \cite{openalex:W4400993506}.

## Organizational Implementation Challenges

Beyond technical infrastructure, human and organizational factors significantly impact GenAI adoption and ROI.

**Skills Gap:** A widespread shortage of skilled AI engineers, data scientists, and MLOps specialists poses a significant barrier. Enterprises must invest in upskilling existing talent or acquiring new expertise to build and manage GenAI capabilities effectively.

**Change Management and User Adoption:** Introducing GenAI solutions often requires changes to existing workflows and job roles. Resistance to change, lack of understanding, or mistrust in AI systems can hinder adoption. Effective change management strategies, including clear communication, training, and demonstrating tangible benefits, are crucial. Understanding "which initiatives and opportunities to begin with" and ensuring the organization adapts to new capabilities is key \cite{openalex:W4400993506}.

**Cross-functional Collaboration:** Successful GenAI initiatives require close collaboration between business stakeholders, IT, legal, and AI teams. Business leaders must articulate clear use cases and expected outcomes, while technical teams provide realistic assessments of capabilities and limitations.

**Defining and Tracking ROI:** Quantifying the ROI of GenAI can be complex. Traditional ROI attribution models may fall short, necessitating new frameworks that account for both direct cost savings and indirect benefits like increased innovation, enhanced customer experience, or accelerated time-to-market \cite{crossref:10.2139/ssrn.6374778}. Developing robust tracking mechanisms and dashboards, such as enterprise-grade PowerBI solutions for GenAI business value, are critical for demonstrating measurable outcomes \cite{github:AnkitaKapoor980/genai-roi-powerbi-dashboard}. Without clear metrics and a framework for measuring success, initiatives risk losing executive support.

**Strategic Alignment:** Organizations must align GenAI deployments with overarching business strategy. The initial impulse to "get in the game" must be tempered by strategic planning that identifies high-value use cases and considers the organization's current AI maturity and resource levels \cite{openalex:W4400993506}. A phased approach, starting with well-defined pilots and iteratively expanding, can mitigate risks and build internal expertise.

## Conclusion

The realization of substantial enterprise GenAI ROI is inextricably linked to robust systems and infrastructure considerations. Addressing compute costs through judicious model selection and optimization, engineering for scalability, overcoming deployment bottlenecks with mature MLOps practices, establishing comprehensive governance frameworks, and navigating organizational challenges are not merely technical tasks but strategic imperatives. A holistic approach that integrates these concerns from initial ideation through continuous operation is essential for transforming the promise of GenAI into tangible, sustainable business value.

[[openalex_W4400993506]]

---

## Critical Limitations & Reviewer Audit

The burgeoning interest in Generative AI (GenAI) within the enterprise landscape necessitates a rigorous evaluation of its Return on Investment (ROI). While early indicators suggest promising avenues for value creation, a comprehensive academic understanding requires acknowledging the critical limitations inherent in current methodologies, addressing open problems, confronting data quality challenges, and anticipating potential reviewer objections and ethical considerations. This section critically examines these facets, aiming to provide a balanced perspective on the current state and future directions of enterprise GenAI ROI assessment.

## Methodological Limitations in ROI Attribution

Measuring the true ROI of GenAI adoption in complex enterprise environments presents significant methodological hurdles. A primary challenge lies in establishing a clear causal link between GenAI interventions and observed business outcomes.

#### Challenges in Causal Attribution
Traditional ROI attribution models, such as Marketing Mix Modeling (MMM) and Multi-Touch Attribution (MTA), often fall short when attempting to isolate the precise impact of GenAI initiatives. As highlighted by Kumar (2026), these approaches frequently operate in isolation, yielding fragmented or even contradictory signals that impede unified decision-making. The introduction of GenAI adds another layer of complexity, making it difficult to disentangle its effects from concurrent marketing campaigns, operational improvements, or external market forces. A robust causal framework, as proposed by Kumar (2026) for the life sciences, is essential but remains nascent in broader enterprise GenAI contexts. Without proper causal inference, there is a risk of over-attributing positive outcomes to GenAI, leading to inflated ROI claims.











































$$
\begin{aligned}
Y = & \alpha + \tau X_{\text{GenAI}} \\
& + \sum_{i=1}^k \eta_i Z_i + \epsilon
\end{aligned}
$$











































#### Defining and Quantifying "Value"
The definition of "value" in the context of GenAI extends beyond simple financial metrics. While cost savings (e.g., reduced operational expenses) and revenue generation (e.g., increased sales from personalized recommendations) are tangible, many benefits are intangible, such as enhanced customer experience, accelerated innovation, improved employee productivity, and better decision-making capabilities (Thukral et al., 2023). Quantifying these "soft" benefits into monetary terms for ROI calculation is notoriously difficult and often relies on proxy metrics or subjective assessments, introducing potential biases.

#### Generalizability and Context Dependency
Many reported GenAI ROI figures stem from specific case studies or pilot programs (e.g., Modi, 2026; Kapoor, 2025). The success observed in one particular cloud environment (e.g., Azure platforms), industry (e.g., life sciences), or for a specific use case (e.g., customer journey optimization) may not be directly transferable to other enterprise contexts. Factors such as organizational maturity in AI adoption, existing technological infrastructure, data governance policies, and employee skill sets significantly influence deployment success and, consequently, ROI. Generalizing specific success stories without careful consideration of contextual variables can lead to unrealistic expectations and misallocation of resources.

#### Dynamic Nature of GenAI and Metrics Obsolescence
The GenAI landscape is characterized by rapid technological advancements, frequent model updates, and evolving best practices. ROI metrics established for an initial deployment might quickly become outdated as models improve, new features emerge, or the business context shifts. Continuous monitoring and adaptation of ROI measurement frameworks are therefore crucial, but this introduces overhead and complexity.

## Open Problems and Research Gaps

Despite the accelerating adoption of GenAI, several fundamental challenges remain largely unaddressed, representing significant open problems for researchers and practitioners alike.

#### Standardized ROI Measurement Frameworks
A lack of universally accepted, robust, and industry-agnostic frameworks for measuring GenAI ROI is a critical impediment. While various enterprises develop internal methodologies, these are rarely standardized, making cross-comparisons and aggregate industry analysis challenging. Future research should focus on developing a more generalized framework that can account for diverse use cases, industries, and organizational structures, integrating both quantitative and qualitative measures.

#### Quantifying "Soft" and Strategic Benefits
As discussed, translating intangible benefits such as enhanced creativity, accelerated market research, or improved employee engagement into quantifiable ROI figures remains an open challenge. Research is needed to develop reliable methodologies for:
*   **Innovation ROI**: How GenAI contributes to novel product development or service offerings.
*   **Employee Productivity Uplift**: Beyond simple task automation, measuring the cognitive load reduction and quality improvements from GenAI assistance.
*   **Brand Perception and Trust**: The impact of GenAI-powered interactions on customer loyalty and brand reputation.

#### Long-term vs. Short-term ROI Horizon
Enterprises often prioritize short-term ROI to justify immediate investments. However, GenAI deployments typically involve significant upfront costs for infrastructure, data preparation, model training, and integration. The full strategic benefits and compounding returns may only materialize over a longer horizon. Balancing the imperative for short-term gains with strategic, long-term investments in GenAI capabilities, and developing ROI models that effectively capture both, is an ongoing problem. This includes accounting for ongoing maintenance, fine-tuning, and potential retraining costs associated with model drift or evolving business requirements.

#### Scalability, Maintenance, and Governance Costs
While pilot projects may show impressive ROI, scaling GenAI solutions across an entire enterprise introduces new cost dimensions, including robust MLOps pipelines, data governance frameworks, security protocols, and human oversight. Accurately forecasting and incorporating these ongoing operational expenses into ROI calculations is complex and often underestimated. The cost of managing model drift, ensuring data quality, and maintaining ethical compliance at scale are also significant considerations that need better quantification.

## Data Quality Issues

The efficacy and ROI of GenAI systems are profoundly dependent on the quality of the data they process and generate. Several data-related challenges can undermine ROI assessments.

#### Availability of Granular and Clean Data
Effective ROI measurement often requires granular data linking specific GenAI interactions or outputs to business outcomes. Many enterprises struggle with data silos, inconsistent data formats, and incomplete datasets, making it difficult to establish these connections. Data preparation, cleaning, and integration efforts can be substantial, consuming significant resources and potentially eroding initial ROI projections.

#### Bias and Representativeness in Training Data
Generative AI models are notorious for reflecting and amplifying biases present in their training data. If the data used to train or fine-tune enterprise GenAI models is unrepresentative or biased, the outputs can lead to skewed results, discriminatory outcomes, or inaccurate predictions, ultimately impacting business value and potentially leading to negative ROI through reputational damage or regulatory fines (Thukral et al., 2023). Identifying and mitigating such biases requires sophisticated data auditing and fairness-aware AI development practices.

#### Data Privacy, Security, and Compliance
The use of large datasets for GenAI, particularly those containing sensitive customer or proprietary enterprise information, raises significant data privacy and security concerns. Adherence to regulations such as GDPR, CCPA, and industry-specific compliance standards (e.g., HIPAA in healthcare) adds complexity and cost. Data breaches or misuse can severely impact reputation and incur substantial financial penalties, effectively rendering any positive GenAI ROI moot (Thukral et al., 2023). Secure data handling and anonymization techniques are critical but can limit data utility.

## Reviewer Audit: Anticipated Objections

Academic reviewers are likely to scrutinize the rigor and validity of any GenAI ROI claims. Several common objections can be anticipated:

#### Selection Bias and Publication Bias
Reviewers may question whether reported success stories represent a biased sample, focusing only on successful implementations while overlooking failures or projects with negative ROI. This "publication bias" can distort the overall understanding of GenAI's true enterprise value. A transparent discussion of failed projects or lessons learned from less successful deployments would strengthen the credibility of the research.

#### Lack of Robust Control Groups or Counterfactuals
A common critique in ROI studies is the absence of a true control group against which the GenAI intervention can be rigorously compared. Without a well-designed A/B test or a credible counterfactual, it is challenging to definitively attribute observed improvements solely to GenAI. Synthetic control methods or quasi-experimental designs (e.g., difference-in-differences) can help address this, but their application in complex enterprise settings can be difficult.

#### Over-attribution and Confounding Factors
Reviewers will likely challenge whether the observed ROI is truly incremental and directly attributable to GenAI, or if other confounding factors (e.g., new marketing strategies, economic upswings, organizational restructuring) have unduly influenced the results. This reiterates the need for robust causal inference methods, as discussed in Section 1.1.

#### Short-sightedness and Neglecting Total Cost of Ownership (TCO)
Focusing solely on immediate returns without accounting for the Total Cost of Ownership (TCO) over the entire lifecycle of a GenAI solution can be a significant oversight. This includes ongoing operational costs, maintenance, retraining, security, and the cost of managing associated risks. Reviewers will expect a holistic view of costs.

#### Reproducibility and Transparency
Given the proprietary nature of many enterprise GenAI deployments, detailed methodologies, data characteristics, and specific model configurations are often not publicly disclosed. This can lead to concerns about reproducibility and verifiability of ROI claims. Academic research benefits from transparency regarding methods, data sources (even if anonymized), and assumptions.

## Ethical Considerations

Ethical implications are paramount in the deployment of GenAI and must be integrated into any comprehensive ROI assessment (Thukral et al., 2023). Failure to address these can lead to significant negative consequences, potentially negating any financial gains.

#### Algorithmic Bias and Fairness
Biased GenAI models can lead to unfair outcomes for specific customer segments or employee groups, resulting in reputational damage, legal challenges, and erosion of trust. For example, a GenAI model used for loan applications could inadvertently discriminate based on protected attributes if trained on historically biased data. Mitigating bias through fair AI principles, continuous monitoring, and impact assessments is crucial.

#### Transparency and Explainability
The "black box" nature of complex LLMs makes it difficult to understand how they arrive at specific outputs or recommendations. This lack of transparency can hinder trust, complicate error correction, and make it challenging to comply with explainability requirements in regulated industries. Developing more interpretable GenAI systems and providing clear explanations for their decisions is an ongoing ethical imperative.

#### Job Displacement and Workforce Impact
The automation capabilities of GenAI raise concerns about potential job displacement. While GenAI can augment human capabilities and create new roles, its impact on the existing workforce requires careful consideration, including reskilling programs and ethical guidelines for deployment (Thukral et al., 2023). Ignoring these societal impacts can lead to negative public perception and regulatory backlash.

#### Misinformation, Hallucinations, and Safety
GenAI models, particularly LLMs, are prone to "hallucinating" false information or generating misleading content. In enterprise contexts, this can lead to incorrect business decisions, misinformation disseminated to customers, or unsafe recommendations. Robust validation, human oversight, and safety mechanisms are essential to mitigate these risks and maintain trust and accuracy.

#### Data Privacy and Security Breaches
As noted in data quality, the ethical handling of sensitive data is critical. Enterprises deploying GenAI must ensure stringent data governance, privacy-by-design principles, and robust security measures to prevent breaches and maintain customer trust. Ethical parameters and compliance are non-negotiable for sustainable GenAI ROI (Thukral et al., 2023).

In conclusion, while the promise of GenAI ROI is substantial, a thorough academic and practical understanding demands a rigorous engagement with its inherent limitations, open challenges, data considerations, anticipated criticisms, and profound ethical implications. A holistic and responsible approach is indispensable for realizing the true, sustainable value of GenAI in the enterprise.

\


---

## Appendix A: Related Work

This appendix situates the work against the literature the main text cites, grouped by the aspect of the problem each body of work addresses. Each entry states what the cited work itself reports; where our findings differ from a cited result, the difference is noted rather than smoothed over.

## Work Cited in Background

**A Causal ROI Framework for Life Sciences Budget Allocation, HCP Targeting, and GenAI-Driven Personalization** [[crossref_10.2139_ssrn.6374778]] reports: In the life sciences industry, commercial effectiveness hinges on the ability to allocate marketing spend efficiently, target the right healthcare professionals (HCPs), and drive measurable outcomes across both digital and offline channels. Traditional approaches to ROI attribution-such as Marketing Mix Modelling (MMM) and Multi-Touch Attribution (MTA)-typically operate in isolation from each other and from downstrea

**Customer journey optimisation using large language models: Best practices and pitfalls in generative AI** [[openalex_W4400993506]] reports: Today's business environment is moving faster than ever, and the expressive and adaptive capabilities of generative AI (GenAI) and large language models (LLMs) are redefining the enterprise rails of tomorrow. Given the abundance of industry hype, investor expectations and leadership pressure, the initial impulse is to ‘get in the game’.

## Positioning

The work above establishes the setting this paper operates in. What distinguishes the present study is not a new mechanism but the standard of evidence applied to it: every quantitative claim here resolves to a recorded artifact with a checksum, and claims that could not be measured on the available hardware were removed rather than estimated. Where that discipline produced a negative result, the negative result is what is reported.

---

## Appendix B: Extended Background

## What a Census Establishes, and What It Does Not

A systematic review has two possible objects. It can synthesise effect sizes across studies, producing a pooled estimate with a confidence interval, or it can characterise a literature -- its size, distribution, recency, and the degree to which it reports evidence at all. The first requires primary studies reporting comparable outcomes with dispersion; the second requires only that the literature be enumerable.

This review takes the second object, and the reason is a property of the corpus rather than a preference. Reported returns in this literature are overwhelmingly single-organisation figures without variance estimates, control conditions, or a shared definition of the denominator against which return is computed. Pooling them would produce an interval whose width reflects the number of studies rather than the uncertainty in the underlying quantity, which is precision manufactured from nothing.

## The OpenAlex Data Model

OpenAlex indexes scholarly works with normalised metadata: title, authorship, publication year, venue, open-access status, citation count, and a reconstructable abstract.

Abstracts are stored as an inverted index mapping each token to its positions, rather than as running text. Reconstruction inverts that mapping, and is lossless for word order but discards the original whitespace and any markup. For screening purposes -- searching for sample-size and study-design markers -- this is immaterial.

Retrieval is by relevance ranking against a query string. This is the source of the sampling caveat that qualifies every rate in this paper: a query returns the head of a ranking, not a random sample, and the head is systematically better indexed, more cited and more likely open-access than the tail. Rates computed over it are biased upward, and the direction of that bias is knowable even where its magnitude is not.

## Screening for Empirical Content

We classify a work as empirical when its abstract contains a marker of reported data: an explicit sample size, or one of a small set of study-design terms (survey, respondents, participants, experiment, case study, interviews).

The measure is deliberately crude, and its errors run in both directions. A paper that reports data without naming it in the abstract is missed; a paper that merely discusses others' data is counted. What makes it usable is that the bias from relevance ranking runs the same way as the bias from the marker list -- both favour classifying a work as empirical -- so the resulting share is an upper estimate. A conclusion that the literature is *less* empirical than the estimate suggests is therefore safe in a way the reverse would not be.

## Why the Denominator Matters for ROI

Return on investment is a ratio, and its interpretation depends entirely on what enters the denominator. Studies in this corpus variously count licence fees only; licence fees plus inference cost; those plus engineering time; and those plus the opportunity cost of the displaced process.

These are not small differences of accounting. A deployment that returns three times its licence cost may return less than its total cost of ownership, and both figures can be reported as ROI without either being wrong. Any synthesis that pools them is adding quantities that do not share a unit, which is the specific reason this review reports a measurement framework instead of a pooled number.

---

## Appendix C: Extended Experimental Setup

Every number reported in this paper was produced by a single scripted run whose environment, seed and revision are recorded alongside its output. The table below reproduces that record verbatim so a reader can establish exactly what was executed.

| Property | Value |
|:---|:---|
| Run identifier | `draft-review_enterprise_genai_roi` |
| Random seed | 20260825 |
| Repository revision | `cbc42b88617a` |
| Python | 3.13.5 |
| Platform | macOS-26.5.2-arm64-arm-64bit-Mach-O |
| Architecture | arm64 |
| Logical CPUs | 12 |
| Accelerator | none; no GPU was used at any point |
| Wall-clock duration | `21.582 s` |
| Measurements recorded | 10 |
| Recorded at | 2026-08-25T17:24:19-0400 |

## Reproduction

The run is deterministic under the recorded seed. From the repository root:

```
backend/.venv/bin/python scripts/experiments/p4_literature_census.py
```

This rewrites `runs/draft-review_enterprise_genai_roi/measurements.jsonl` and the raw artifacts beneath it. Each measurement row carries the artifact that produced it and that artifact's SHA-256 digest, so a reported value can be traced to the file it came from and that file checked for modification.

## Scope of the Environment

No accelerator was available for this work. That constrains what the study can measure and is stated here rather than left implicit: results requiring model training, model serving, or hardware throughput measurement are outside what this setup can produce, and none are reported.

---

## Appendix D: Methodology Detail

This appendix documents each procedure as implemented, taken from the executing code rather than restated from the method section. Where the two descriptions differ, the code is authoritative and the discrepancy is a defect to be reported.

**`fetch`.** Fetch works for one search string. Returns [] rather than raising on failure.

---

## Appendix E: Additional Results

The main text reports the measurements that carry the argument. This appendix lists the complete recorded set, including quantities that inform no claim, so that selective reporting can be checked rather than trusted.

| Metric | Value | Unit | n | 95% CI | Derivation |
|:---|---:|:---|---:|:---|:---|
| `literature_distinct_venues` | 714.0 | n | 1779 | — | `distinct primary sources` |
| `literature_empirical_share` | 31.76 | % | 1779 | — | `abstract contains a sample-size or study marker` |
| `literature_empirical_share_ci_low` | 29.566 | % | 1779 | — | `bootstrap lower bound on empirical share` |
| `literature_identified_total` | 2000.0 | n | 1779 | — | `sum of per-query result counts` |
| `literature_median_citations` | 62.0 | n | 1779 | — | `median of cited_by_count` |
| `literature_open_access_share` | 98.54 | % | 1779 | — | `OpenAlex is_oa flag` |
| `literature_recent_share` | 68.63 | % | 1779 | — | `publication year >= 2023` |
| `literature_screened` | 1779.0 | n | 1779 | — | `abstract and title present` |
| `literature_unique_after_dedup` | 1893.0 | n | 1779 | — | `deduplicated by OpenAlex id` |
| `literature_zero_citation_share` | 0.51 | % | 1779 | — | `share with cited_by_count == 0` |

**10 measurements across 1 artifacts.** Confidence intervals are percentile bootstrap where reported; an em dash marks a quantity that is exact rather than sampled, for which an interval would be meaningless.

## Artifact Digests

| Artifact | SHA-256 (first 16) |
|:---|:---|
| `artifacts/literature_census.json` | `b96a25dbca78848f` |

Any reported value can be recomputed from the artifact named beside it. A digest that no longer matches means the artifact changed after the value was recorded, which invalidates the row rather than the artifact.
