# ADR-013: Separate O-1A and EB-1A Evidence Profiles

## Status
Accepted

## Decision

The evidence tracker stores O-1A and EB-1A portfolios separately and reports documented evidence only. It never returns an automated legal eligibility confirmation.

## Rationale

The former tracker mixed O-1A language with EB-1A regulatory citations and inferred judging, originality, and media criteria from internal system activity. Publication quality signals are useful portfolio evidence, but they are not themselves legal determinations.

## Consequences

- Every evidence item must identify its external source and date.
- Automated peer review is not counted as judging the work of others.
- A lawyer-facing dossier can be generated, but requires professional review before use.
