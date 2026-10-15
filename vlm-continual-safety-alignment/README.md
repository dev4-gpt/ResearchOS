# VLM Continual Safety Alignment

Faithful replication of Bach, Nguyen, Le, Tran, "Continual Safety Alignment via Gradient-Based Sample Selection" (arXiv:2604.17215v1), extended to vision-language models — the paper's own named future-work item ("Extending gradient-based selection to vision-language models... requires further investigation," Section F).

**This project is fully independent of the rest of this repository.** It does not use `scripts/`, `backend/`, or `run_submission_gate.py`, and has no relationship to `papers/p6/` (an earlier, unrelated attempt in this repo that claims the same topic but never actually loaded a VLM or ran on a GPU — left untouched, out of scope here).

## Scope and status

See [`docs/paper-analysis.md`](docs/paper-analysis.md) for a faithful summary of what the source paper actually claims, and [`docs/method-mapping.md`](docs/method-mapping.md) for every LLM→VLM substitution made, each backed by a real citation.

Target: a paper draft by December 2026, built for a professor/advisor audience, with every reported number traceable to an actual executed run.

## Ground rule

**No number goes into `docs/` or a manuscript unless it comes from a `runs/<run-id>/metrics.jsonl` line.** No placeholders, no estimates presented as results. `runs/<run-id>/manifest.json` records model, LoRA config, dataset + subsample size/seed, and git commit hash for every run.

## Layout

```
docs/            paper-analysis.md, method-mapping.md, architecture.html
configs/         model / task / hyperparameter configs (yaml)
src/
  selection.py       Algorithm 1 (gradient-based sample selection), LoRA-param-scoped
  train.py           LoRA continual fine-tuning loop
  eval_safety.py     ASR via MM-SafetyBench / FigStep / JailBreakV-28K + per-benchmark judge protocols
  eval_basin.py      VISAGE-style weight-space perturbation measurement
  eval_capability.py lmms-eval / task-accuracy wrapper
  data/              per-dataset loaders
runs/            <run-id>/manifest.json + metrics.jsonl per experiment
notebooks/       exploratory only — never a source of reported numbers
```

## Models

Three VLMs are the default target (not a stretch goal), validated stepwise then run in parallel — see [`docs/method-mapping.md`](docs/method-mapping.md#1-base-models) for the full rationale:

1. **Qwen2-VL-2B-Instruct** — smallest, used alone in Phase 1 to validate the pipeline and the phenomenon cheaply
2. **LLaVA-1.6-7B** — different architecture/vendor lineage (Vicuna/LLaMA-based)
3. **LLaVA-RLHF** — explicitly RLHF-safety-aligned, closest to the paper's own starting models

The pipeline is config-driven (`configs/<model-name>.yaml`) so adding models #2 and #3 in Phase 2 requires no code changes — only new configs.

## Current phase

Phase 0 (setup) — see the plan for the full phased breakdown:
- **Phase 1** (must-have): core hypothesis replication on Qwen2-VL-2B-Instruct only — the stepwise validation gate before scaling to all three models.
- **Phase 2** (must-have): full 4-task continual sequence on all three models, run in parallel once compute allows.
- **Phase 3** (should-have): additional baselines/robustness across all three models.
- **Phase 4** (stretch): O-LoRA baseline, per-model sample audit.
- **Phase 5**: write-up, including cross-architecture comparison.
