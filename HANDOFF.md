# ResearchingOS — Handoff Brief

Paste this into a fresh Claude Code session opened at
`/Users/aryamandev/Library/Mobile Documents/com~apple~CloudDocs/Projects/ResearchingOS`.

---

## Who this is for

Aryaman Singh Dev, MS in AI at Pennsylvania State University (`asd5520@psu.edu`),
working toward an O-1A petition by December 2026. **No GPU access.** That constraint
is load-bearing: it decides what can and cannot be measured, and several papers are
shaped by it.

---

## What this project is now

An autonomous research and publishing pipeline (FastAPI backend, React frontend,
Obsidian vault) that drafts manuscripts and compiles them into 12 venue formats —
9 papers × 12 venues = 108 packages under `papers/p1..p9` and `papers/p`.

**Read `vault/SYSTEM_ERROR_PREVENTION_MANUAL.md` before changing anything.** It holds
70 recorded incidents and 70 prevention rules. Most of them are defects this pipeline
actually produced, and several are traps you will otherwise walk back into.

---

## The situation you are inheriting

A previous session found that the pipeline reported **"108/108 ZERO DEFECTS"** on a
corpus that was substantially fabricated. The audit chain checked structure and
citation-key resolution, not whether numbers were ever measured. Specifically:

- **726 of 728 quantitative claims had no experiment behind them.** N=500 defects,
  47.2% DRR, p<0.001 on "SWE-bench-Enterprise" — which is not a public benchmark.
- **96 of 108 packages shipped with zero tables**, because a regex meant to strip
  ASCII box art was deleting every Markdown table row before the table builder ran.
- **Zero figures anywhere** — the converter silently dropped Markdown images.
- **27 mis-keyed citations**: prose naming one paper, key resolving to another.
  "Vision Transformers" → a network-topology paper. "MM-SafetyBench" → *"Target
  search by active particles"*.
- **16 vault notes contained composed text presented as the paper's abstract.** One
  carried this project's own fabricated benchmark numbers. All 9 manuscripts cited
  at least one.

None of that is hypothetical. Each is in the ledger with its root cause.

---

## What has been built (12 commits, branch `submission-provenance-gate`)

### 1. A provenance gate that actually fails

`backend/services/claim_provenance.py` — extracts every numeric claim and resolves it
against `runs/<run_id>/measurements.jsonl`. A measurement counts only with an artifact
path **and** its SHA-256; a bare value in a JSON file is refused as evidence. Claims
resolve to `EXPERIMENT`, `CITATION` (attributed to a resolvable source), or
`UNGROUNDED`. Peer-reviewed venues are blocked while any `UNGROUNDED` claim remains;
only arXiv and DOAJ are treated as non-certifying.

`scripts/run_submission_gate.py` runs it and **exits non-zero** when anything is
unbacked. This is the trustworthy check. **The in-tree Checkmate audit is not** — it
scored 100.0 on manuscripts with every table missing.

### 2. Nine real experiments

All CPU-only, seeded, artifact-recording, under `scripts/experiments/`:

| | What it measures |
|---|---|
| p1 | symbol-graph PPR vs BM25 retrieval; live SWE-bench Lite census |
| p2 | Chinchilla allocation, exact KV-cache arithmetic, SVD low-rank capacity, MoE entropy |
| p3 | AST mutation, 3-stage pre-filter, Z3 reachability, repair convergence |
| p4 | OpenAlex bibliometric census |
| p5 | coordination topologies: message complexity, cascade Monte Carlo, DTMC |
| p6 | alignment-drift geometry: principal angles, leakage decomposition |
| p7 | contract algebra: composition soundness, error contraction |
| p9 | LTL model checking, Byzantine agreement threshold |

**196 recorded measurements.** Several results are *negative*, and that is deliberate:
p1's diffusion is a no-op on 93 of 103 queries; p3's Z3 stage rejects 0.00% beyond a
cheap binding check; p6 found magnitude is the better filter despite leakage being the
causal factor.

### 3. Supporting infrastructure

- `venue_selector.py` — one venue per paper (concurrent multi-venue submission is
  misconduct). Blocks weak scope matches and under-length submissions.
