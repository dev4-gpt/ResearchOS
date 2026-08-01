---
title: "Impact and Implications of Generative AI for Enterprise Architects in Agile Environments: A Systematic Literature Review"
authors:
  - "Stefan Julian Kooy"
  - "Jean Paul Sebastian Piest"
  - "Rob Henk Bemthuis"
url: "http://arxiv.org/abs/2510.22003v1"
published: "2025-10-24"
citations: "0"
source: "arXiv"
id: "arxiv:2510.22003"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "systematic-review-&-meta-taxonomy-of-generative-ai-in-enterprise-workflows:-empirical-evidence,-economic-limits,-skill-equalization,-and-task-boundary-frontiers"
---
```obsidian
---
title: "Impact and Implications of Generative AI for Enterprise Architects in Agile Environments: A Systematic Literature Review"
authors:
  - Stefan Julian Kooy
  - Jean Paul Sebastian Piest
  - Rob Henk Bemthuis
source: "http://arxiv.org/abs/2510.22003v1"
publication_date: 2025-10-24
tags:
  - GenerativeAI
  - EnterpriseArchitecture
  - Agile
  - SystematicLiteratureReview
  - Scrum
keywords:
  - Generative AI
  - Enterprise Architect
  - Agile
  - Scrum
  - Systematic Literature Review
abstract: |
  Generative AI (GenAI) is reshaping enterprise architecture work in agile software organizations, yet evidence on its effects remains scattered. We report a systematic literature review (SLR), following established SLR protocols of Kitchenham and PRISMA, of 1,697 records, yielding 33 studies across enterprise, solution, domain, business, and IT architect roles. GenAI most consistently supports (i) design ideation and trade-off exploration; (ii) rapid creation and refinement of artifacts (e.g., code, models, documentation); and (iii) architectural decision support and knowledge retrieval. Reported risks include opacity and bias, contextually incorrect outputs leading to rework, privacy and compliance concerns, and social loafing. We also identify emerging skills and competencies, including prompt engineering, model evaluation, and professional oversight, and organizational enablers around readiness and adaptive governance. The review contributes with (1) a mapping of GenAI use cases and risks in agile architecting, (2) implications for capability building and governance, and (3) an initial research agenda on human-AI collaboration in architecture. Overall, the findings inform responsible adoption of GenAI that accelerates digital transformation while safeguarding architectural integrity.
---

## Claims and Research Questions

The paper primarily aims to clarify whether [[Generative AI]] ([[GenAI]]) can contribute to [[Architectural Agility]] and operational efficiency, and under what conditions.

**Main Research Question (RQ):**
*   How does [[GenAI]] influence the evolving role, skills, and responsibilities of [[Architects]] in large-scale [[Agile Software Development]] environments?

**Sub-Research Questions (Sub-RQs):**
1.  Which technical characteristics of [[GenAI]] create opportunities and challenges for [[Architects]] in [[Agile Environments]]?
2.  Which current [[GenAI]] use cases influence [[Architectural Practices]] and decision making in [[Agile Organizations]]?
3.  How does [[GenAI]] affect traditional roles, tasks, and required skills of [[Architects]] in [[Agile Digital Transformations]]?
4.  What organizational and technological factors influence the adoption trajectory of [[GenAI]] in [[Architecture Practices]]?
5.  What governance and capability adaptations are needed to integrate [[GenAI]] into [[Architecture Practices]]?

## Methodologies

### Study Design
*   **Methodology Type**: [[Systematic Literature Review]] (SLR)
*   **Protocols Followed**: Kitchenham’s guidelines [32] and [[PRISMA]] [43].
*   **Full Protocol**: Available at [45].

### Search Strategy
*   **Databases**: IEEE Xplore and Scopus.
*   **Search Date**: February 17, 2025.
*   **Language**: English-language queries.
*   **Query Focus**:
    *   [[GenAI]] characteristics.
    *   [[Architectural Roles]] and skills.
    *   [[Agile Architecture]].
    *   [[AI Governance]] and adoption.
*   **Query Sets (Table 1 Reference)**:
    *   Q1: "Generative AI" AND agile AND (characteristics OR capabilities OR features OR opportunities OR challenges)
    *   Q2: ("enterprise architect" OR "domain architect" OR "solution architect" OR "business architect" OR "IT architect") AND (role OR task OR skill)
    *   Q3: ("enterprise architect" OR "domain architect" OR "solution architect" OR "business architect" OR "IT architect") AND (agile OR Scrum OR SAFe OR DevOps)
    *   Q4: (("Generative AI" OR "generative artificial intelligence") AND governance) OR ("AI" AND "maturity model")

### Inclusion and Exclusion Criteria (Table 2 Reference)
*   **Inclusion**:
    *   Studies addressing at least one of the RQs.
    *   Subject areas: computer science, software engineering, information systems, management, business.
    *   Publication types: peer-reviewed journals, conference proceedings, workshop papers, book chapters, theses, technical reports.
    *   Publication year: 2018-2025 generally, but 2022-2025 for GenAI-specific work (reflecting recent emergence).
*   **Exclusion**:
    *   Studies focusing on non-GenAI (e.g., rule-based systems, traditional ML, robotics).
    *   Editorials, opinion pieces, keynotes, non-peer-reviewed whitepapers, patents.
    *   Non-English papers.

### Data Extraction and Synthesis
*   Data extracted against the defined [[Research Questions]] (Table 3 Reference).
*   **Analysis Methods**: [[Mapping Analysis]] and [[Thematic Analysis]] to identify cross-study patterns and synthesize findings.

### Quality Assurance
*   Methodological rigor, transparency, and potential biases were assessed [45].

## Experimental Results and Quantitative Benchmarks

### Search and Selection Process (Figure 1 Reference)
*   **Initial Records Found**: 1,697 from IEEE Xplore and Scopus.
*   **Records Excluded after Title Screening**: 1,529.
*   **Records Screened based on Abstract**: 168.
*   **Records Excluded after Abstract Screening**: 96 (including 16 duplicates).
*   **Full-Text Reports Assessed**: 72.
*   **Reports Excluded after Full-Text Assessment**: 39.
*   **Reports Included in the Review**: 33 studies.

### Roles Covered
The 33 selected studies covered various [[Architect]] roles:
*   [[Enterprise Architect]]
*   [[Solution Architect]]
*   [[Domain Architect]]
*   [[Business Architect]]
*   [[IT Architect]]

### Key Findings: GenAI Support Areas
[[GenAI]] most consistently supports [[Architects]] in agile environments across three main areas:
1.  **Design Ideation and Trade-off Exploration**: Assisting in generating multiple design alternatives and evaluating their pros and cons.
2.  **Rapid Creation and Refinement of Artifacts**: Expediting the production and improvement of architectural artifacts (e.g., code, models, documentation).
3.  **Architectural Decision Support and Knowledge Retrieval**: Aiding in informed decision-making and efficient access to relevant architectural knowledge.

### Key Findings: Reported Risks
The review identified several significant risks associated with [[GenAI]] adoption for [[Architects]]:
*   **Opacity and Bias**: Lack of transparency in [[GenAI]] models and potential for perpetuating biases.
*   **Contextually Incorrect Outputs**: Generation of outputs that are technically plausible but contextually inaccurate, leading to rework.
*   **Privacy and Compliance Concerns**: Risks related to data privacy, intellectual property, and regulatory compliance.
*   **Social Loafing**: The tendency for individuals to exert less effort when working in a group (or with AI) than when working alone.

### Key Findings: Emerging Skills and Competencies
To effectively leverage [[GenAI]], architects require new and enhanced skills:
*   [[Prompt Engineering]]: The ability to formulate effective inputs for [[GenAI]] models.
*   [[Model Evaluation]]: Competence in assessing the quality, accuracy, and biases of [[GenAI]] outputs.
*   [[Professional Oversight]]: The critical human judgment and accountability required to supervise [[GenAI]]'s work.

### Key Findings: Organizational Enablers
Successful integration of [[GenAI]] necessitates organizational adjustments:
*   **Readiness**: Organizational preparedness in terms of infrastructure, culture, and capabilities.
*   **Adaptive Governance**: Flexible and evolving governance frameworks to manage [[GenAI]]'s risks and opportunities.

## Stated Limitations

The provided full text content *does not include Section 6* of the paper, which is stated to contain "limitations, and directions for future research." Therefore, explicit limitations acknowledged by the authors cannot be extracted from the given text.

## Contributions

The review offers several key contributions:
1.  A comprehensive mapping of [[GenAI Use Cases]] and associated risks within the context of [[Agile Architecting]].
2.  Identification of implications for [[Capability Building]] and [[AI Governance]] to facilitate responsible [[GenAI]] adoption.
3.  An initial [[Research Agenda]] focusing on [[Human-AI Collaboration]] in [[Architecture]].

Overall, the findings are intended to inform the responsible adoption of [[GenAI]] to accelerate [[Digital Transformation]] while safeguarding [[Architectural Integrity]].
```