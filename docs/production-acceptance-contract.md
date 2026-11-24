# Production acceptance contract

Prepared November 23, 2026 after roadmap commit `2862fe8`. Status: DRAFT — targets below are planning assumptions; external deployment decisions remain unconfirmed. This document grants no new spending or infrastructure authorization.

## Release boundary

One trusted operator on one approved host, with FastAPI/React, a single API process, SQLite job stores, an immutable artifact bundle per completed publisher job, and isolated code/writer/TeX runtimes. Multi-user tenant isolation is outside this release. The operator may prepare and download manuscripts; publication/submission remains a separate explicitly authorized action.

Sources of truth: SQLite for accepted job identity, state and events; per-run manifests and hashed artifacts for outputs; the existing shared spending database for reservations. Discovery metadata is not proof of full-text grounding. A generated ranking, manuscript or model verdict is not independent experimental evidence.

## Proposed acceptance measurements

| Property | Target and measurement | Required receipt |
| --- | --- | --- |
| Local correctness | Full backend/frontend checks and reproducible clean-checkout builds pass | CI URL, commit SHA, lock hashes, image digests and sanitized output |
| Control-plane capacity | 10 concurrent clients for 30 minutes; p95 health/job-status latency <1s; unexpected errors <1%; intentional 401/403/409/429 counted separately | Load configuration, response distribution, queue age and resource samples |
| Admission | Managed stores retain capacity 100 queued/running jobs per DB; all other expensive paths have explicit bounded admission | Saturation probe, expected rejections, recovery after drain |
| Accepted-work correctness | Zero lost accepted jobs; identical idempotency keys return original outcome; changed payload rejected; interrupted paid work not automatically replayed | Failure injection before/after persistence and external effects |
| Artifact integrity | Historical revisions return their original bytes; missing/modified required artifacts prevent download | Two-revision and tamper receipts through deployed API |
| Research quality | Reviewed corpus and held-out labels fixed before optimization; zero fabricated citation identities in accepted bundle; every numeric claim supported or removed; independent candidate replay succeeds within declared tolerances | Reviewer decisions, model/prompt/input versions, run IDs and hashes; report failures |
| Execution cost | Every managed paid path reserves before dispatch and observes deadline; ambiguous failures retain reservations | Shared-ledger concurrency, exhaustion and crash receipts plus provider-account controls |
| HTTPS/access | Four public surfaces return expected 200; anonymous API/download rejected; foreign origin rejected; Secure/HttpOnly cookie, expiry and SSE reconnection work | Public TLS checks and real-browser journey |
| Recovery | Encrypted off-host snapshot restored with credentials withheld; RPO ≤24h and RTO ≤1h | Hash inventory, SQLite integrity, original budget totals, startup and historical download evidence |
| Operations | Alerts reach designated operator; disk quota/retention and dependency outage recover predictably; rollback preserves compatible state | Alert receipt, disk/queue/outage probes and rollback result |

These are staging acceptance tests, not a measured availability SLO. Research-job completion is measured separately against each run's approved time/token/tool limits; a fast HTTP acceptance response does not establish completed research.

## Pending operator decisions

| Input | Current state | Blocks |
| --- | --- | --- |
| Existing SSH target/account and public FQDN | Not supplied; `research.example` is a placeholder | Deployment and public acceptance |
| TLS issuance/renewal method | Not supplied | Trusted public HTTPS and renewal rehearsal |
| Backup destination, credentials and key custodian | Not supplied | Encrypted off-host backup |
| Isolated recovery target | Not supplied | Off-host restore and measured RPO/RTO |
| Alert destination and responsible operator | Not supplied | Alert delivery and operational handoff |
| Reviewed corpus, evaluation labels, manuscript/bibliography and reviewer | Not supplied for live acceptance | Scientific validity and end-to-end live workflow |
| Approved provider/model, price ceilings and request quotas | Must be reviewed for the chosen live profile | Reliable bounded paid execution |
| Sufficient validation allowance | Recorded cap $5; reserved $4.794125; available $0.205875; no increase authorized | Any live profile exceeding remaining conservative allowance |

Supply secret material through private configuration on the relevant host, never this document or committed artifacts. Reinspect actual allowance before any paid execution. Never create a fresh ledger to bypass its historical reservations.

## Evidence and stopping

Record PASS, FAIL, BLOCKED or NOT RUN per criterion in `release-completion-checklist.md`, with timestamp, release revision, relevant image/config/input hashes and an accessible sanitized receipt. Old local results remain historical until revalidated for the release candidate. Unknown destinations cannot be inferred from unrelated cloud accounts or SSH aliases.

Milestone 1 is only fully passed after pending decisions and target assumptions are confirmed. Continue independent reproducibility/security/operations work while those decisions are pending. Final release requires all applicable acceptance rows passed; otherwise report exact blockers and stop paid/deployment work.
