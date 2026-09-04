---
name: run-research-experiments
description: Wraps the p1-p9 experiment scripts under scripts/experiments/, plus resync_manuscripts.py and paper_template.py, as ResearchingOS's measurement pipeline — there is no unified runner, so this documents the per-script invocation, run_id-to-manuscript mapping, and the resync-then-gate verification loop.
---

# Run Research Experiments

Use when asked to re-run an experiment, refresh a manuscript's numbers, or check word-count progress against the house template. There is **no single "run all" entrypoint** — invoke each `pN_*.py` script individually.

## 1. Scripts and what they measure (each takes no CLI args; each is hardcoded to one manuscript's `run_id`)

| Script | Writes to `run_id` | Manuscript stem |
|---|---|---|
| `p1_symbol_graph_retrieval.py` | `draft-review_symbol_graph_rag_vs_qlora_swe_bench_lite` | `review_symbol_graph_rag_vs_qlora_swe_bench_lite` |
| `p1b_swebench_retrieval.py` | same as p1 | same |
| `p2_scaling_laws.py` | `draft-review_architectural_dynamics_long_12_page` | `review_architectural_dynamics_long_12_page` |
| `p3_ast_repair.py` | `draft-autonomous_code_synthesis_and_self_healing_multi_agent_systems` | `autonomous_code_synthesis_and_self_healing_multi_agent_systems` |
| `p4_literature_census.py` | `draft-review_enterprise_genai_roi` | `review_enterprise_genai_roi` |
| `p5_coordination_topologies.py` | `draft-review_enterprise_adoption_of_multi_agent_ai_systems_infr` | `review_enterprise_adoption_of_multi_agent_ai_systems_infr` |
| `p6_alignment_geometry.py` | `draft-review_continual_safety_alignment_in_vision_language_models` | `review_continual_safety_alignment_in_vision_language_models` |
| `p7_contract_composition.py` | `draft-review_composable_ai_systems_for_trustworthy_agentic_pipelines` | `review_composable_ai_systems_for_trustworthy_agentic_pipelines` |
| `p9_formal_verification.py` | `draft-review_trustworthy_multi_agent_systems_formal_verification` | `review_trustworthy_multi_agent_systems_formal_verification` |
| `p10_adversarial_provenance.py` | n/a (mutation battery against the gate itself) | CI-only, run with `--check` |

No script exists for `review_spatio_temporal_grounding_in_video_question_answering` (needs GPU; out of scope — do not fabricate a substitute).

## 2. Invocation

```
backend/.venv/bin/python scripts/experiments/<script>.py
```

Run from repo root. Each writes `runs/<run_id>/{artifacts/*.json, measurements.jsonl, experiment_manifest.json}` via `ExperimentRecorder` (`scripts/experiments/harness.py`). Refuses to overwrite existing measurements without an explicit reseed path — re-running is safe and idempotent by design.

## 3. After any experiment run, project results into the manuscript

```
backend/.venv/bin/python scripts/experiments/resync_manuscripts.py --apply
backend/.venv/bin/python scripts/run_submission_gate.py
```

Never hand-edit a number into a manuscript. `resync_manuscripts.py` is the only supported path from `measurements.jsonl` into prose; the gate is the only supported check that every remaining number is grounded. Flags: `--only STEM` to restrict, `--check` for CI (no writes), `--seed-from GITREF` to bootstrap sidecars on a stale draft, `--reseed` after a hand-reconciled draft, `--seed-also METRIC=OLDVALUE` to bootstrap a metric a run only ever printed in prose.

## 4. Word-count gap check (report-only, no args)

```
backend/.venv/bin/python scripts/experiments/paper_template.py
```

Reports main/appendix word counts against the house template (5182 main + 3987 appendix words, from arXiv 2604.17215) and lists any structurally missing sections per manuscript.

## 5. Corpus-sensitivity warning

`p1_symbol_graph_retrieval.py` globs `backend/**` + `scripts/**`; `p3_ast_repair.py` globs `backend/services`. Any code change under those paths moves their metrics — re-run the affected script and resync before trusting the gate again. Editing `.agents/skills/**` or `vault/**` does not touch either glob.

## 6. GPU-dependent work

None of p1-p10 requires a GPU. The video-QA manuscript's missing experimental sections do, and are out of scope until GPU access exists — do not write results-shaped prose with invented numbers to fill that gap.
