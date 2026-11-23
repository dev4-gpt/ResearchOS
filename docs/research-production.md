# Research workflow: operations and release status

The integrations now have a local orchestration entrypoint: OpenResearch discovery → optional AlphaEvolve/Harness² experiments → isolated PaperOrchestra generation → evidence review. This is not yet a production-qualified deployment. Live provider/Docker execution, independent scientific replay and deployment operations remain unvalidated.

## Execute

Use the backend virtualenv and explicitly exported environment variables; these CLIs do not load `.env`. The HTTP app now requires operator authentication by default; follow `production-deployment.md` for HTTPS, private persistence and worker configuration. Engine/writer execution remains operator-only CLI; the UI/API inspect results. Deployment certification remains gated on the evidence below.

Create a JSON spec using absolute paths:

```json
{
  "query": "your research question",
  "materials": "/absolute/materials",
  "template": "/absolute/template",
  "writer_model": "YOUR_MODEL_ID",
  "reflection_model": "YOUR_MODEL_ID",
  "cutoff": "2026-11",
  "generate": false,
  "writer_seconds": 1800,
  "experiments": [
    {"engine": "alphaevolve", "mode": "demo", "seed": 0},
    {"engine": "harness2", "mode": "demo", "seed": 0}
  ]
}
```

Materials require `idea_sparse.md` and `experimental_log.md`; template requires `template.tex` and `guidelines.md`. `generate: false` runs discovery/experiments and prepares writer materials without generating a manuscript. Discovery still needs network access. Demo experiments are synthetic and never become scientific findings.

```bash
backend/.venv/bin/python scripts/check_research_readiness.py
backend/.venv/bin/python scripts/research_workflow.py --spec /absolute/workflow.json
backend/.venv/bin/python scripts/research_workflow.py --resume WORKFLOW_ID
```

For live experiments, use `mode: live`, an explicit provider model, a reviewed non-synthetic `dataset_path` and budgets described in `research_engines.md`. Export `RESEARCH_ENGINES_ENABLED=true`, `GEMINI_API_KEY` and a digest-pinned `RESEARCH_ENGINE_IMAGE`. Real labels and scientific validation cannot be substituted by fixture tests.

For writing, set `generate: true` and use the hash-locked, credential-free container and host broker described in [PaperOrchestra](paperorchestra.md). Supply the approved Gemini configuration, the same existing spending ledger, and the reviewed bibliography and citation map as frozen template inputs.

## Isolation and recovery

Writer execution uses a non-root container with a read-only root, no capabilities, restricted memory/CPU/PIDs, read-only source/material/template mounts and one writable output directory. Plotting is disabled. It needs outbound network for model/literature APIs; production egress controls remain a deployment requirement. Timeout and sampled output-size limits stop the container. The sampled disk limit may overshoot; deploy on a quota-controlled volume. Model credentials are passed by environment name, not embedded in commands. Upstream prints a credential, so its stdout/stderr and Docker logging are disabled.

The worker requires both TeX and a nonempty PDF before intake; this checks output presence, not PDF validity or venue compliance. It records failed cleanup as blocked. A crash/restart never automatically reissues paid stages. Completed stages are reused, frozen specs/datasets are checked, and engine metrics are recomputed. For interrupted stages, inspect the manifest and referenced container, stop any remaining container, then create a new workflow after reviewing prior provider usage. Back up the ignored `runs/research_workflows` and `runs/paperorchestra` directories to private durable storage; test restoration before deployment. Manifest hashes detect accidental edits, not malicious rewriting by the local operator.

## Review

Discovery and engine provenance are appended to the writer's experimental log with explicit unverified/synthetic labels. They are not automatically admitted as manuscript evidence. Importing externally generated output remains supported.

```bash
backend/.venv/bin/python scripts/paperorchestra.py run --job JOB_ID --seconds 1800
backend/.venv/bin/python scripts/paperorchestra.py review --job JOB_ID \
  --manuscript intake-ID/path/paper.tex --citation-map /absolute/citation-map.json
```

The citation map is a reviewed JSON object mapping actual BibTeX keys to exact `vault/01_Papers/*.md` filenames, for example `{"smith2020": "arxiv_12345.md"}`. The reviewer requires full-text ingestion metadata, records source hashes and uses the strict FactChecker. TeX includes/dynamic commands are blocked pending review of a flattened manuscript. It never compiles untrusted TeX on the host. A clean automated report still requires citation identity/entailment, executable experiment replay, compiled PDF/venue review and human publication approval. There is no automatic journal submission.

Inspect `/api/research-engines/workflows`, existing engine routes and `/api/paperorchestra/jobs`. The Workbench shows writer states. A production readiness report never equates source pins, mock tests or a frontend build with a live release.

## Release gates still open

- Live tests of all providers and container isolation, including timeout, cancellation and recovery.
- Reproducible locked writer image, enforced provider spending controls and egress/storage limits.
- Independent benchmark dataset, executable candidate replay and reviewed claim bindings.
- End-to-end real manuscript, exact citation identity, target venue/PDF validation and human approval.
- Authenticated deployment, private persistence, backup/restore and monitoring.
- All four HTTP connectivity checks passing from the deployment environment.

## Validation recorded 2026-11-20

- 56 related backend tests passed, covering workflow recovery, writer failures/timeouts, output intake, review, actual pinned engine components and existing fact-checker/reproducibility integrations.
- Frontend TypeScript/Vite build passed. Source hash verification and whitespace checks passed.
- OpenResearch reports `orx 0.2.18`; all three upstream source sets verify.
- Writer execution tests use a simulated container process; no live writer/provider run was performed.
- All four real localhost checks were denied with `Operation not permitted`; in-process API tests are not a substitute.
- Current machine-readable prerequisites: `runs/research_engines/production-readiness.json`.
