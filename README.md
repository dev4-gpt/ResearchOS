# ResearchingOS

An open-source, autonomous AI-native academic publishing engine and research operating system. You provide a research topic; a two-tier council of specialized LLM agents and meta-reviewers conducts deep multi-repository literature discovery, executes formal boardroom debates, grounds all empirical facts, and compiles 100% publication-ready LaTeX manuscripts across 12 premier academic venues.

```
Topic → Scout → Analyst → [ Engineer | Statistician | Reviewer #2 ] → Boardroom Debate → Chairman → Writer 
      ↳ Tier 2: Meta-Review & Cross-Venue Alignment Council → 12-Venue LaTeX Compilers → Vault / Papers
```

---

## System Architecture

ResearchingOS operates a **Dual-Phase Multi-Agent Orchestration Architecture**:

### Tier 1: Senior Principal Research Author & 7-Agent Council
- **Senior Scout Researcher (`Scout`)**: Queries 12 primary scholarly repositories (arXiv, OpenAlex, Semantic Scholar, Europe PMC, Crossref, DOAJ, PLOS, HAL, PubMed, DBLP, GitHub, Hugging Face) using Reciprocal Rank Fusion (RRF).
- **Lead Analyst (`Analyst`)**: Parses methodology, formal proofs, loss formulations, and architectures, ingesting notes into `vault/01_Papers/`.
- **Senior Systems Engineer (`Engineer`)**: Audits algorithmic design, parameter efficiency, memory ceilings, and compute FLOPs scaling laws.
- **Senior Statistician & Methods Critic (`Statistician`)**: Evaluates sample sizes ($N$), baselines, statistical significance ($p$-values), and empirical effect sizes.
- **Reviewer #2 / Academic Editor (`Reviewer2`)**: Hostile peer reviewer identifying un-ablated claims, overhype, and rejection vulnerabilities.
- **CEO / Institute Chairman (`Chairman`)**: Moderates council debates and synthesizes consensus outlines saved to `vault/03_Debates/`.
- **Senior Research Writer & Publisher (`Writer`)**: Drafts formal literature review manuscripts ($8,000+$ words) in `vault/04_Drafts/` with inline citations and LaTeX equations.

### Tier 2: Meta-Review & Cross-Venue Alignment Council
- **Exhaustive Citation Expansion**: Expands manuscripts to cite **15–30+ distinct, authentic peer-reviewed references** from the grounded vault index.
- **Formal Technical Rigor**: Enforces rigorous formal proofs, Lyapunov convergence guarantees, multi-baseline empirical tables ($N \ge 300$), and explicit threat-to-validity analyses.
- **Venue-Specific Page Budgeting**: Re-formats and re-balances layouts to adhere strictly to target venue specifications (e.g., exact 4-page IEEE camera-ready density, NeurIPS 9-page limits, ICML 8-page limits).

---

## 12 Supported Academic Venues

ResearchingOS generates custom, compilable LaTeX (`.tex`), BibTeX (`.bib`), and publication PDFs across 12 academic venues:

| Venue | Class / Style | Focus & Standards | Page Budget |
| :--- | :--- | :--- | :--- |
| **`IEEEtran`** | `IEEEtran.cls` | IEEE Transactions & Conferences | 4 pages (Short/Camera-Ready) / 10–14 pages (Journal) |
| **`NeurIPS`** | `neurips_2024.sty` | Neural Information Processing Systems | 9 pages main content + references |
| **`ICML`** | `icml2024.sty` | International Conference on Machine Learning | 8 pages main content + references |
| **`CVPR`** | `cvpr.sty` | Computer Vision and Pattern Recognition | 8 pages main content + references |
| **`ACL`** | `acl_latex.sty` | Association for Computational Linguistics | 8 pages (Long) / 4 pages (Short) + references |
| **`ACM`** | `acmart.cls` | ACM Transactions & Conferences | 10–12 pages (Survey) / 9 pages (Conference) |
| **`IEEE Access`** | `ieeeaccess.cls` | Open Access Interdisciplinary Engineering | Multi-page full journal layout |
| **`SpringerOpen`**| `svjour3.cls` | Springer Open Computer Science & AI | Double-column standard journal layout |
| **`MDPI`** | `mdpi.cls` | MDPI Applied Sciences & Electronics | Full structured academic journal layout |
| **`DOAJ`** | Standard Article | Directory of Open Access Journals | Clean universal preprint layout |
| **`arXiv`** | Standard Article | Pre-print Server Format | Authoritative archival format |
| **`Femington`** | Custom Journal | Institute for Econometric & AI Governance | Policy and enterprise review format |

---

## Published Master Papers Library

The repository includes 60 verified, publication-ready manuscripts organized by topic and master bundles:

* **Master Bundle (`papers/p/`)**: Complete collection of all 60 compilable venue publications, BibTeX libraries, and build manifests (100% SHA256 checksum identity).
* **Topic Packages (`papers/p1` through `papers/p5`)**:
  * **`papers/p1`**: *Empirical Evaluation of Symbol-Graph RAG vs QLoRA on SWE-bench Lite* (27 distinct peer-reviewed citations)
  * **`papers/p2`**: *Architectural Dynamics, Parameter Efficiency & Scaling Laws in LLM Reasoning* (24 distinct peer-reviewed citations)
  * **`papers/p3`**: *Autonomous Code Synthesis and Self-Healing Multi-Agent Systems* (22 distinct peer-reviewed citations)
  * **`papers/p4`**: *Empirical ROI and Systems Governance of Enterprise GenAI Adoption* (18 distinct peer-reviewed citations)
  * **`papers/p5`**: *Enterprise Adoption of Multi-Agent AI Systems: Infrastructure & Economics* (28 distinct peer-reviewed citations)

---

## Project Structure

```
ResearchingOS/
├── .agents/                  # Agent rules, workflows, and meta-review skills
├── backend/                  # FastAPI + multi-agent pipeline + LaTeX exporters
│   ├── agents/               # 7-Agent Council & Harness Controllers
│   ├── services/             # FactChecker, LaTeXExporter, PublisherReadiness
│   └── tests/                # 112+ automated unit and integration tests
├── frontend/                 # React 19 + TypeScript + Vite UI + 3D Canvas
├── papers/                   # Deployed publication packages
│   ├── p/                    # Master 60-paper multi-venue release bundle
│   ├── p1/ ... p5/           # Filtered topic packages
├── scripts/                  # Verification, audit, and deployment scripts
└── vault/                    # Obsidian knowledge base
    ├── 01_Papers/            # 440+ ingested paper notes with frontmatter
    ├── 02_Concepts/          # Concept taxonomies
    ├── 03_Debates/           # Council transcripts
    └── 04_Drafts/            # Manuscript drafts and LaTeX export targets
```

---

## Quick Start

### Prerequisites
- Python $\ge$ 3.10 and [`uv`](https://docs.astral.sh/uv/)
- Node.js $\ge$ 18
- Modern TeX Live distribution (`pdflatex`, `bibtex`)

### 1. Start the Backend
```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## Verification & Quality Assurance

Run the comprehensive audit suite to verify zero-defect readiness:

```bash
# Run all backend unit and integration tests (112 tests)
pytest backend/tests/

# Run the comprehensive 60-paper multi-venue audit
python3 scripts/comprehensive_zero_error_audit.py

# Verify 4-layer live connectivity
curl -I http://127.0.0.1:8000/api/health
curl -I http://127.0.0.1:8000/api/vault/files
```

---

## License

MIT License.
