# Production findings

- Current architecture is a single-operator FastAPI/React workspace with SQLite durable jobs, job-bound verified publisher bundles and isolated execution. No evidence supports multi-tenant production readiness.
- Roadmap commit is `2862fe8`; last historical local receipt reports 381 backend tests and four frontend tests.
- CI frontend runs npm ci/tests/build but omits lint. CI backend installs requirements-ci.txt; no separate frozen backend lock validation or pinned upstream download/check job exists.
- Writer Dockerfile consumes a hashed writer lock; frontend and backend have tracked locks. Independent CI environments are needed to avoid perturbing numerical experiment dependencies.
- Live Harness², public HTTPS and off-host restore remain blocked. Remaining historically recorded allowance is $0.205875, not an authorization increase.
- Jam with AI index was read earlier in this conversation; it is a concept map, not executable configuration. No need to reread every linked article to test these project-specific guarantees.
- Refreshed the index and official uv locking documentation during execution: `--frozen` alone does not check metadata drift, so CI must first run `uv lock --check`.
- Research skills expose license notes but currently activate verified advisory entries regardless of license clearance. Commercial distribution remains a release-review requirement; no permission can be inferred from source visibility.
- Clean-runner bug found: universal skill discovery test required >10 operator-installed global skills. Replaced that dependency with original synthetic temporary skill documents; production discovery is unchanged.
- Added process-local bounded failed-auth throttling across protected paths, nonce-bearing registered sessions and server-side sign-out revocation; restart invalidates browser sessions. Valid credentials bypass failure lockout to keep the single operator recoverable.
- Added 10 MiB aggregate request bound (including chunked bodies), 1 MB managed job payload bound, and low-disk rejection of new work. These do not replace an actual deployment filesystem quota or admission controls for every legacy tool.
- Added authenticated aggregate operations endpoint plus a credential-redacting monitor CLI and timer/service examples. Alert delivery and hard quota validation still require the approved target.
- Authenticated deployments now default-deny uncleared advisory skill activation/content; per-skill distribution approval requires an actual license review before setting it.
- Hosting remains undecided after operator response. Mac free space: 1.8 GiB; Docker Desktop directory: 26 GB; project `.tools` 204 MB, vault 256 MB, runs 26 MB, frontend dependencies 168 MB. These are filesystem observations, not a Docker image/volume deletion inventory. No cleanup occurred. Backend venv is a symlink to `/Users/aryamandev/.venvs/researchingos` and was not measured by the initial directory-size command.
- Monitor follow-up fixed an unhandled non-object JSON response and replaced syntactic alert validation with an explicit alert-name allowlist; responses are limited to 64 KiB. Ten regressions passed.
