# Evidence-First Publication Compiler

## What changed

ResearchingOS now treats publication as a gated build process:

```text
research run → provenance ledger → claim/citation audit → venue build → PDF QA → peer review → human sign-off
```

Agents still propose sources, analyses, synthesis, and manuscript text. Deterministic services decide whether an artifact is safe to release.

The implementation adds:

- Canonical citation keys and typed source, evidence, claim, venue, manifest, and build-decision models.
- A durable `runs/{run_id}/` ledger containing source records, claims, synthesis, manuscript files, build artifacts, hashes, logs, and QA reports.
- Citation-level numeric verification against the cited paper instead of the entire corpus.
- Bibliography checks for empty keys, duplicate keys, and cited keys missing from the generated `.bib` file.
- Strict peer-review JSON validation. Parsing failure is a rejection, not an automatic acceptance.
- Fail-closed release states. Synthetic dry-run output cannot become camera-ready output.
- Venue profiles and TeX/PDF checks for page limits, required sections, identity leaks, local paths, placeholders, missing glyph artifacts, and forbidden tokens.
- Explicit provider modes: `auto`, `dry_run`, and `live`.
- O-1A evidence inventory language separated from EB-1A criteria and legal eligibility determinations.

## Why this is better

The previous pipeline allowed plausible-looking output to pass even when a number was unsupported, a citation key was broken, a peer-review response was malformed, or the PDF contained visible artifacts. The new pipeline makes those conditions observable and blocking.

The human review step is therefore narrowed to decisions automation cannot legitimately make: authorship, ethics, originality, interpretation, conflicts of interest, and final submission metadata.

## How to run verification

From `backend/`:

```bash
.venv/bin/pytest tests -q
.venv/bin/python ../scripts/security_scan.py
```

Use `RESEARCHINGOS_RUN_MODE=dry_run` for synthetic development runs. Those runs are useful for testing orchestration, but they are never releaseable.

## Required next actions

1. Rotate the Gemini and NVIDIA credentials currently detected in the local `.env`; never commit them.
2. Install the modern `google-genai` dependency in the live environment and remove reliance on the deprecated SDK fallback.
3. Provision and pin the official template package for each intended venue, including its version and hash. Missing packages must remain a build blocker.
4. Regenerate existing PDFs through the gated endpoint. Current historical PDFs are invalid until they pass the new QA report.
5. Replace the legacy `references.bib` artifact after the manuscript has valid provenance and citation metadata.
6. Add page-scope measurement for venues where references and appendices are excluded from the main-body limit.
7. Have an immigration attorney review the separate O-1A/EB-1A evidence inventories.

## Current acceptance rule

No PDF should be treated as camera-ready merely because LaTeX compiled. It must have a passing evidence audit, bibliography audit, strict peer review, pinned venue profile, successful compilation, passing PDF QA, and a reproducibility manifest.
