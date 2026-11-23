# Production resource decisions

Planning review: November 23, 2026. No dependencies installed, model calls made, deployment performed or new capability implemented in this pass.

## System design source

Read the [Jam with AI system-design index](https://jamwithai.substack.com/p/system-design-for-engineers-all-concepts), plus the local `skills/system-design-review/SKILL.md` and its failure/AI production checks. The index organizes 162 concepts and linked articles/videos; it is a learning map, not an application repository or deployable template. This pass read the index, not every linked article. Apply requirements, estimates, idempotency, bounded queues, consistency, recovery and observability to the actual architecture. Do not add sharding, Kubernetes or distributed queues merely because they appear in the index.

## Candidate decisions

| Resource | Decision | Acceptance before adoption |
| --- | --- | --- |
| Existing OpenResearch, Harness², AlphaEvolve adapter, PaperOrchestra | Retain existing integrations; close live qualification | Current pins/licenses, bounded paid calls, held-out evaluation, artifact verification; do not claim equivalence to hosted AlphaEvolve |
| [restic](https://github.com/restic/restic) | Candidate encrypted off-host backup tool | Pin reviewed version, verify license/backend support, protect repository key, coordinated snapshot and isolated restore with measured RPO/RTO |
| [OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python) | Candidate instrumentation | Compatibility and overhead check; propagate job IDs; redact prompts, source text and credentials by default; verify exporter outage does not block jobs |
| [k6](https://github.com/grafana/k6) | Candidate control-plane load testing | Pin version; use synthetic staged requests, bounded duration/load, no uncontrolled paid jobs; measure latency/errors/queue age and recovery |
| [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym) | Optional isolated evaluation integration | Verify current APIs and runtime requirements, pinned environment, trajectories/verifiers and held-out tasks; all inference uses existing budget boundary |
| [LitmusBench v0.2](https://huggingface.co/datasets/nvidia/Nemotron-RL-litmus-bench-v0.2) | Optional chemistry-only evaluation | Preserve source-specific licensing and original splits; no test-set tuning or general research-quality claim |
| [Nemotron for Science](https://nvidianews.nvidia.com/news/nvidia-introduces-nemotron-for-science-to-accelerate-discoveries-with-agents) | Optional model comparison | Verify accessible model/API, hardware, license and pricing; compare identical tasks, success, cost, latency and citation accuracy before changing defaults |
| Prior starred shortlist: Giskard, research skill collections, SPACE, Shepherd | Review only when an explicit gap survives existing tooling | See `starred-research-assessment.md`; recheck upstream revision, license, security, compatibility and maintenance; run a bounded spike before adoption |

The earlier local starred assessment records 191 listings across seven pages. Today's attempts to fetch the user's stars page, including a paginated URL, were blocked; the connector exposes no dedicated starred-list operation. This is not a fresh audit of all stars. New repositories are candidates, not automatic dependencies. Official repository pages for restic, OpenTelemetry Python and k6 were opened during this pass; code/security audits were not performed.

## Execution evidence

For each release requirement record: status, target, exact commit/image/config/input versions, command or probe, timestamp, observed result, sanitized receipt location and unresolved gap. Keep secrets and unpublished materials private; put hashes and sanitized outcomes in Git. Refresh receipts after changes invalidate them. References to untracked local evidence must either become sanitized tracked receipts or clearly identify their restricted external location before release.

Initial scope is a trusted single operator. Before inviting independent users, define identity/tenant ownership across every storage, queue, SSE, retrieval and download path, then test cross-user rejection. The current shared operator credentials do not implement those guarantees.
