# Layer Specification: Ingestion & PDF Extraction Service

## 1. Overview

The **PDF Extraction Service** (`backend/services/pdf_extractor.py`) handles downloading full paper PDFs from open-access academic repositories and converting raw PDF text into structured markdown section notes.

---

## 2. Ingestion Pipeline & PDF Retrieval

```
  [Paper Query / ID]
          │
          ▼
  [Fetch PDF Binary from arXiv / OpenAlex / Europe PMC]
          │
          ▼
  [PyPDF Extraction & Section Header Regex Parsing]
          │
          ▼
  [Construct Structured Markdown Note with YAML Frontmatter]
          │
          ▼
  [Save to vault/01_Papers/{paper_id}.md]
```

### 2.1 Supported Repositories & PDF URLs
- **arXiv**: Downloads direct PDFs from `https://arxiv.org/pdf/{arxiv_id}.pdf`.
- **OpenAlex**: Resolves `open_access.pdf_url` fields.
- **Europe PMC**: Downloads full-text XML/PDFs via PMC BioC API.

### 2.2 Section Structure Parsing
The service uses regex boundary matching to categorize extracted text into standard academic paper sections:
1. `Abstract`
2. `Introduction & Related Work`
3. `Methodology & Systems Architecture`
4. `Experiments & Empirical Benchmarks`
5. `Results & Quantitative Findings`
6. `Discussion & Limitations`
7. `Conclusion & Future Directions`

---

## 3. Metadata Frontmatter Specification

Ingested paper notes saved in `vault/01_Papers/` contain formal YAML frontmatter:

```yaml
---
title: "Thinking Like A Lawyer In The Age Of Generative AI: Cognitive Limits On AI Adoption Among Lawyers"
authors:
  - "Daniel Schwarcz"
  - "Debarati Das"
  - "Dongyeop Kang"
  - "Brett H. McDonnell"
url: "https://doi.org/10.2139/ssrn.5260645"
published: "2025-05-20"
citations: "14"
source: "Crossref"
id: "crossref:10.2139/ssrn.5260645"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "enterprise-ai"
---
```
