# Layer Specification: IEEEtran LaTeX & BibTeX Exporter Engine

## 1. Overview

The **LaTeX Exporter Service** (`backend/services/latex_exporter.py`) converts markdown manuscripts into compilable two-column IEEEtran LaTeX (`.tex`) and BibTeX (`.bib`) files.

---

## 2. Formatting & Transformation Rules

### 2.1 Character Sanitization
- Escapes special LaTeX characters in text blocks while preserving math equations (`$$...$$` and `$...$`):
  - `&` $\rightarrow$ `\&`
  - `%` $\rightarrow$ `\%`
  - `#` $\rightarrow$ `\#`
  - `_` $\rightarrow$ `\_`

### 2.2 Header & Citation Transformations
- `# Title` / `## Heading` $\rightarrow$ `\section{Heading}`
- `### Subheading` $\rightarrow$ `\subsection{Subheading}`
- `#### Subsubheading` $\rightarrow$ `\subsubsection{Subsubheading}`
- Obsidian Wikilinks `[[paper_id]]` $\rightarrow$ `\cite{paper_id}`
- Bold/Italics `**text**` $\rightarrow$ `\textbf{text}`

### 2.3 BibTeX Generation Rules
Given ingested paper frontmatter metadata, `generate_bibtex` builds formal BibTeX `@article` entries:

```bibtex
@article{crossref_10_2139_ssrn_5260645,
  title={Thinking Like A Lawyer In The Age Of Generative AI: Cognitive Limits On AI Adoption Among Lawyers},
  author={Daniel Schwarcz and Debarati Das and Dongyeop Kang and Brett H. McDonnell},
  journal={Academic Research Repository},
  year={2025},
  url={https://doi.org/10.2139/ssrn.5260645}
}
```

---

## 3. Template Document Structure

Exports utilize the official IEEE journal class template:

```latex
\documentclass[10pt,journal,compsoc,twocolumn]{IEEEtran}
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{hyperref}

\begin{document}

\title{...}
\author{...}

\maketitle

\begin{abstract}
...
\end{abstract}

...

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```
