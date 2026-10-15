# OpenResearch integration

ResearchingOS connects to [alphaXiv/OpenResearch](https://github.com/alphaXiv/OpenResearch)
through its official `orx` CLI. Verified with CLI 0.2.18 and upstream source
`58eaa168380b95f2cca36907d8f627ae27280dd5`.

## Pipeline behavior

When the executable is available, Scout adds alphaXiv keyword and semantic
retrieval to `AcademicSearchService.run_combined_search`. Both result lists enter
the existing title deduplication and reciprocal rank fusion. Each strategy fails
independently; the other scholarly sources continue when OpenResearch is missing,
disabled, times out, or returns an error. A search can add up to 20 seconds to a
Scout batch when the dependency is unresponsive.

The adapter preserves arXiv identifiers so the existing PDF ingestion stage can
download the original paper. Discovery abstracts are not full PDFs. alphaXiv
votes are not citation counts; absent authors and citations are left empty/zero.
The manuscript fact checker and publication gates still apply.

The Feynman Workbench has an **OpenResearch** tab with connection status, manual
keyword/semantic discovery, local projects, experiment trees, and run history.
Project/run text is displayed as supplied by the CLI. It is not converted into
verified measurements or automatically admitted as manuscript evidence.
Launch and manage experiments in the OpenResearch workspace; this integration
does not start compute jobs or change experiment branches.

## Setup

Install `orx` using the upstream setup guide. For an isolated project installation,
download and inspect the official installer, then set
`OPENRESEARCH_CLI_UNMANAGED_INSTALL="$PWD/.tools/openresearch"` when running it.
The `.tools/` directory is ignored by Git and is not distributed with the repository.

The backend searches `.tools/openresearch/orx`, then `PATH`. Override with
`OPENRESEARCH_BIN_PATH=/absolute/path/to/orx`. Set `OPENRESEARCH_ENABLED=false`
to disable the adapter, including automatic Scout searches. Restart the backend
after changing its environment. All adapter commands pass `--no-telemetry`.

Run `orx up` from your experiment repository to start OpenResearch's local
workspace at `http://127.0.0.1:4791`, then import/create a project there. Project
inspection uses the current user's OpenResearch store. Literature discovery does
not require a project or login. OpenResearch account/compute setup stays in its UI.

## API

| Endpoint | Behavior |
| --- | --- |
| `GET /api/openresearch/status` | Installation, version, enabled/available state |
| `POST /api/openresearch/discover` | `{ "query": "topic", "strategy": "keyword", "limit": 10 }`; strategy also supports `embedding` |
| `GET /api/openresearch/projects` | Local project records from `orx projects --json` |
| `GET /api/openresearch/projects/{id}` | Project tree and run history as CLI text |

Dependency failures return HTTP 503 with an explanation; invalid input returns
400/422. There is no arbitrary shell-command endpoint or simulated success mode.

## Verification

Run `backend/.venv/bin/python -m pytest backend/tests/test_openresearch.py` and
`npm run build --prefix frontend`. Unit tests isolate the external CLI and verify
argument handling, unavailable dependencies, upstream errors, JSON validation,
independent retrieval failure, Scout ranking, and the original PDF ingestion path.
