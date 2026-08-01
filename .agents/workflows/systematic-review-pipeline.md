---
description: Workflow for executing a 20-paper systematic review, paper ingestion, full PDF extraction, council debate, and draft generation.
---

# Workflow: Systematic Review & Meta-Taxonomy Pipeline

Follow this operational workflow to run an end-to-end multi-agent systematic literature review.

## Stage 1: Topic Definition & Literature Discovery
1. Define target research topic and query parameters (e.g. `max_papers=20`).
2. Invoke `AcademicSearchService` to query 12 scientific databases:
   - arXiv, OpenAlex, Europe PMC, PubMed, Crossref, DBLP, PLOS, DOAJ, ACM, IEEE Xplore, GitHub, Hugging Face.
3. Rank retrieved paper records using Reciprocal Rank Fusion (RRF).

## Stage 2: Full PDF Extraction & Vault Ingestion
1. For each paper URL or arXiv ID, call `PDFExtractionService`:
   - Download PDF from `https://arxiv.org/pdf/{arxiv_id}.pdf` or OpenAlex open-access URL.
   - Extract section structures (*Abstract, Introduction, Method, Experiments, Results, Discussion, Conclusion*).
2. Save structured markdown file to `vault/01_Papers/{paper_id}.md` with frontmatter `full_pdf_ingested: true`.

## Stage 3: Multi-Agent Boardroom Council Audit & Debate
1. Spawn parallel critique agents:
   - **Senior Systems Engineer**: Audit FLOPs compute laws, hardware VRAM limits, and architecture viability.
   - **Senior Statistician**: Audit sample sizes ($N$), $p$-values, control groups, and empirical effect sizes.
   - **Reviewer #2**: Audit rejection risks, short-term horizon deficits, un-ablated baselines, and overhype.
2. Execute **CEO / Chairman Synthesis**:
   - Synthesize consensus points, resolve debate tensions, and output debate transcript to `vault/03_Debates/debate_{topic_slug}.md`.

## Stage 4: Journal-Grade Manuscript Drafting
1. Execute **Senior Research Writer**:
   - Draft an 8,000+ word, 15-page IEEE/ACM two-column literature review manuscript in `vault/04_Drafts/review_{topic_slug}.md`.
   - Embed inline Obsidian wikilinks `[[paper_id]]` for all citations.

## Stage 5: Automated Fact-Check Verification
1. Run `FactCheckerService` on the draft manuscript:
   - Audit target wikilink existence in `vault/01_Papers/`.
   - Extract numeric claims ($N=...$, $\%$, $p < 0.001$) and verify grounding against source text.
2. Attach `fact_check_score` and `verification_matrix` to manuscript frontmatter.
