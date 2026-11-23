# Single-operator deployment

This implementation hardens one trusted operator on one host. It is not a multi-tenant service or a completed production certification. Research/meta-review and publisher jobs persist in SQLite; other engine/writer stages retain their existing manifests and CLI execution boundary.

## Configure and start

1. Use the approved existing private Linux host with supported Python, Node, Nginx and a rootless Docker runtime. Run under a dedicated unprivileged account with `umask 077`. Keep code, state and the vault outside iCloud/network/shared directories. Do not expose Docker's socket over the network or mount it into an internet-facing container.
2. Install backend dependencies from `backend/uv.lock` using `uv sync --project backend --frozen`. Build frontend with `npm ci && npm run build` in `frontend`. Leave `VITE_BACKEND_URL` unset for same-origin deployment. No secrets belong in Vite variables.
3. Supply environment variables using a private service environment file. Set `RESEARCHINGOS_ACCESS_MODE=authenticated`, a random `RESEARCHINGOS_PASSWORD` of at least 32 characters, `RESEARCHINGOS_OPERATOR`, explicit HTTPS `RESEARCHINGOS_ORIGINS`, explicit `RESEARCHINGOS_HOSTS`, and `RESEARCHINGOS_COOKIE_SECURE=true`. Set absolute `VAULT_PATH`, `RESEARCHINGOS_JOBS_DB` and `RESEARCHINGOS_PUBLISHER_DB`. All state directories must be writable only by the service account. Missing access configuration prevents worker startup.
4. Build, lock, scan and test the required TeX image. Set `RESEARCHINGOS_TEX_IMAGE=NAME@sha256:DIGEST` to its actual local digest. Configure separate engine/writer images per their runbooks. Do not substitute a fabricated digest. Compilation has no host fallback in authenticated mode. Give scratch/output storage a hard filesystem quota; command timeouts and memory limits do not impose a disk quota.
5. Start exactly one API process from `backend`: `.venv/bin/uvicorn main:app --host 127.0.0.1 --port 18000 --workers 1 --no-proxy-headers`. Adapt `deploy/researchingos.service.example` for supervised startup and run `systemd-analyze verify` against the resolved unit. Use restart-on-failure and a single process without reload. Multiple workers are rejected by exclusive job database locks. Bind only loopback and firewall the API port.
6. Adapt `deploy/nginx.conf.example` to your domain, certificate and frontend path; validate with `nginx -t` before activation. The proxy serves only frontend assets directly. Both `/api/` and `/vault/` go through authentication. Preserve same-origin requests and disable SSE buffering. Do not deploy with local access mode behind any proxy.
7. Sign in through the UI. It receives an eight-hour HttpOnly Secure cookie. Password rotation invalidates existing sessions. CLI probes use Basic credentials over HTTPS. Keep proxy access logs free of authorization/cookie headers. Restrict login attempts at the proxy.

## Jobs and recovery

Each accepted research/meta-review job has a UUID and durable events. Reuse the same `Idempotency-Key` for an uncertain POST only when its payload is identical; changed inputs return 409. The queue admits at most 100 queued/running jobs per database and returns 429 when full. SSE reconnects replay after `Last-Event-ID`; closing the browser does not cancel execution. Session storage restores the last job stream after refresh. The status endpoint is `/api/research/jobs/{id}`; cancellation only applies to queued work.

On restart, queued work resumes and previously running work becomes `interrupted`. Inspect provider usage and artifacts before explicitly creating replacement work. Interrupted paid stages never automatically retry. Publisher requests are retained separately instead of coalescing away accepted work. Authentication is shared operator access, not tenant ownership. Job/event history currently has no automatic expiry: monitor size, archive while stopped, and set storage alerts. Do not manually delete active rows.

## Backup and restore

Stop admission and gracefully stop the service before a consistent whole-system backup. If a worker cannot finish, stop the process, record the interruption and reconcile its provider/container effects. Copy the vault, the research and publisher SQLite databases, the spending ledger, all `runs/` manifests/artifacts and private deployment configuration to encrypted backup storage. Exclude secrets from general logs/reports. SQLite's backup API is valid for a database snapshot while running, but does not make the vault and job state a coordinated snapshot.

Restore to an isolated host with no provider credentials or external egress. Check file permissions, open all three databases, run `PRAGMA integrity_check`, verify artifact hashes and confirm queued/interrupted states. A unit test exercises SQLite backup/restore; an operator must still perform and record a full vault/artifact restore drill. Proposed initial objectives: RPO 24 hours, RTO 1 hour, then revise from measured results.

## Release evidence required

