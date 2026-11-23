# ResearchingOS Reproducibility Agent

The coding component targets the **main Gemma 4 Developer Agent competition**.
The experiment report can also support a separate paper-track submission. The
main competition scores passing repository repairs, not manuscript quality.

Official references, reviewed October 26, 2026:
- [Competition requirements](https://www.kaggle.com/competitions/gemma-4-developer-agent)
- [Paper track](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper)
- [ADK Agent Config](https://adk.dev/agents/config/)

## What is implemented

`scripts/run_reproducibility.py` exports a pinned **local Git repository** into a
fresh disposable tree for every task and approach. The original checkout is never
patched. Repository history, symlinks, API credentials, and host model settings
are not mounted in the test container. Model operations are structured JSON:
list, read, edit, test, and finish. No model-selected host shell commands run.

Three approaches share the same checkpoint, issue, baseline, source edit allowlist,
test command, wall-clock cap, cumulative input/output-token cap, step cap, and
tool-output cap:

| Approach | Navigation |
|---|---|
| plain | list and read files |
| lexical | plain plus BM25 file ranking |
| graph | lexical plus AST import edges and call-name candidates |

The AST graph does not perform complete Python name resolution. Ambiguous names
are labeled as candidates. This graph differs from Kaggle's provided graph and
embedding tools; local results do not establish official-harness performance.
Execution order rotates between tasks. Temperature is zero, but deterministic
model output is not guaranteed. Warm-cache effects and GPU scheduling remain
limitations; use multiple runs and a held-out task split for publishable claims.

Tests execute in Docker using a locally installed image pinned by digest, without
network, root privileges, host environment variables, or writable host mounts.
The image must provide Python and preinstalled project dependencies. Tests run
from a temporary container copy. A resolution requires a failing baseline, a
nonempty source patch, and a passing final validation command. A passing process
is a local development signal; official hidden tests remain authoritative.

## Run the complete fixture workflow

```bash
docker pull python:3.12-slim
docker image inspect python:3.12-slim --format '{{index .RepoDigests 0}}'
# Use the returned immutable image reference:
backend/.venv/bin/python scripts/run_reproducibility.py --demo \
  --image python@sha256:YOUR_LOCALLY_INSTALLED_IMAGE_DIGEST
```

The fixture asks whether arithmetic-mean code implements its stated method. It
records three failing assertions, applies a scripted denominator repair, and
records the three passing assertions, patch, and report for each approach.
**No model runs in this mode.** Every artifact is labeled synthetic; the claim
verification API rejects these results as empirical evidence. Its method excerpt
is a fixture specification, not an academic citation.

## Run a live Gemma comparison

Serve an approved Gemma 4 checkpoint behind an OpenAI-compatible `/v1` endpoint.
There is no fallback to Gemini, another provider, or mock inference. The endpoint
must return its exact configured model identifier and actual token usage. Use
`REPRO_GEMMA_BASE_URL` explicitly; existing ResearchingOS API keys are not reused.
An endpoint identifier does not cryptographically attest the weights it serves;
record your serving configuration and checkpoint provenance externally.

Create a JSON array of tasks:

```json
[
  {
    "id": "issue-001",
    "repository": "/absolute/path/to/local/checkout",
    "commit": "FULL_40_CHARACTER_COMMIT_SHA",
    "question": "Does the implementation satisfy the supplied method?",
    "issue": "A specific reproducible bug description",
    "paper_id": "exact_vault_paper_id",
    "method_excerpt": "A checked excerpt or a clearly labeled hypothesis",
    "editable_paths": ["src/module.py"],
    "test_command": ["python", "-m", "pytest", "-q", "tests/test_regression.py"],
    "image": "project-runtime@sha256:FULL_64_CHARACTER_IMAGE_DIGEST"
  }
]
```

```bash
export REPRO_GEMMA_BASE_URL=http://127.0.0.1:9000/v1
# Set REPRO_GEMMA_API_KEY only if your selected endpoint needs it.
backend/.venv/bin/python scripts/run_reproducibility.py --tasks /path/to/tasks.json \
  --model gemma-4-31b-it-qat-w4a16-ct --seconds 180 --tokens 32000 --steps 16
```

The runner does not fetch papers, clone remote repositories, build images, install
dependencies, train weights, or submit to Kaggle automatically. Pin and review
the input repositories, source excerpts, and test commands before evaluation.
The task manifest is a trusted operator input. Do not select tests based on which
approach wins; freeze the task set and budgets before comparing approaches.

`runs/reproducibility/<run>/` contains:
- `summary.json`: pinned tasks, budgets, per-approach outcomes and resource use.
- `<task>/<approach>/result.json`: baseline and validation commands and logs.
- `<task>/<approach>/patch.diff` and `trajectory.json`: exact edits and model actions.
- `artifacts.json`: SHA-256 manifest of the evaluation artifacts.
- `report.md`: readable evidence report with links to logs and patches.

Feynman Workbench → **Reproducibility** displays these reports. The HTTP interface
reads reports and verifies named measurements; it cannot launch arbitrary code.

## Claim verification and manuscript use

`POST /api/reproducibility/runs/<run>/verify` accepts:
`{"arm":"graph","metric":"resolved","value":2}`.
It verifies artifact hashes and the exact named metric. A number occurring
elsewhere in a run cannot verify this claim. Fixture runs are always blocked.
Hashes detect changes relative to a saved manifest; they are not independent
attestations that a model, dataset, or scientific conclusion is authentic.

The existing FactChecker now requires exact normalized citation keys; plausible
author-year keys receive no verification credit. Strict numeric prose checks
accept exact attributed source sentences, or explicit `claim_text` bindings with
an `artifact_root`, underlying `artifact`, and matching `sha256`. Loose historical
measurement rows and bare matching values cannot certify arbitrary prose.
Contribution/novelty statements require review instead of automatic verification
from citation existence. This intentionally blocks legacy drafts that relied on
the older shortcuts. It does not implement general scientific entailment.

For academic drafts, follow the existing measurement → manuscript resync →
submission-gate workflow; do not paste numbers into manuscript prose manually.
Reproducibility reports currently remain separate from manuscript resync.

## Competition candidate

`notebooks/kaggle/researchingos_gemma4.ipynb` prepares the candidate on Kaggle,
checks GPU access, locates the mounted harness README, and displays the organizer
sample configs. It deliberately does not invent an evaluation command. At setup
time the account had not joined the competition and Kaggle gated those files
behind rule acceptance; the existing account flow also showed phone verification
pending. Official execution cells remain pending inspection of the actual harness.

`competition/gemma4/agent.yaml` and its prompt use the competition's documented
harness tools. Package them with:

```bash
backend/.venv/bin/python scripts/package_gemma_candidate.py \
  --output /tmp/researchingos-candidate-submission.zip
```

This is a **candidate config, not a validated submission**. It uses native
harness tools rather than the local JSON protocol, so its behavior needs separate
evaluation. Before entry, run the current official `HARNESS_README.md` validator
in a competition notebook, verify tool/config compatibility and supported model
variants, evaluate public development tasks, and inspect failures. No LoRA is
included. Do not claim a benchmark improvement until live measured results exist.
