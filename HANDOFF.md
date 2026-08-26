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

### 4. Current state

**All 9 manuscripts: 116 claims, 0 ungrounded. Gate exits 0. 108/108 builds.**
74 pages total, 6–11 pages each, all with figures and Appendices A–F.

Venue allocation: p2→ICML (competitive), p9→IEEEtran, p1→IEEE Access,
p3/p6/p7→ACM, p4→SpringerOpen, p5→MDPI, p8→arXiv.

---

## Is this ready to publish? No. Be honest with the user about this.

The **integrity** problem is solved. The **contribution** problem is not.

**Blocking:**

1. **Main bodies are 1,500–3,000 words under target.** Appendices are well-provisioned;
   the argument sections are thin. p6 is 2,093 words against 5,182.
2. **85 citations remain flagged** as topically weak (`vault/00_System/CITATION_REVIEW.md`).
   These need author judgement — do **not** auto-replace. A previous attempt proposed
   swapping InstructGPT for *"Automated Fracture Image Captioning."*
3. **Four papers are missing template sections** (p2 Experiments, p7 Analysis, p4
   abstract/intro/analysis, p8 several by design).
4. **The contributions are modest.** Honest, reproducible, and modest. p3's finding is
   "an SMT stage we added contributed nothing." p1's is "our method didn't beat BM25."
   These are publishable as negative results in the right venue, but they are not
   strong-acceptance papers at a top conference, and nobody should tell the user they are.
5. **p8 reports no results at all** — correctly, since it needs GPUs.

**Also open:** ERR-044 (FactChecker numeric detection broken, 1 failing test),
ERR-046 (ACM branch emits no author metadata), ERR-063 (**API keys sitting in iCloud
sync-conflict folders `Projects 2` and `Projects 4` — the user should delete these and
rotate the keys**).

---

## What "production level" would mean here

Ranked by what actually moves the needle:

1. **Get one paper grounded on a real benchmark.** Everything here is CPU-measurable
   modelling. One paper with a genuine SWE-bench Lite run behind it is worth more than
   nine analytical ones. This needs GPU access or cloud credits, and it is the single
   highest-value thing outstanding.
2. **Wire the gate into CI.** `run_submission_gate.py` should block merges. Right now
   it is run manually and nothing enforces it.
3. **Fix or retire the legacy audit chain.** Checkmate and FactCheckerService still
   report green on things the provenance gate catches. Two graders that disagree is a
   defect in the graders (ERR-056 — partly reconciled, not finished).
4. **Finish the main bodies.** Deliberate authorship, not generation. Padding will
   reintroduce exactly what was removed.
5. **Then submit — one venue per paper, sequentially.** Not 108 packages.

---

## Rules that will save you time

- **Never write a number into a manuscript by hand.** Generate it from
  `measurements.jsonl` (`manuscript_sync.py`). A hand-typed value drifted 940→943
  between two runs of the same script and nobody noticed (ERR-052).
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