- HTTPS smoke: frontend, authenticated backend health, vault listing and draft listing all return 200; anonymous API/artifact requests return 401; foreign origin is rejected; secure cookie login and SSE work in a browser.
- Actual locked-image TeX and PaperOrchestra execution, including timeout, cleanup, quota exhaustion and network isolation/egress policy tests.
- Budget-capped live provider runs for discovery, Harness², the AlphaEvolve adapter and manuscript generation; benchmark and citation review. A source pin or demo run does not prove equivalence to Google's hosted AlphaEvolve.
- Provider-account billing controls and dedicated validation credentials remain an operator deployment gate. The application enforces shared reservations and request deadlines, and the queue runs each council or meta-review job in a deadline-bound subprocess.
- Full backup restoration, job crash recovery under real execution, load/latency measurements and alert delivery. Alert on process failure, queue age, interrupted/failed jobs, disk capacity, provider quota and backup age.
- Additional expensive legacy endpoints and CLI jobs are not governed by the research queue's admission limit. Review and restrict them before broader exposure. Multi-user access requires tenant authorization, separate credentials/data boundaries and additional resource accounting.

Do not label this deployment production-ready until these gates have recorded evidence. Automated tests validate implemented boundaries, not operational SLOs or scientific correctness.

## Cumulative validation spending and restore tooling

Managed model paths, including council DSPy, Scout, the engine adapters, reproducibility and the PaperOrchestra broker, require `RESEARCHINGOS_SPEND_LEDGER` (one persistent SQLite path shared by every run) and `RESEARCHINGOS_SPEND_CAP_USD`. The validation cap authorized on 2026-11-21 is $5. Reservations are atomic and rounded up, persist after restart and are not released on ambiguous failures. Changing an existing ledger's cap implicitly is rejected. Keep the ledger in the backup scope; deleting it discards spending history. The ceiling still depends on valid model pricing and token bounds. These are application-side reservations. Account-wide billing still depends on controls at each provider. Set approved model IDs and reviewed per-provider price ceilings; retain the same ledger path and cap across worker and CLI invocations. Native fx execution remains disabled pending a metered integration.

`scripts/provider_smoke.py` makes exactly one text-only request with no tools, no retries and at most 128 output tokens. It requires the shared ledger settings, records sanitized diagnostics and sends only a generic connectivity prompt. It is not an end-to-end engine or manuscript test. Model prices were checked against https://ai.google.dev/gemini-api/docs/pricing on 2026-11-21; the smoke's $100/million-token reservation ceiling is deliberately conservative, not a quoted price.

`scripts/restore_drill.py` takes exclusive managed-worker/vault locks, rejects symlinks, verifies the source is unchanged during copying, restores vault/run data into a private temporary directory and checks every file hash and any SQLite databases. It removes temporary copies afterward and never replaces source data. Stop independent CLI writers first. Run `python3 scripts/restore_drill.py --report docs/restore-drill-result.json`. The local drill does not provision an encrypted off-host backup or restore deployment secrets; those remain separate release requirements.

## Existing-host HTTPS acceptance

Obtain the exact public FQDN and SSH target/login for the existing service host, plus the certificate or DNS-validation method. Confirm the agreed host and existing services before activation. Build the frontend without `VITE_BACKEND_URL`, record the deployed image digests and use the service account’s private environment file. Leave provider-backed paths disabled until the model allowlists, reviewed ceilings, existing shared ledger and provider account limits are configured. The private API listens on port 18000. Keep any other service already bound to port 8000 running.

After Nginx and certificate verification, run `scripts/check_release_connectivity.py --frontend https://FQDN --backend https://FQDN --authenticated` from a client with the normal trust store. Set the operator secret in its private environment. Record each HTTP status, anonymous and foreign-origin rejection, cookie attributes and browser SSE reconnection. Check `/api/ready` with authentication and an explicit dry-run job and publisher download before enabling the paid paths.

## Off-host recovery acceptance

Use an approved encrypted off-host backup destination and a separate existing restore host or an isolated recovery environment. Record the snapshot timestamp, source revision, image digests, deployment file versions, and encrypted backup object identity. Include application data, the original spending database with pacing state, and encrypted copies of private settings and certificate material. Scope the key material and restore credentials to the recovery operator.

Restore using the deployment's documented ownership and paths with provider credentials withheld and outbound model traffic disabled. Verify hashes and run SQLite integrity checks. Start one restored backend with a loopback reverse proxy. Verify the four release surfaces, interrupted and queued job state, a historical verified publisher download, and the restored spending budget. Measure RPO from the data timestamp and RTO from restore start to verified service, then record both against the 24-hour RPO and one-hour RTO objectives. The evidence package should contain checksums, statuses and elapsed times. Keep passwords, API keys and private keys in the encrypted backup.
