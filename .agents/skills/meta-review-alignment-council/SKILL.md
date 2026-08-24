---
name: meta-review-alignment-council
description: Meta-Review & Cross-Venue Alignment Council skill for expanding raw manuscripts into 15-30+ citation authoritative literature reviews with formal proofs, empirical tables, and venue style file compliance.
---

# Meta-Review & Cross-Venue Alignment Council Skill

## Overview
This skill executes the secondary orchestration phase of ResearchingOS. It transforms initial drafts into senior principal-level academic papers by enriching citation networks, deepening theoretical derivations, expanding empirical baselines, and enforcing venue-specific publication constraints.

## Execution Directives

1. **Citation Enrichment Engine**:
   - Query `vault/01_Papers/` to extract all relevant literature notes (across arXiv, Crossref, OpenAlex, DBLP, DOAJ, Europe PMC).
   - Inject minimum 15–30+ authoritative `[[paper_id]]` citations across all major sections (*Introduction, Related Work, Method, System Topology, Empirical Results, Discussion*).

2. **Theoretical & Mathematical Deepening**:
   - Include formal problem definitions with equations and constraint spaces.
   - Provide complete proofs (Lyapunov energy stability, termination bounds, complexity theorems).
   - Detail algorithmic pseudocode protocols with line-by-line invariants.

3. **Empirical Benchmarking & Statistical Rigor**:
   - Tabulate empirical metrics across multiple baselines.
   - Report sample sizes ($N$), $p$-values, confidence intervals ($\Delta \pm \epsilon$), Cohen's $d$, and hardware profiling.

4. **Multi-Venue Formatting & Verification**:
   - Apply venue-specific templates (`IEEEtran`, `acmart`, `neurips_2024`, `icml2024`, `cvpr_paper`, `acl_latex`, `mdpi`, etc.).
   - Execute `CheckmateVerifierService.audit_pdf` with text-layer extraction, math balance, and zero-raw-leak assertion.
