# Production design review — November 23, 2026

Status: partially verified; release remains incomplete. This review follows the existing single-operator scope and acceptance contract.

## Findings and actions

| Priority | Code/evidence | Consequence | Required action and acceptance |
| --- | --- | --- | --- |
| High | `docs/release-completion-checklist.md`: no completed live engine/writer chain | Fixtures do not establish scientific or provider correctness | Reviewed held-out inputs and bounded funded profile; independently review every required artifact before release |
| High | `deploy/nginx.conf.example`: placeholder hostname/certificate; login throttling applies only to `/api/session` while `OperatorAccess` accepts Basic credentials on other paths | Public deployment unverified; session-only throttling does not bound password attempts elsewhere | Apply rate controls to every credential-bearing path at the approved ingress, test repeated bad credentials and legitimate SSE, then verify public TLS and access |
| High | Deployment runbook requires a hard filesystem quota; no measured target quota/retention receipt exists | Timeout/memory limits alone cannot prevent storage exhaustion | Configure target filesystem quota and artifact retention; inject full-disk failure and verify recoverable job state and retained historical bundles |
| High | Restore receipts cover local copies; actual backup/restore destinations absent | Host loss recovery is unproven | Encrypted off-host backup and isolated startup with original budget database, historical downloads and measured RPO/RTO |
| Medium | CI did not validate the frozen backend install or source-lock downloads; frontend lint omitted | Existing local installs can hide missing or stale build inputs | Added separate reproducibility CI job, audit script and lint; clean CI and Docker image receipts still required |
| Medium | Skill manifest contains unlicensed/noncommercial reference notes; runtime activation checks advisory mode and hashes | Source verification does not establish distribution permission | Review per-source terms; exclude uncleared third-party content from shipped images/bundles and verify installed distribution inventory |
| Medium | No approved alert destination or delivery receipt | Queue failure, old backups and exhausted capacity may go unnoticed | Select recipient; implement correlated health/queue/disk/budget/backup signals and exercise delivery without manuscript/credential leakage |

## Architecture and capacity assumptions

Browser requests go through same-origin HTTPS ingress to the authenticated loopback API. Submission is persisted in SQLite before work; a single exclusive worker claims it, runs bounded isolated execution, persists results/events, and the browser reconnects using stored event sequence. Completed publisher jobs identify their own manifests and artifact bytes. The shared spending ledger must remain the reservation authority across processes.

Retain this topology until measurements require a change. Ten concurrent browser clients is a proposed load test, not a throughput guarantee. For illustration, 100 queued jobs at 15 minutes per job on one worker imply roughly 25 hours of work; a queue cap alone does not bound acceptable waiting time. Measure job age and reject/defer admission when an approved age threshold is exceeded. Size artifact capacity as measured bytes per run × runs per day × retention days plus snapshots and headroom; no measured payload distribution or retention decision is available yet.

Stateful recovery and model quality are separate gates. Do not introduce cache, sharding, Kubernetes or a replacement orchestrator without evidence of the bottleneck and a recovery/consistency contract. No service availability SLO or broad multi-user launch is certified here.

## Implemented in this checkpoint

- `scripts/check_build_inputs.py` verifies exact hashed writer dependencies against input constraints, immutable Docker bases and source-lock declarations including path traversal rejection.
- Six regressions exercise drift, missing hashes, unsafe source paths and removal of build hash enforcement.
- CI checks backend metadata drift before frozen sync and verifies downloaded source bytes; frontend lint runs with existing tests/build.
- Universal-skills discovery test now uses original temporary fixtures; its API test uses temporary vault/slides state.

Checks do not replace dependency vulnerability scanning, license clearance, real image builds, actual GitHub CI execution or the outstanding security/operational work above.

## Follow-up implementation

The application now adds failed-auth throttling across protected routes independently of the ingress, unique registered/revocable browser sessions with sign-out, request and managed-job byte limits, low-disk admission rejection, aggregate queue/worker/disk/budget/backup diagnostics and a monitor command with supervisor examples. Authenticated advisory-skill content/activation is default-denied until per-skill distribution approval is recorded. PDF downloads use an exact HTTPS scholarly-host allowlist, no redirects or environment proxies, and a 20 MiB byte bound. Unsupported PDF origins fall back to metadata/abstract handling; this narrows full-text ingestion and must be included in live discovery acceptance. Network egress controls and hostile PDF parser resource isolation still require deployment review.

These changes address portions of the findings, not all acceptance receipts. Ingress defense in depth, actual filesystem quota, retention approval, alert delivery, independent license determination, full legacy tool admission/deadline audit, clean CI/image execution and live/deployed recovery evidence remain open. Sessions reset on restart; authentication failure counters are process-local. Single-process scope remains mandatory.
