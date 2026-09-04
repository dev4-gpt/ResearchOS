---
name: run-submission-gate
description: Wraps scripts/run_submission_gate.py, the provenance-audit-and-venue-allocation gate that must pass before any manuscript is submitted or released, so an external agent harness can invoke it and interpret its exit code and reports.
---

# Run Submission Gate

Use before any release, submission, or when asked whether a manuscript is ready to ship. Audits every quantitative claim in `vault/04_Drafts/*.md` against `runs/<run_id>/measurements.jsonl` and allocates one venue per manuscript.

## 1. Command

| Purpose | Command |
|---|---|
| Standard run | `backend/.venv/bin/python scripts/run_submission_gate.py` |
| Strategy override | `backend/.venv/bin/python scripts/run_submission_gate.py --strategy {balanced\|max_acceptance\|prestige}` |
| Cap competitive-venue allocations | `... --max-competitive N` |

Run from the repo root. Requires `backend/.venv` to already exist.

## 2. Exit codes

| Code | Meaning |
|---:|---|
| 0 | `GATE: PASSED` — every quantitative claim traces to evidence |
| 1 | `GATE: BLOCKED` — at least one claim is ungrounded, or an identity placeholder remains |

## 3. Outputs (written to `vault/00_System/`, versioned with the manuscripts)

- `CLAIM_PROVENANCE_REPORT.md` — per-manuscript claim counts (experiment-backed / citation-backed / ungrounded)
- `VENUE_ALLOCATION.md` — one allocated venue per manuscript
- `submission_gate.json` — machine-readable version of both, including per-claim `cite_keys`, `grounding`, and `evidence` path

## 4. What it does NOT check

Citation *relevance* (does the source actually support the claim) is a separate, non-gating concern — see the `run-research-experiments` skill's `review_citations.py` reference, or run it directly: `backend/.venv/bin/python scripts/review_citations.py --by-key`.

## 5. Known false-negative: iCloud materialization race (ERR-088)

This repo lives under iCloud Drive. A `BLOCKED` result can be a false negative if `runs/**/measurements.jsonl` has not finished on-demand materialization. **Never trust a single BLOCKED run** — re-run once with unchanged inputs before reporting it as fact.

## 6. Workflow position

Run **after** `scripts/experiments/resync_manuscripts.py --apply` (or `--check`) on any session that touched a manuscript or re-ran an experiment. The gate checks a different thing than resync: resync keeps the draft equal to the run; the gate checks that every number in the draft resolves to a hashed artifact.
