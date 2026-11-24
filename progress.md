# Progress

## November 23, 2026

- Read requested planning and system-design guidance and current code/configuration.
- Created persistent task, findings and progress files; continued from existing release plan and acceptance contract.
- Beginning reproducibility/CI work. No paid calls or deployment performed.
- Added build-input audit and six regression tests; all six passed. Current writer inputs, immutable Docker bases and engine source declarations passed; backend lock check resolved 106 packages and pinned installed source-byte verification passed.
- Added separate frozen-install/source verification CI job and frontend lint. Full backend/frontend checks running.
- Isolated offline installation could not complete because its fresh cache lacks an ormsgpack wheel. Did not alter the existing environment or use a replacement spending ledger.
- Full backend suite passed 387 tests (seven warnings); after isolating the universal-skills tests, all 12 affected tests passed (two warnings). Frontend four tests and production build passed; lint zero errors/109 warnings.
- Added code-grounded design review with ingress throttling, disk capacity, licensing, alerting and external acceptance gaps. These remain open; no production completion claim.
- Isolated frontend on 3000 and backend on 18000 returned HTTP 200 for all four required surfaces. Owned process groups stopped and temporary state removed. Whitespace check passed; new build audit passed Gitleaks. Changes are local and uncommitted; previously observed Git metadata restriction remains unresolved.

## Continued implementation

- Implemented authentication throttling, unique revocable sessions, API/UI sign-out, request byte limits, job payload/disk admission, aggregate operations diagnostics, monitor CLI/supervision examples and authenticated-mode skill distribution gate.
- Targeted security/queue/publisher checks: 22 passed. Operations/distribution/access/skill fixture checks: 17 passed before final diagnostics additions.
- Deployment runbook describes exact behavior and boundaries; no external destination, paid run or account-wide billing control was invented.
- Added HTTPS scholarly-origin PDF download allowlist, no redirect following or environment proxies, 20 MiB decoded-byte bound and regression cases. Full backend suite then passed 405 tests/seven warnings. Frontend four tests/build passed; lint zero errors/109 warnings.
- Authenticated real-process local check: all four HTTP surfaces 200; anonymous/foreign-origin rejection, Secure cookie flags, captured-cookie rejection after sign-out, expected operations alerts and oversized request rejection passed. Ten-client/100-request health smoke: zero errors, p95 0.0088 seconds; this is not a staging soak. Receipt: docs/local-authenticated-validation-2026-11-23.json.
- All owned validation processes stopped; original ledger hash unchanged. No paid inference, public deployment or off-host recovery performed.
- Final review restricted six experimental legacy executor routes to local mode; 48 final boundary regressions passed/two warnings. Reviewed 30 changed source/config/documentation files with Gitleaks: no leaks. Whitespace check passed. All changes remain local and uncommitted; Git metadata writes are restricted in this session.

## Completion follow-up

- Inspected GitHub run https://github.com/dev4-gpt/ResearchOS/actions/runs/45309065824 for pushed `afc09af`: frontend and reproducibility jobs succeeded; integrity submission/provenance checks passed, but pytest collection failed on missing `openai` and `pymupdf`. Later integrity steps did not run. CI resolved dspy 3.5.0 transitively despite the dspy-ai 3.3.0 compatibility pin. Added direct dspy 3.3.0, openai 2.53.0 and PyMuPDF 1.28.2 requirements plus import preflight. Clean remote verification remains pending the follow-up commit/push.

- Monitor parser/output and response-size protections added with ten passing regression tests. Full backend verification running on the final local tree; no frontend changes since its passing build/tests.
- Operator has not selected a deployment destination. Explained API-backed operation needs no application-host GPU. Read-only storage inspection: Mac has 1.8 GiB available; Docker Desktop directory is 26 GB. No files, images, volumes or containers removed.
- Existing hosting, live workflow inputs/budget, alert and backup/recovery targets remain required; no infrastructure provisioned.
- Final complete backend suite: 421 passed/seven warnings in 57.74 seconds. Repeated authenticated local integration: four surfaces 200, all access/revocation/body-limit checks passed, 100 requests/ten clients/zero errors, p95 0.0117 seconds. Processes stopped and original ledger hash unchanged. Existing budget remains cap $5, reserved $4.794125, available $0.205875.
- Prepared `scripts/commit-production-checkpoint.sh`: explicit reviewed source/doc paths only, refuses a pre-staged index or unexpected branch, scans before/after staging, then commits/pushes. Bash syntax validation passed. It has not been executed here because Git metadata writes are restricted. User can run it from normal Terminal; no new Codex session required.