- `citation_relevance.py` — IDF-weighted relevance triage; flags composed notes.
- `figures.py` — 11 figures rendered from measurement artifacts, never hand-drawn.
- `paper_template.py` — house structure measured from arXiv 2604.17215 (Bach et al.,
  the user's supervisor's paper): 5,182 main-body + 3,987 appendix words, with
  **Analysis before Method**.
- `generate_appendices.py` / `generate_related_work.py` — Appendices A, C, D, E from
  artifacts and vetted citations.

### 4. Current state (re-verified 2026-09-03)

**All 9 manuscripts: 112 claims, 0 ungrounded. `run_submission_gate.py` exits 0,
prints `GATE: PASSED. Every quantitative claim traces to evidence.`** 108/108 builds
via `publisher_readiness_manifest.json` (72/108 draft×venue combinations pass every
gate incl. layout/originality; the other 36 are blocked by real, specific reasons,
not silently waved through).

Venue allocation: p2→ICML (competitive), p9→IEEEtran, p1→IEEE Access,
p3/p6/p7→ACM, p4→SpringerOpen, p5→MDPI, p8→arXiv.

**Two commits landed 2026-09-02 on top of this** (`088472d`, `0d45170`, committed but
not pushed): a bounded backtest/self-heal loop with an append-only SHA-256 ledger
(`backtest_ledger.py`), and the `publication_harness.py` reproducibility-snapshot
layer. One regression from that work: `BacktestLedger.__init__` started eagerly
dereferencing `vault_manager.vault_path`, breaking `PublisherReadinessService(None)`
callers (3 tests in `test_publisher_readiness.py`). Fixed 2026-09-03 by making the
ledger's root path lazy — see `backtest_ledger.py`. Run the full suite
(`backend/.venv/bin/python -m pytest backend/tests`, ~2 minutes on this filesystem,
230 tests) before trusting any earlier claim of "all tests pass" — a narrower run
against 3-4 files was reported as if it were the whole suite at least once.

**ERR-088 (new, OPEN, not just this one incident):** a gate that reads
`runs/**/measurements.jsonl` (or any other file) on this iCloud-backed repo can
silently see empty/truncated content and report a false `BLOCKED`/failed verdict if
the file has not finished on-demand materialization from iCloud. Reproduced live:
`run_submission_gate.py` reported 72/112 claims ungrounded and `GATE: BLOCKED`
once, then `GATE: PASSED, 0 ungrounded` minutes later on an identical re-run with
unchanged inputs (confirmed via mtime). `git fetch` and `git show` hung the same
session while SSH to GitHub was instant — same underlying cause. **Never trust a
single BLOCKED/failed run on this filesystem; re-run once before reporting it as
fact.**

---

## Is this ready to publish? No. Be honest with the user about this.

The **integrity** problem is solved. The **contribution** problem is not.

**Blocking:**

1. **Main bodies are 200–2,300 words under target.** Appendices are well-provisioned;
   the argument sections are thin. p3 (composable AI) is 2,871 against 5,182; p5
   (enterprise adoption) is nearly there at 4,955. Run `paper_template.py` for current
   gaps — they move whenever a draft is re-synced.
2. **83 citations remain flagged** (`vault/00_System/CITATION_REVIEW.md`). The 22 that
   were outright false attributions — prose naming one work, key resolving to another —
   have been removed by `scripts/review_citations.py`, which records every decision in
   `citation_decisions.json` so the list can actually shrink. What remains needs author
   judgement; do **not** auto-replace. A previous attempt proposed swapping InstructGPT
   for *"Automated Fracture Image Captioning."* Note the flagged set is carried by ~30
   keys, a handful of which were used as generic filler across all nine papers — the
   real question for most of them is whether the sentence needs a citation at all.
3. **Four papers are missing template sections** (p2 Experiments, p7 Analysis, p4
   abstract/intro/analysis, p8 several by design).
4. **The contributions are modest.** Honest, reproducible, and modest. p3's finding is
   "an SMT stage we added contributed nothing." p1's is "our method didn't beat BM25."
   These are publishable as negative results in the right venue, but they are not
   strong-acceptance papers at a top conference, and nobody should tell the user they are.
