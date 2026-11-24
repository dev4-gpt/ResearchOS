# Release completion checklist

Outcome: LOCAL WORK COMPLETE — production gates blocked.

## Repository — PASS

- [x] `4ab172f` is an ancestor of `ebbda0e`. GitHub branch lookup confirmed remote tip `ebbda0eeb310d5aee6bd02223b22cb80d4be84a9` before this documentation commit.
- [x] `backend/uv.lock`, `deploy/runtime/writer-requirements.lock`, and `integrations/research_engines.lock.json` are tracked.
- [x] `uv lock --check --offline --directory backend`: passed, 106 packages resolved from existing cache.
- [x] All 19 direct writer requirements are present in the lock and satisfy input version constraints. The Dockerfile consumes this lock with `--require-hashes`.
- [x] `python3 scripts/setup_research_engines.py --check`: all installed pinned upstream source hashes verified. The setup script and runtime consume the same tracked source lock.

## Local verification — PASS

Validation used a fresh temporary vault and job databases, disabled dotenv loading in Python, and an environment allowlist without provider credentials or the spending-ledger setting. No paid calls were made. Existing services and private data were not replaced.

| Check | Evidence |
| --- | --- |
| Full backend suite | `python -m pytest backend/tests -q`: 381 passed, seven deprecation warnings, 57.37 seconds |
| Frontend tests | `npm test`: four passed |
| Production build | `npm run build`: TypeScript and Vite passed |
| Lint | `npm run lint`: exit 0, zero errors, 109 existing warnings |
| Frontend | `http://127.0.0.1:13000/`: HTTP 200 |
| Backend health | `http://127.0.0.1:18000/api/health`: HTTP 200 |
| Vault listing | `http://127.0.0.1:18000/api/vault/files`: HTTP 200 |
| Draft listing | `http://127.0.0.1:18000/api/vault/files?category=drafts`: HTTP 200 |
| Publisher download integrity | `test_bundle_preserves_each_published_revision_and_rejects_artifact_damage` passed: separate completed revisions return their own bytes; missing/changed manifests, stage events, PDF, TeX and bibliography return 409; missing job ID returns 422 and unknown job returns 404 |
| Cleanup | Both owned server process groups terminated and reaped; temporary validation state removed; no validation processes left running |
| Spending preservation | Read-only SQLite inspection: cap $5.000000, reserved $4.794125, remaining $0.205875. Ledger SHA-256 identical before and after validation |

Backend download handler also explicitly rejects jobs whose status is not `completed` with HTTP 409. No implementation failure required a source change. Full local command output is retained outside Git at `/private/tmp/researchingos-release-validation.log`; it is ephemeral evidence, not a dependency of this checklist. This session did not rebuild Docker images or claim public TLS acceptance. Earlier local runtime/restore records were inspected as historical evidence only.

## Production gates

Existing configuration inspected: repository deployment examples, private dotenv field presence (values not copied), deployment runbook, release checkpoint and previous local validation records. Provider key fields exist locally, but no deployment, SSH, public origin, backup or recovery target fields were found in those dotenv files. Nginx still specifies `research.example`. No unrelated SSH alias was assumed to be an approved target.

| Gate | Status | Evidence and exact missing input |
| --- | --- | --- |
| Live provider workflows | BLOCKED | Historical Harness² attempts did not reach held-out scoring. Local fixtures and tests do not establish live acceptance. Need reviewed evaluation/manuscript inputs, approved provider/model and price-ceiling settings, and an end-to-end run profile whose conservative reservation fits the existing $0.205875. Historical smallest successful simulated trace was estimated above that allowance. No reservation reset, cap increase, or repeated paid attempt is permitted. If no valid profile fits, this gate remains blocked under the fixed $5 cap. |
| Public authenticated HTTPS | BLOCKED | Templates are placeholders; loopback HTTP does not satisfy public HTTPS. Need the approved existing server SSH target/login and access, public FQDN, certificate/DNS-validation method, and private operator configuration supplied securely. No paid infrastructure provisioned. |
| Encrypted off-host backup and recovery | BLOCKED | Prior evidence covers a local restore only. Need an approved encrypted backup destination and access, encryption/key custody method, and an existing isolated restore target with access. After deployment, restore the actual configuration/artifacts/databases and original spending ledger, verify historical downloads, and measure RPO/RTO. |

## Save and push

- [x] Preserve unrelated vault edits/deletions, private runtime outputs and existing ledger.
- [x] Include dependency/source locks in repository; exclude runtime locks, databases, credentials and unpublished manuscripts from this change.
- [x] Proposed checklist passed Gitleaks (no leaks) and staged whitespace validation.
- Delivery: this checklist is committed on `wip/backup-local-2026-10-19`; the final handoff records its commit hash and confirmed push result.

## Deferred next milestone

Optional NeMo Gym evaluation integration for actual research tasks, inspectable trajectories, verifiers and held-out comparisons of Harness²/AlphaEvolve. Preserve job identity, artifact hashes, timeouts and shared spending controls. Compare an optional Nemotron model on verified success, cost, latency and citation accuracy before changing defaults. LitmusBench belongs only in a future chemistry module with source licensing metadata and test-split isolation. No integration, downloads, training or independent verification of external resource claims was performed during this release preparation.

Stop at these blockers. No further paid runs or deployment/recovery attempts until the minimum inputs above are available within the unchanged budget.

## November 23 implementation follow-up (local, not yet committed)

Additional local hardening is recorded in `progress.md`, `task_plan.md` and `production-design-review-2026-11-23.md`. Added revocable sessions/sign-out, failed-auth throttling, request/job/disk admission bounds, protected operations metrics, monitor supervision examples, restricted PDF downloading, distribution approval gates and reproducibility CI checks. Experimental unqualified legacy executors are local-only in authenticated deployments.

Full backend suite passed 405 tests after the main changes; the final legacy-route restriction is checked separately. Frontend four tests/build passed with zero lint errors and 109 warnings. Authenticated local integration and short ten-client health probe passed; see `local-authenticated-validation-2026-11-23.json`. This is loopback HTTP with cookie flags inspected, not public trusted TLS acceptance or real-browser acceptance.

Remaining evidence: clean frozen install on CI (local offline cache lacked a wheel), vulnerability/image scans and actual rebuilt image probes; reviewed license permissions; live research/independent scientific review; public HTTPS/browser journey; target filesystem quota/retention and delivered alert; rollback/30-minute staging soak; encrypted off-host recovery. The original ledger was unchanged. These improvements do not close production acceptance.

Final local follow-up: all 421 backend tests passed, including legacy-route restrictions and ten monitor regressions. The authenticated real-process smoke was repeated successfully (four surfaces 200; ten clients/100 health requests, zero errors, p95 0.0117 seconds). Owned processes were stopped and the original ledger hash remained unchanged. Frontend source has not changed since its passing tests/build/lint. Hosting is still undecided; no GPU is required on the application host when using hosted model APIs. Mac storage inspection found 1.8 GiB available and Docker Desktop directory size 26 GB; no cleanup occurred.
