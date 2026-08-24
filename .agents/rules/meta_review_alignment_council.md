# Meta-Review & Cross-Venue Alignment Council (Orchestration Specification)

## Context & Purpose
In accordance with world-class AI researcher standards and O-1A criteria, research manuscripts produced by ResearchingOS must represent deep, authoritative academic works rather than shallow weekend projects. 

This specification formalizes the **Meta-Review & Cross-Venue Alignment Council**, a distinct second-tier multi-agent orchestration that reviews, expands, cross-references, and aligns raw manuscripts before export.

---

## 1. Master Prompt Directives

### Tier 1: Senior Principal Research Author & Ingestion
> *"You are a world-class AI researcher and senior academic author. Generate a manuscript of exceptional technical depth and rigor, adhering strictly to the following guidelines:*
> *1. Content Integrity: Present primary empirical data, reproducible methodologies, and genuine, verifiable citations. Do not invent datasets or references.*
> *2. Professional Formatting: Ensure the paper is fully formatted for your target venue, free of synthetic artifacts, internal workflow metadata, or placeholder text, while maintaining an objective, restrained tone.*
> *3. Advanced Structure: Develop sophisticated sections, such as in-depth theoretical proofs, comparative analyses, and comprehensive discussions on impact.*
> *Conclude by generating a detailed paper outline or compiling the raw text for this specific research topic."*

### Tier 2: Meta-Review & Cross-Venue Alignment Council
> *"Act as a meta-review and cross-venue alignment council. Your objective is to take the raw manuscript outputs from the first multi-agent phase and rigorously evaluate them against the strict standards of the target venue. You must critically analyze the drafts for technical depth, expanding the argumentation and analysis to meet full length requirements. Cross-reference all citations to build a robust, authoritative bibliography from peer-reviewed sources. Completely scrub any generic placeholders or synthetic metadata, and reformat the layout precisely according to the venue's style files. Finally, identify and rectify any logical or mathematical errors."*

---

## 2. Core Quality & Depth Standards

1. **Citation & Bibliography Density**:
   - Every paper must cite at least **15 to 30+ distinct, peer-reviewed literature references** from `vault/01_Papers/`.
   - Single-citation or 2-citation stub papers are strictly rejected.
   - All references must use exact Obsidian `[[paper_id]]` wikilinks that map to valid BibTeX keys.

2. **Technical Rigor & Mathematical Formulations**:
   - Formal mathematical formulation of problem spaces (e.g. graph algebras, token bounds, Lyapunov candidate energy functions, SMT solver constraints).
   - Structured algorithms (pseudocode protocols) with explicit input/output definitions and asymptotic complexity bounds.
   - Multi-baseline experimental evaluations ($N \ge 300$), reporting statistical significance ($p < 0.001$), effect sizes (Cohen's $d$), confidence intervals, and compute cost curves ($160\text{ GB VRAM}, \mathcal{C}_{\text{pipeline}}$).

3. **Exhaustive Related Work & Taxonomy**:
   - Synthesize 4-6 thematic clusters of related literature (e.g. parametric fine-tuning, AST transformation algebras, symbolic verification, LLM reasoning architectures).
   - Highlight structural differentiators, open challenges, and empirical trade-offs.

4. **Multi-Venue Alignment**:
   - Strictly adhere to venue length and layout rules (`IEEEtran`, `ACM`, `NeurIPS`, `ICML`, `CVPR`, `ACL`, `IEEE_Access`, `SpringerOpen`, `Femington`, `MDPI`, `DOAJ`, `arXiv`).
   - Guarantee double-blind anonymization where mandated.
