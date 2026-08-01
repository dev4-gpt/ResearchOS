---
description: Workflow for converting vault markdown manuscripts into compilable two-column IEEEtran LaTeX (.tex) and BibTeX (.bib) files.
---

# Workflow: IEEEtran LaTeX & BibTeX Export

Follow this workflow to export markdown manuscripts for formal journal submission to IEEE, ACM, or Nature.

## Step 1: Markdown to IEEEtran Conversion
1. Invoke `LaTeXExporterService`:
   - Parse YAML frontmatter to extract Title, Authors, and Abstract.
   - Sanitize special LaTeX characters (`&` -> `\&`, `%` -> `\%`, `#` -> `\#`, `_` -> `\_`).
   - Convert Markdown headers (`#`, `##`, `###`) to `\section{...}`, `\subsection{...}`, `\subsubsection{...}`.
   - Convert Obsidian wikilinks `[[paper_id]]` to LaTeX citations `\cite{paper_id}`.
   - Convert Markdown bold/italics (`**text**` -> `\textbf{text}`, `*text*` -> `\textit{text}`).
2. Wrap body inside formal IEEEtran template:
   `\documentclass[10pt,journal,compsoc,twocolumn]{IEEEtran}`

## Step 2: BibTeX Reference Generation
1. Read all ingested paper metadata from `vault/01_Papers/`.
2. Generate structured `@article{...}` BibTeX entries with paper ID, title, author list, publication year, journal/conference source, and DOI URL.
3. Save generated references file to `vault/04_Drafts/references.bib`.

## Step 3: Local or Overleaf Compilation
1. Save LaTeX code to `vault/04_Drafts/{manuscript_name}_IEEEtran.tex`.
2. Compile locally using:
   `pdflatex {manuscript_name}_IEEEtran.tex && bibtex {manuscript_name}_IEEEtran && pdflatex {manuscript_name}_IEEEtran.tex`
3. Or upload `.tex` and `.bib` files directly to Overleaf for camera-ready PDF compilation.
