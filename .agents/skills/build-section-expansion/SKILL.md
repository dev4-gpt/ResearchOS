---
name: build-section-expansion
description: Map-Reduce Section Expansion skill for ResearchingOS. Converts a 10-section outline into a 15-25 page (8,000-18,000+ words) academic paper with formal LaTeX equations, pseudocode algorithms, and comparison tables.
---

# Build Section Expansion Skill (`/build`)

Use this skill during Phase 3 of the Research Lifecycle to expand each outline section into exhaustive academic prose.

## Core Rules & Execution

1. **Map-Reduce Architecture**:
   - Spawns parallel or sequential section writer nodes for all 10 planned sections.
   - Each section targets 1,000–2,000 words of dense, authoritative academic prose.

2. **Required Technical Elements per Section**:
   - **Math & Equations**: Use `\begin{equation} ... \end{equation}` for formal loss functions, vector spaces, and scaling laws.
   - **Taxonomy Tables**: Use Markdown/LaTeX tables for multi-paper parameter comparisons.
   - **Algorithm Blocks**: Provide Python/Pseudocode blocks for original frameworks (e.g. MAHI).
   - **Citations**: Include native `\cite{citation_key}` tags matching `references.bib`.

3. **Anti-Filler Directive**:
   - Write in direct, principal-level prose.
   - Never use AI fluff words ("In conclusion", "delve into", "tapestry of", "beacon of", "crucial role").
