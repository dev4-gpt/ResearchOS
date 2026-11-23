# Production hardening verification — 2026-11-20

## Result

Implemented the single-operator hardening plan. Release status remains **blocked pending operational evidence**. No external deployment or paid provider run was performed.

## Checks executed

- **157 backend tests passed**, with two existing `datetime.utcnow()` deprecation warnings. Scope: production boundaries, publisher jobs, API, research workflow, PaperOrchestra, research engines, Scout discovery, LaTeX exporter, venue exporter, vault and publisher readiness. This was a targeted regression suite, not the entire repository suite.
- **3 frontend tests passed**: failed mutations do not retry, network failures propagate without replay, caller idempotency keys are retained, and API/stream/artifact URLs share the configured origin.
- TypeScript compilation and Vite production build passed.
- SQLite tests cover concurrent idempotency, queue capacity, exclusive worker ownership, interrupted-job recovery, durable events and database backup restoration.
- API tests cover anonymous access rejection, secure cookies, foreign-origin rejection, password rotation, startup configuration, SSE replay/terminal events, disconnected subscribers and worker readiness reporting.
- Compiler tests assert production requires a pinned image and uses isolated Docker arguments with cleanup; these are mocked execution checks, not live container validation.
- Real HTTP smoke started fresh temporary backend/frontend processes on loopback ports 18876/13000 with private temporary state, ephemeral credentials and no provider keys. Results:

| Check | HTTP result |
| --- | --- |
| Frontend | 200 |
| Authenticated backend health | 200 |
| Authenticated vault listing | 200 |
| Authenticated draft listing | 200 |
| Anonymous API | 401 |
| Anonymous artifact | 401 |

The smoke processes were stopped and temporary state removed. This does not establish deployed HTTPS/browser/SSE behavior through Nginx. Existing services on other ports were untouched.

The prerequisite script run separately against default ports found frontend 3000 unavailable and the service at 8000 returning 404 for ResearchingOS routes. It verified upstream source pins and OpenResearch `orx 0.2.18`; engine execution/provider configuration and candidate/writer runtime prerequisites were not enabled in the probe environment. The script does not load `.env`, so these results describe that invocation, not every possible private configuration.

## Reproduce

```bash
backend/.venv/bin/python -m pytest backend/tests/test_production_boundaries.py backend/tests/test_publisher_jobs.py backend/tests/test_api.py backend/tests/test_research_workflow.py backend/tests/test_paperorchestra.py backend/tests/test_research_engines.py backend/tests/test_scout_discovery.py backend/tests/test_latex_exporter.py backend/tests/test_venue_exporter.py backend/tests/test_vault.py backend/tests/test_publisher_readiness.py -q
cd frontend
npm run build
npm test
```

The existing virtual environment needed `socksio` for its configured SOCKS proxy; verification used an isolated temporary dependency directory. `httpx[socks]` is now declared in the backend dependencies and CI requirements, and the backend lockfile records it. Recreate deployment environments from the lockfile rather than depending on the temporary test environment.

## Remaining release gates

Follow `production-deployment.md`: configure real HTTPS/service supervision, provider-enforced budgets and bounded legacy calls, locked runtime images and storage/egress limits; exercise all four integrations live with a reviewed dataset; record a full vault/artifact restore, crash recovery, load measurements and alert delivery. Legacy expensive endpoints still need resource governance for unattended/broader use. No multi-tenant authorization was added.
