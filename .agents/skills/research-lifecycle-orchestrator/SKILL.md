---
name: research-lifecycle-orchestrator
description: Addy Osmani Agent Skills architecture adaptation for ResearchingOS. Defines the 6-phase development lifecycle (/spec, /plan, /build, /test, /review, /ship) and autonomous pass (/build auto) for 15-25 page camera-ready academic manuscripts.
---

# Agent Skills Architecture for ResearchingOS

This skill establishes the production-grade engineering workflow based on the Addy Osmani Agent Skills architecture (`https://github.com/addyosmani/agent-skills`).

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
 │ Topic│ ───▶ │Council│ ───▶ │ Map- │ ───▶ │ Fact │ ───▶ │ Peer │ ───▶ │Camera│
 │ Dossier│    │Debate│      │Reduce│      │Check │      │Review│      │Ready │
 └──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /test         /review       /ship
```

---

## Commands & Lifecycle Phases

| Phase | Command | Key Principle | Exit Gate |
|-------|---------|---------------|-----------|
| **1. DEFINE** | `/spec` | Ingestion before drafting | 20-30 papers ingested with extracted abstracts & citation keys |
| **2. PLAN** | `/plan` | 10-section atomic structure | Chairman 10-section outline with equations & table schemas |
| **3. BUILD** | `/build` | Map-Reduce section expansion | 1,000–2,000 words per section (15–25 pages total) |
| **4. VERIFY** | `/test` | Proof groundings | Fact-check score = 100.0%, 0 invented citation keys |
| **5. REVIEW** | `/review` | Adversarial audit | Peer Review Decision = STRONG ACCEPT |
| **6. SHIP** | `/ship` | Camera-ready PDF | Clean pdflatex build, PDF QA passed, O-1A evidence logged |

---

## Slash Commands Usage

- **`/spec`**: Triggers paper discovery across arXiv/OpenAlex and saves structured paper notes to `vault/01_Papers/`.
- **`/plan`**: Convenes the 6-agent boardroom debate (Scout, Analyst, Engineer, Statistician, Reviewer2, Chairman) and saves output to `vault/03_Debates/`.
- **`/build`**: Invokes the LangGraph Map-Reduce Section Generator to expand each section with LaTeX math (`\begin{equation}`), Markdown tables, and pseudocode algorithms.
- **`/build auto`**: Runs the complete end-to-end pipeline autonomously from paper ingestion through to compiled 15–25 page camera-ready PDF export.
- **`/test`**: Runs `FactCheckerService` linter against source paper text.
- **`/review`**: Runs `RedTeamAudit` and `PeerReviewAudit` area chair review against conference rubrics.
- **`/ship`**: Compiles venue LaTeX (`NeurIPS`, `CVPR`, `IEEEtran`, `ACM`), verifies PDF layout, and exports to `vault/04_Drafts/`.

---

## Quality Gates & Anti-Rationalization Rules

1. **No Short-Path Drafting**: Never generate a single-pass ~2-page draft. Always map-reduce expand all 10 planned sections.
2. **Zero Invented Citations**: All inline citations must map to `references.bib` and Obsidian wikilinks `[[paper_id]]`.
3. **Fact-Checked Proof**: Numerical claims ($N$, $\%$, $p$-values) must match source text.
4. **Clean Abstract Block**: Strip duplicate `# Abstract` / `## Abstract` from body markdown to prevent duplicate `1 Abstract` section titles in LaTeX.
