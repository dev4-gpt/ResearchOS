# ResearchingOS

An open-source, AI-native research operating system. You give it a topic; a council of seven specialized LLM agents searches a dozen academic databases, debates the findings in a multi-turn boardroom session, and produces a peer-review-grade literature review saved as structured Obsidian Markdown in a local vault.

```
Topic → Scout → Analyst → [ Engineer | Statistician | Reviewer #2 ] → Boardroom Debate → Chairman → Writer → Vault
```

## Features

- **Multi-source search** — arXiv, OpenAlex, Semantic Scholar, EuropePMC, Crossref, DOAJ, PLOS, HAL, PubMed, DBLP, GitHub, Hugging Face (all queried in parallel)
- **Seven-agent council** — Scout, Analyst, Engineer, Statistician, Reviewer #2, Chairman, Writer
- **Live streaming** — Server-Sent Events push every log line to the frontend in real time
- **Obsidian vault** — all paper notes, debate transcripts, and draft reviews written as wiki-linked Markdown
- **Knowledge graph** — auto-built from `[[WikiLink]]` references across the vault
- **Evidence-first release gates** — claims, citations, provenance, venue constraints, peer review, and PDF QA are verified before a camera-ready PDF can be downloaded
- **Dry-run mode** — works without a Gemini API key (mock responses, real search structure); synthetic output is never releaseable

## Project structure

```
ResearchingOS/
├── backend/          # FastAPI + multi-agent pipeline (Python / uv)
├── frontend/         # React 19 + TypeScript + Vite UI
├── vault/            # Obsidian knowledge base (auto-populated by agents)
│   ├── 01_Papers/
│   ├── 02_Concepts/
│   ├── 03_Debates/
│   └── 04_Drafts/
└── .env.example      # Environment variable template
```

## Quick start

### Prerequisites

- Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/)
- Node.js ≥ 18
- A [Gemini API key](https://aistudio.google.com/app/apikey) (optional — dry-run works without one)

### 1. Clone and configure

```bash
git clone https://github.com/your-org/ResearchingOS.git
cd ResearchingOS
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Start the backend

```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `GEMINI_API_KEY` | No | — | Enables live LLM calls; omit for dry-run |
| `RESEARCHINGOS_RUN_MODE` | No | `auto` | `auto`, `dry_run`, or `live`; synthetic runs can never be released |
| `GEMINI_FLASH_MODEL` | No | `gemini-2.0-flash` | Override flash model for all agents |
| `GEMINI_PRO_MODEL` | No | `gemini-2.0-pro-exp` | Override pro model for chairman/writer |
| `VAULT_PATH` | No | `../vault` | Absolute or backend-relative path to vault |
| `PORT` | No | `8000` | Backend server port |
| `HOST` | No | `127.0.0.1` | Backend server host |
| `CONTACT_EMAIL` | No | — | Added to API User-Agent for polite-pool routing |

See `.env.example` for a full template.

## Evidence-first publication compiler

Each research run writes a durable ledger under `runs/{run_id}/` containing the manifest, source provenance, claims, synthesis, manuscript, and venue build artifacts. The release controller blocks camera-ready output for unsupported claims, missing or duplicate citation keys, invalid peer-review JSON, synthetic content, failed compilation, venue violations, PDF artifacts, or missing reproducibility metadata.

The human sign-off screen is intended for authorship, ethics, originality, interpretation, conflicts of interest, and final submission metadata. It is not a substitute for those decisions, and ResearchingOS does not determine immigration eligibility. O-1A and EB-1A evidence are tracked as separate profiles for attorney review.

Useful verification commands:

```bash
cd backend
.venv/bin/pytest tests -q
.venv/bin/python ../scripts/security_scan.py
```

Rotate any credentials reported by the security scan before using live providers. Keep `.env` local and out of version control.

## API overview

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Service health + dry-run status |
| `POST` | `/api/research/start` | Launch pipeline (`{"topic": "..."}`) → returns `project_id` |
| `GET` | `/api/research/stream/{project_id}` | SSE stream of agent logs |
| `GET` | `/api/vault/files` | List all vault files (optionally `?category=papers`) |
| `GET` | `/api/vault/read` | Read a single file (`?category=papers&filename=…`) |
| `POST` | `/api/vault/write` | Save / edit a vault file |
| `GET` | `/api/vault/graph` | Knowledge graph (nodes + edges) |

Full backend docs at `http://localhost:8000/docs` (FastAPI auto-docs).

## Vault conventions

See [README.md](./vault/README.md) for folder structure, filename patterns, required frontmatter fields, and the deduplication policy.

## Contributing

1. Fork the repo and create a branch.
2. `cd backend && uv run pytest` — all tests must pass.
3. Open a pull request with a clear description of the change.

## License

MIT
