# PaperOrchestra writing and review

ResearchingOS now has an optional handoff/intake adapter for the official [google-research/paper-orchestra](https://github.com/google-research/paper-orchestra) project, pinned to `d9bae997e793a015ed38bb1605be9eb58c00284f`.

Its role is manuscript writing from pre-writing materials. AlphaEvolve and Harness² remain experiment/workflow engines; PaperOrchestra operates downstream of research. The adapter prepares inputs, optionally runs the upstream writer in a resource-limited Docker container, imports outputs and performs citation/claim audits. See [workflow operations and release gates](research-production.md). Live generation remains unvalidated; publication is never automatic.

## Prepare inputs

The existing setup script downloads and checks the locked upstream text files, including their license:

```bash
backend/.venv/bin/python scripts/setup_research_engines.py
backend/.venv/bin/python scripts/setup_research_engines.py --check
```

Create a materials directory containing `idea_sparse.md` and `experimental_log.md`. Optional figures go under `figures/`; include `figures/info.json` for their descriptions. If omitted, the adapter writes an empty figure list. Describe absent experiments honestly; synthetic engine demonstrations must not be presented as empirical findings. Input labels are not proof of evidence quality.

Choose a venue-appropriate template directory with `template.tex` and `guidelines.md`, plus its style files. Upstream includes 2025 templates; selecting one does not establish compliance with a current venue.

```bash
backend/.venv/bin/python scripts/paperorchestra.py prepare \
  --materials /absolute/path/materials \
  --template /absolute/path/template \
  --writer-model YOUR_MODEL_ID \
  --reflection-model YOUR_MODEL_ID \
  --cutoff 2026-11
```

This copies the expected inputs into a new `runs/paperorchestra/<job-id>/` directory, records SHA-256 hashes and returns the exact upstream command as an argument array. No shell command is executed and no model call is made. Each job has a unique output directory; preparing it cannot overwrite an existing upstream output.

## Generate with the bounded writer

Use `deploy/runtime/writer.Dockerfile` and its hash-locked dependencies. Freeze a reviewed `references.bib` and matching `citation_map.json` in the template alongside the venue inputs. The reviewed-input adapter uses those citations for the writing phase. Google Search grounding and Semantic Scholar network discovery are disabled in the writer container.

Set `PAPERORCHESTRA_ENABLED=true`, `PAPERORCHESTRA_IMAGE` to the inspected immutable image reference, `GEMINI_API_KEY`, the Gemini model allowlist and reviewed price ceiling, and the existing shared spending ledger variables. The managed Gemini 2.5 Flash path runs without container network access or provider credentials. The host broker validates the generation request, reserves its input and output ceiling and forwards it once under a deadline. Run `scripts/paperorchestra.py run --job JOB_ID --seconds 1800`. Paid failure leaves reservations intact. Rerunning an interrupted job returns its reconciled status and attempts to remove its recorded container.

After generation:

```bash
backend/.venv/bin/python scripts/paperorchestra.py import-output \
  --job PAPERORCHESTRA_JOB_ID \
  --output /absolute/path/upstream_output
```

Import requires LaTeX source, copies supported manuscript/figure files, rejects symlinks and bundles exceeding 50 MiB, and retains separate snapshots for repeated imports. Imported files are never executed. An imported PDF does not prove generation provenance, compilation success, or scientific correctness.

## Review boundary and UI

Feynman Workbench → Research engines shows PaperOrchestra's source status and prepared/imported jobs. Read-only routes:

- `GET /api/paperorchestra/jobs`
- `GET /api/paperorchestra/jobs/{job_id}`

Every job remains `publication_eligible: false`. Imported drafts stay outside `vault/04_Drafts`; citation-to-vault mapping, numerical claim grounding, venue/layout validation and human review are still required. Existing publisher gates remain unchanged. No automatic conversion of arbitrary BibTeX entries into trusted vault papers is implemented.

Tests cover the pinned upstream CLI flags, required inputs, artifact tampering, path traversal/symlinks, repeated imports, PDF-only rejection, and read-only API access. See the release validation report for image evidence and the status of provider-backed generation.