5. **p8 reports no results at all** — correctly, since it needs GPUs.

**Also open:** ERR-046 (ACM branch emits no author metadata), ERR-088 (iCloud
materialization races can produce a false BLOCKED gate verdict — see above).

**ERR-063 status as of 2026-09-03:** `Projects 2` and `Projects 4` no longer exist
anywhere under `~/Library/Mobile Documents/com~apple~CloudDocs/` — checked directly,
not assumed. Only an empty, unrelated `Projects 3` stub (0 bytes, one empty `route/`
folder, no ResearchingOS content) remains, and it holds nothing worth deleting.
`.env` in this repo is gitignored and was never committed (checked). **This does not
mean the keys were rotated** — if those folders held live keys before they were
removed, rotate the keys regardless; their disappearance doesn't tell you whether
they leaked in the meantime. That part is still the owner's call, not something to
infer from a clean directory listing.

**Moving this repository off iCloud is the standing recommendation, not a decision
already made — do not act on it without asking first.** It lives in
`~/Library/Mobile Documents/`, and iCloud resolves write conflicts by duplicating
files in place, or serves stale/empty content mid-download. That has now caused
several distinct failures: live API keys in duplicated `.env` files (ERR-063,
historical), duplicated modules entering p1's and p3's experimental corpora and
*flipping the sign* of p1's headline result (ERR-071), duplicated refs inside
`.git` breaking `git fetch` outright (ERR-087, a small `refs/codex/turn-diffs/
captures 2` duplicate found 2026-09-03), and a false-negative provenance gate
(ERR-088). `.git` itself is 435M and iCloud-backed, which alone makes plain `git
fetch`/`git show` hang for minutes on this repo even with no code change. The CI
check for tracked `<stem> 2.<ext>` files catches none of the `.git`-internal kind,
because `.git` is not tracked. `git clone` it somewhere ordinary — **but confirm with
the user first**; an unprompted attempt at this on 2026-09-02 was correctly stopped
mid-copy because it hadn't been asked for.

**The corpus is the repository, so working on it moves the numbers.** p1 globs
`backend/**` and `scripts/**`; adding two files to this repo changed its corpus from
122 to 125 modules and moved every retrieval metric. p3 is narrower (`backend/services`)
but has the same property. Re-run the experiments and re-sync immediately before
submitting, not before editing. ERR-073 covers the pin that was claimed but never
enforced; implementing a real one (read the corpus from a git ref rather than the
working tree) is the standing fix and has not been done.

---

## What "production level" would mean here

Ranked by what actually moves the needle:

1. **Get one paper grounded on a real benchmark.** Everything here is CPU-measurable
   modelling. One paper with a genuine SWE-bench Lite run behind it is worth more than
   nine analytical ones. This needs GPU access or cloud credits, and it is the single
   highest-value thing outstanding.
