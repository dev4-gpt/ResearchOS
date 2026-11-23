# AlphaEvolve and Harness²

ResearchingOS integrates two pinned upstream methods through independent adapters. It uses AlphaEvolve's actual greedy population database, prompt sampler and SEARCH/REPLACE parser in a bounded loop. It uses Harness²'s actual `run_domain` recursion, composition and experience library through a custom research-task adapter. Neither is a rebranding of the manuscript hill-climber.

## Setup and demos

From the repository root:

```bash
backend/.venv/bin/python scripts/setup_research_engines.py
backend/.venv/bin/python scripts/setup_research_engines.py --check
backend/.venv/bin/python scripts/run_research_engine.py alphaevolve --seed 0
backend/.venv/bin/python scripts/run_research_engine.py harness2 --seed 0
```

Setup downloads only the files in `integrations/research_engines.lock.json`, checking their Git blob hashes. Source copies live under ignored `.tools/research-engines/`; their licenses are included. It does not install dependencies or run upstream setup scripts. The adapters require Python 3.12/3.13, NumPy, typing_extensions and google-genai (only for live calls); the existing backend environment was used for validation. AlphaEvolve's original full requirements include older scientific packages; do not install them over the backend environment. This adapter does not import its Docker SDK evaluator or full `async_run` entrypoint.

For the unmodified Harness² demo, independently of our adapter:

```bash
PYTHONPATH=.tools/research-engines/harness2 backend/.venv/bin/python -m harness2.cli.demo --output /tmp/researchingos-harness2-demo --k 2
```

Our demo uses fixed, reviewed candidate edits and deterministic execution with the real upstream method components. It makes zero model calls and never executes arbitrary candidate Python on the host. Its synthetic labels intentionally favor query/title overlap. Better fixture scores demonstrate wiring, NOT model quality or research progress.

## Live runs

Live runs are disabled by default. Configure environment variables explicitly; the CLI does not read `.env`:

- `RESEARCH_ENGINES_ENABLED=true`
- `GEMINI_API_KEY`: Gemini API credential, not a ChatGPT subscription.
- `RESEARCH_ENGINE_IMAGE`: a locally available Python container image with GNU `timeout`, referenced as `name@sha256:<digest>` (AlphaEvolve only).

Supply a real model ID that supports the Gemini API generation settings, a reviewed dataset, and explicit budgets. Provider compatibility is not yet live-validated. Example (replace `MODEL_ID`, not a claimed model name):

```bash
backend/.venv/bin/python scripts/run_research_engine.py alphaevolve --mode live --model MODEL_ID --dataset /absolute/path/ranking.json --steps 2 --seconds 180 --calls 16 --tokens 200000 --max-usd 1 --token-price-ceiling 100
backend/.venv/bin/python scripts/run_research_engine.py harness2 --mode live --model MODEL_ID --dataset /absolute/path/ranking.json --seconds 180 --calls 16 --tokens 200000 --max-usd 1 --token-price-ceiling 100
```

The price ceiling is an operator-provided maximum USD per million tokens, not a provider price or billing guarantee. Reservations use input bytes plus bounded output; they remain charged to the run budget on request failures. Provider-reported tokens are tracked separately. Calls, reserved tokens, reserved cost and wall time all stop work. A parent process enforces the wall-clock limit even if an upstream method catches an exception. Interrupting the CLI terminates its worker process group; run failures remain visible.

Dataset schema is demonstrated in `backend/tests/fixtures/research_engines/ranking.json`: `synthetic`, `tasks`, safe task `id`, `split` (`development` or `heldout`), `query`, `documents` with IDs/titles, `source_rankings` and graded `labels` (0–3). Use trustworthy independent labels and enough held-out queries for your research question. All rankings must be complete permutations. Both engines see development inputs; only AlphaEvolve gets development scores. Neither receives held-out labels. Harness² retains development experience only; its final harness is frozen before held-out execution. Default data always remains synthetic, even with a live model.

AlphaEvolve candidate functions run in networkless, unprivileged, read-only, resource-limited Docker containers with no mounted host files or credentials. They return ID rankings; the host computes metrics from private labels. Docker/image failure blocks execution; there is no host-execution fallback. Harness² uses a text-only model channel: edits are restricted to system prompt and tool guidance. The upstream unrestricted Codex/OpenCode executor is never launched. This restriction deliberately excludes scripts, plugins, permission edits and subagents. The research adapter currently supports sequential `k=1`; the official demo exercises both modes separately.

## Evidence and UI

Feynman Workbench → **Research engines** displays source status, runs, failures, model usage, seed, metrics, provenance and artifacts. HTTP routes are read-only:

- `GET /api/research-engines/status`
- `GET /api/research-engines/runs`
- `GET /api/research-engines/runs/{id}`
- `GET /api/research-engines/runs/{id}/artifact?name=measurements.json`

`runs/research_engines/<id>/` stores spec, frozen dataset/evaluator, upstream pin, candidate, evolution or Harness² history, measurements, summary and SHA-256 manifest. Successful measurements also enter the existing EvidenceLedger. The API checks hashes and recomputes metrics rather than trusting score text. `FactCheckerService.verify_research_engine_run` fails closed: this MVP does not automatically admit any engine run to manuscript evidence. Hashes detect accidental tampering, not a malicious operator rewriting the entire evidence bundle. Live executable replay, independent evaluation and research review remain necessary before publication admission.

## Validation and remaining limits

Run `backend/.venv/bin/python -m pytest backend/tests/test_research_engines.py` and `npm run build --prefix frontend`. Upstream integration tests explicitly skip if pinned sources have not been downloaded; other tests still run.

Three deterministic seeds are plumbing checks, not a significance study. Full budget-matched live comparisons, independent re-execution of generated programs, real dataset efficacy, and Docker isolation probes require a network/Docker-capable environment. No GPU or paid benchmark installation is required for the demos. Existing manuscript fitness proxies remain unchanged and are not used as experimental objectives.

### Recorded validation (2026-11-17)

- 12 research-engine tests passed; 26 API tests and 24 existing reproducibility/fact-checker/autoresearch tests passed (62 distinct tests).
- Frontend TypeScript/Vite production build passed.
- Both pinned upstream source inventories passed hash verification.
- Official Harness² deterministic demo passed 2 tasks in both modes; our adapters passed three seeds each. Raw comparison: `runs/research_engines/demo-comparison.json`.
- All four live localhost probes returned environment-level `Operation not permitted`; service health remains unverified. In-process registered API health/vault/drafts/engine routes returned HTTP 200. Docker daemon access was also denied, and direct GitHub network access from the executor failed. No live model calls or paid compute runs were performed.
