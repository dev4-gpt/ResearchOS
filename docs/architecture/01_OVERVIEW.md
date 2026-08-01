# System Architecture Overview — ResearchingOS

## 1. Executive Summary

**ResearchingOS** is an autonomous multi-agent academic research platform designed to automate literature discovery, full-text PDF parsing, quantitative statistical auditing, adversarial peer review, Obsidian knowledge graph construction, and IEEE/ACM paper compilation.

Unlike generic chatbot assistants that produce hallucinated overviews, ResearchingOS uses a **deliberate multi-agent council architecture** paired with an automated **zero-hallucination fact-checking linter engine** to guarantee empirical grounding across every claim, metric, and citation.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        RESEARCHINGOS SYSTEM ARCHITECTURE                               │
├───────────────────┬───────────────────┬───────────────────┬────────────────────────────┤
│ Layer 1: Search   │ Layer 2: PDF      │ Layer 3: Multi-   │ Layer 4: Fact-Checker &    │
│    & Discovery    │    Extraction     │    Agent Council  │    IEEEtran Export Engine  │
│   (12 Scientific  │   (pypdf, section │   (7 Senior       │   (Obsidian Vault Graph,   │
│    Repositories)  │    parsing)       │    Personas)      │    LaTeX/BibTeX Exporter)  │
└───────────────────┴───────────────────┴───────────────────┴────────────────────────────┘
```

---

## 2. Core Subsystems & Data Flow

### 2.1 Backend Core (Python / FastAPI)
- **FastAPI Application (`backend/main.py`)**: Asynchronous API server handling research start requests (`/api/research/start`), SSE log streaming (`/api/research/stream/{id}`), vault CRUD operations (`/api/vault/*`), and LaTeX exporting (`/api/vault/export-latex`).
- **Council Orchestrator (`backend/agents/council.py`)**: Manages the execution lifecycle across the 7 agent personas, including exponential rate-limit retries, model cascade rotation (`gemini-2.5-flash`, `gemini-2.0-flash-exp`, `gemini-1.5-flash`), and dry-run fallbacks.
- **Search Service (`backend/services/search.py`)**: Asynchronous HTTP discovery client aggregating paper metadata across arXiv, OpenAlex, Europe PMC, PubMed, Crossref, DBLP, PLOS, DOAJ, ACM Digital Library, IEEE Xplore, GitHub, and Hugging Face.
- **PDF Extraction Service (`backend/services/pdf_extractor.py`)**: Downloads full-text paper PDFs and parses section boundaries into structured markdown notes.
- **Fact-Checker Service (`backend/services/fact_checker.py`)**: Audits manuscript drafts for broken wikilinks and verifies numeric claim grounding ($N=...$, $\%$, $p$-values).
- **LaTeX Exporter Service (`backend/services/latex_exporter.py`)**: Converts markdown manuscripts into compilable two-column IEEEtran LaTeX (`.tex`) and BibTeX (`.bib`).

### 2.2 Storage Layer (Obsidian Vault Knowledge Graph)
- **Vault Directory (`vault/`)**:
  - `01_Papers/`: Ingested paper markdown notes with YAML frontmatter (`full_pdf_ingested: true`).
  - `02_Concepts/`: Cross-paper concept taxonomy.
  - `03_Debates/`: Transcripts of boardroom council debates and Chairman syntheses.
  - `04_Drafts/`: 15+ page journal-ready manuscript drafts ($8,000+$ words).

### 2.3 Frontend Application (React 19 / Vite / 3D CSS)
- **Control Deck (`Dashboard.tsx`)**: Hero section featuring the 3D scroll-driven metallic laptop workspace (`Laptop3DWorkspace.tsx`).
- **Agent Boardroom (`Boardroom.tsx`)**: Live SSE streaming interface displaying real-time agent debate logs and consensus meters.
- **Knowledge Graph (`GraphView.tsx`)**: Interactive 2D/3D visual network mapping paper relationships and `[[WikiLinks]]`.
- **HITL Publisher (`DocEditor.tsx`)**: Document editor with live preview, Fact-Check score badges, and one-click "Export IEEEtran LaTeX & BibTeX" controls.

---

## 3. Technology Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, Google Gemini API (`google-generativeai`), PyPDF, HTTPX, Pytest.
- **Frontend**: React 19, TypeScript 6.0, Vite 8.0, Framer Motion, Lucide React Icons, 3D CSS Transforms.
- **Storage**: Obsidian Flavored Markdown (YAML Frontmatter + `[[WikiLinks]]`), BibTeX (`.bib`), IEEEtran LaTeX (`.tex`).