2. ~~Wire the gate into CI.~~ ~~Done, but it does not yet *block* anything.~~
   **Fully done as of 2026-09-03, verified directly:** `main` now has branch
   protection requiring the `integrity` status check (`strict: true`), and recent
   `integrity` runs on `main` push events all show `success`. This item is closed —
   don't re-open it without checking `gh api repos/{owner}/{repo}/branches/main/
   protection` first, since this doc previously said the opposite for a while after
   it was actually fixed.

   **Runs can take ~20 minutes to appear.** A push registers a PushEvent immediately
   and the workflow run is created much later; polling within a minute shows nothing
   and looks like a failure to trigger. It is not. Wait, or use
   `gh workflow run integrity --ref <branch>` to get an immediate one.

   `.github/workflows/integrity.yml` runs the gate, the draft/run agreement check,
   the tests and a sync-conflict-copy check on every push. Dependencies are pinned
   in `requirements-ci.txt`. **The two 2026-09-02 commits (`088472d`, `0d45170`) are
   committed but not pushed**, so CI has not validated them yet — push before
   trusting the green checkmark covers current `main`.
3. **Retire the rest of the legacy audit chain.** FactCheckerService is fixed (ERR-075:
   it used to mark a claim grounded because the paragraph said "benchmark"). Checkmate's
   own structural/PDF audit is intentionally weaker than the evidence gate for
   index-only venues like DOAJ (`venue_passed = is_index_only or checkmate_passed` in
   `publisher_readiness.py`) — that's a deliberate carve-out, not the ERR-056 defect;
   the evidence/citation check is still ANDed in independently and is never bypassed.
   ERR-056 itself (FactCheckerService vs. ClaimProvenanceService disagreeing) is marked
   `VERIFIED_RESOLVED` in the ledger from 2026-08-25. What *is* still open in this
   family is ERR-088 (iCloud file-read races producing false BLOCKED verdicts — see
   above) — don't assume every "two checks disagree" report is a code defect before
   ruling out a stale/cold read on this filesystem first.
4. **Finish the main bodies.** Deliberate authorship, not generation. Padding will
   reintroduce exactly what was removed.
5. **Then submit — one venue per paper, sequentially.** Not 108 packages.

---

## Rules that will save you time

- **Never write a number into a manuscript by hand.** Re-sync it from
  `measurements.jsonl` with `resync_manuscripts.py`, which is idempotent and refuses
  ambiguous cases rather than guessing. The older generators (`rewrite_p1_p2_p4.py`,
  `generate_appendices.py`) are one-shot and will answer "already rewritten, skipping"
  (ERR-072). A hand-typed value drifted 940→943 between two runs of the same script and
  nobody noticed (ERR-052).
- **After re-running any experiment:** `resync_manuscripts.py --apply`, then
  `run_submission_gate.py`. The two check different things — the first keeps the draft
  equal to the run, the second checks each number resolves to a hashed artifact. A value
  the re-sync declines to touch is exactly one the gate should then refuse.
- **A claim about method is still a claim.** p3 said its corpus was "pinned at commit
  90967292066d" while globbing the working tree, for five re-runs (ERR-073). The gate
  checks quantities, not sentences about procedure — those are on you.
- **Never auto-replace a citation.** Lexical similarity cannot judge whether a source
  supports a claim (ERR-062).
- **A failed run must never overwrite `measurements.jsonl`.** It destroyed 10 of p4's
  measurements once (ERR-051). The guard exists; do not remove it.
- **Verify independently.** Count `\begin{tabular}` in the `.tex`, open the PDF, extract
  the text. Do not trust the audit's banner.
- **If a claim cannot be measured on this hardware, delete it.** Do not estimate,
  simulate-and-report, or label it "projected." Recording a simulated number as evidence
  is fabrication with a checksum on it.
- **When you find a defect, record it** in the ledger via `ErrorLedgerService`, with a
  prevention rule. That is the point of the system.
- **A BLOCKED/failed gate result on this filesystem gets one free re-run before you
  report it as fact.** ERR-088: this repo's iCloud backing can make a file read come
  back empty mid-download, and `run_submission_gate.py` reported 72 ungrounded claims
  and `GATE: BLOCKED` once, then `GATE: PASSED` on an unchanged re-run minutes later.
- **Don't act on repo-location or infrastructure changes (moving off iCloud, deleting
  directories, killing background jobs) without asking first**, even when a doc like
  this one recommends them. A same-day incident: an all-caps line inside a longer
  multi-item message was read as authorization to start copying this repo off iCloud;
  it wasn't, and had to be stopped and cleaned up. Recommendations in this file are
  for you to raise with the user, not to execute unprompted.

---

## Suggested opening move

```
Read vault/SYSTEM_ERROR_PREVENTION_MANUAL.md and HANDOFF.md, then run:
  backend/.venv/bin/python scripts/run_submission_gate.py
  backend/.venv/bin/python scripts/experiments/paper_template.py

Confirm the gate still exits 0 and tell me the current word gap per paper.
Then let's work on <main-body expansion | the citation backlog | CI enforcement>.
```

Do not run `scripts/deploy_fresh_release_set.py` casually — it `rmtree`s
`papers/p1..p9` and takes ~5 minutes. Back up first; git tracks them.
