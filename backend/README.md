# ResearchingOS — Backend

FastAPI server hosting the multi-agent research pipeline. All agent logic, academic search, and vault I/O lives here.

## Structure

```
backend/
├── main.py               # FastAPI app, routes, SSE streaming
├── agents/
│   └── council.py        # CouncilOrchestrator — 7-agent pipeline
├── services/
│   ├── search.py         # AcademicSearchService — 12 data sources, parallel RRF
│   └── vault.py          # VaultManager — read/write/graph Obsidian Markdown
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_council.py
│   └── test_vault.py
└── pyproject.toml        # uv project manifest
```

## Setup

```bash
uv sync                            # install dependencies
cp ../.env.example ../.env         # configure (GEMINI_API_KEY optional)
uv run uvicorn main:app --reload   # starts on http://127.0.0.1:8000
```

## Running tests

```bash
uv run pytest
```

## Agent pipeline stages

| Stage | Agent(s) | Output |
| --- | --- | --- |
| 1. Ingestion | Scout + Analyst | `vault/01_Papers/*.md` |
| 2. Critique | Engineer, Statistician, Reviewer #2 | In-memory critique dicts |
| 3. Debate | All three + multi-turn replies | Debate transcript |
| 4. Synthesis | Chairman | `vault/03_Debates/debate_*.md` |
| 5. Drafting | Writer | `vault/04_Drafts/review_*.md` |

## Model configuration

All agents default to `gemini-2.0-flash`. Override via env:

```
GEMINI_FLASH_MODEL=gemini-2.5-flash-preview-05-20
GEMINI_PRO_MODEL=gemini-2.5-pro-preview-05-06
```

## Dry-run mode

If `GEMINI_API_KEY` is unset, the orchestrator returns mock responses and skips all API calls. Search, vault I/O, and SSE streaming still execute normally — useful for frontend development.

## Key dependencies

| Package | Purpose |
| --- | --- |
| `fastapi` | HTTP framework + auto-docs |
| `uvicorn[standard]` | ASGI server |
| `google-generativeai` | Gemini SDK |
| `httpx` | Async-compatible HTTP for multi-source search |
| `python-dotenv` | `.env` loading |
