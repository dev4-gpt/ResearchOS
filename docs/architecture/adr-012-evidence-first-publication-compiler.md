# ADR-012: Evidence-First Publication Compiler

## Status
Accepted

## Decision

ResearchingOS uses a modular monolith with a typed evidence ledger, claim-level provenance, versioned venue profiles, deterministic PDF QA, and a fail-closed release controller. Obsidian remains the human-readable projection; the run ledger is the machine-verifiable source of truth.

Synthetic dry-run artifacts, unsupported claims, invalid citations, failed builds, and venue violations cannot be released as camera-ready outputs.

## Rationale

The previous pipeline allowed independent endpoints and LLM outputs to declare readiness. This caused unsupported metrics, invalid BibTeX keys, stale PDF artifacts, and venue-incompatible exports to pass through. A single release controller makes every artifact decision auditable and reproducible.

## Trade-offs

- Some existing drafts will become blocked until their citations and evidence are repaired.
- Official venue packages must be installed or pinned; generic fallbacks are not submission-valid.
- Obsidian and the ledger introduce a projection boundary, but this is preferable to treating free-form Markdown as a database.
