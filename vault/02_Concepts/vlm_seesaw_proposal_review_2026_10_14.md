---
title: "VLM safety seesaw: proposal assessment before v3 results"
project: "vlm-safety"
status: "proposal_review_measurement_validation_required"
review_date_local: "2026-10-14"
manuscript_ready: false
v3_status: "Local notebook code reviewed; Claude transcript says built but not run on GPU; outputs not available"
---

# VLM safety seesaw: proposal assessment

The professor's seesaw question is worth testing, but the available pilot does not establish a seesaw. It measures refusal differences between input conditions in fixed models. A seesaw claim needs evidence that the same intervention improves safety in one modality while reducing it in the other. The strongest next proposal separates that claim from prompt mismatch, comprehension failure, judge error and benign over-refusal.

This is a targeted proposal review, not a completed systematic review or a manuscript. It uses locally available v1/v2/v3 notebook code, saved v1 outputs, the recovered v2 results ZIP, current plans, original PDFs and selected primary literature. The pasted Claude transcript says v3 was built but had not yet run on a GPU; no v3 result bundle was found. The authenticated Claude chat was unavailable, so conclusions below use the pasted transcript and local primary artifacts rather than unseen chat content.

## Project and version identity

`blissful-bose` and `Safety Alignment for VLMs Research` refer to the same `/Users/aryamandev/Developer/blissful-bose` workspace, with origin `https://github.com/dev4-gpt/blissful-bose.git`. The original continual-training project and the recent measurement proposal are successive research directions, not separate repositories.

| Available evidence | What it establishes | Limit |
|---|---|---|
| Original README and continual-alignment notebook | Earlier gradient-based sample-selection direction | Does not define the current seesaw experiment |
| `vlm_modality_tradeoff.ipynb` | v1 implementation | Judge and prompt controls need validation |
| `bundle/` | v1 smoke outputs, 40 items per group (5 per scenario) | Do not pool with larger runs |
| `bundle (1)/` | v1 full pilot, 240 harmful items per group (30 per scenario); includes steering | Exploratory; do not pool with v2 |
| `vlm_modality_tradeoff_v2.ipynb` | v2 implementation | Results are in a separate ZIP |
| `/Users/aryamandev/Downloads/bundle.zip` | v2 run, 304 harmful items per condition (38 per scenario), benign controls and steering | ZIP lacks exact prompt/image copies and per-label response IDs |
| `vlm_modality_tradeoff_v3.ipynb` | Local v3 code reviewed; transcript says built, not run | No completed v3 results audited here |

The intake extracted all pages from 20 unique local PDF files. These are not automatically 20 distinct studies: proceedings/preprint or annotated editions can represent the same work. Bibliographic deduplication, figure inspection and claim verification remain necessary.

## Define the seesaw precisely

There are three different questions:

1. **Static modality gap:** does a fixed VLM behave differently for text-only versus image-conditioned versions of an intent? The current B/C comparison addresses this imperfectly.
2. **Intervention-induced trade-off:** does a specified safety intervention increase image safety while decreasing text safety on matched, held-out items? This is the core seesaw test.
3. **Safety versus usefulness:** does increased refusal also block benign requests or damage comprehension? This is a separate cost and must be reported alongside either result.

For a frozen checkpoint and specified intervention setting λ, let H_m(λ) be the adjudicated harmful-completion probability for modality m, and S_m(λ) = 1 − H_m(λ). The latter requires adjudication of ambiguous, incomplete and unreadable outputs; absence of a refusal phrase is not sufficient. Also report explicit refusal R_m, benign over-refusal O_m, and benign task performance U_m separately.

Relative to λ = 0, estimate ΔS_text(λ) and ΔS_image(λ) on the same paired intent set. An image-directed trade-off requires a credible image improvement and text deterioration beyond predeclared practically relevant margins, with uncertainty on both contrasts. A strict zero-sum claim additionally requires evidence that ΔS_text + ΔS_image remains within a prespecified equivalence margin across the tested settings. A nonsignificant sum is not equivalence evidence. One negative comparison cannot establish a universal conservation law.

Positive item-level text/image correlation also does not rule out a trade-off under intervention. Likewise, shared internal refusal structure can coexist with unequal recognition or routing. These are different estimands. Frozen-model activation steering tests an inference-time intervention; it cannot establish what future continual training will do.

## Literature implications for the proposal

| Primary work | Relevant evidence | Consequence for this project |
|---|---|---|
| [[vlm_local_cmrm_357d4867022c]] — [CMRM, ACL Findings 2025](https://aclanthology.org/2025.findings-acl.186/) | Modality-related representation shifts and inference-time safety recovery | Modality degradation and representation correction are established prior work |
| [[vlm_mars_2606_31876]] — [MARS, version 2](https://arxiv.org/abs/2606.31876v2) | Textual refusal-direction transfer, modality re-centering and adaptive steering | Shared steering alone is insufficient novelty; joint improvement is a competing hypothesis |
| [[vlm_safety_neurons_2608_30750]] — [Safety neurons](https://arxiv.org/abs/2608.30750) | Causal comparisons distinguish localized text pathways from more distributed visual signals | Behavioral correlation cannot substitute for causal mechanism evidence |
| [[vlm_safety_overrides_vision_2608_18628]] — [Safety overrides vision](https://arxiv.org/abs/2608.18628v1) | Conservative grounding instructions can cause abstention despite retained visual evidence | Grounding abstention and harmful-request refusal require different labels |
| [[vlm_casa_2604_00310]] — [CASA, version 2](https://arxiv.org/abs/2604.00310v2) | Abstract describes an internal safety decision and cross-modal transfer | Screen full text; isolate safety-prompt effects from method effects |
| [[vlm_image_attachment_interface_2609_26174]] — [Image-attachment interface, version 2](https://arxiv.org/abs/2609.26174v2) | Blank-image attachment can shift refusal on matched inputs, with checkpoint and image-property dependence | Local blank-image result is a replication target; the broad phenomenon is not a novelty claim |
| [[vlm_vscbench_2505_20362]] — [VSCBench](https://arxiv.org/abs/2505.20362) | Paired safe/unsafe cases measure under-refusal and over-refusal | Include safe usefulness; safety/utility costs are prior work |
| [[vlm_siuo_2406_15279]] — [SIUO](https://arxiv.org/abs/2406.15279v2) | Individually safe modalities can combine into unsafe outputs | Cross-modal evaluation alone is not new; interaction setting differs from typography |
| [[vlm_safety_transfer_2410_12662]] — [Cross-Modal Safety Transfer](https://arxiv.org/abs/2410.12662v2) | Text safety can fail to transfer through visual representations | Transfer gaps are established; they do not imply an inverse text/image law |

The literature supports several possible mechanisms, not a presumption of a universal seesaw. CMRM and VLSBench proceedings identities were verified against ACL Anthology and local PDFs. MARS, the neuron study and the grounding-abstention study were inspected in retrieved full text, without figure audit. CASA, the image-attachment study, VSCBench, SIUO and Cross-Modal Safety Transfer are abstract-only here. The arXiv pages list NAACL 2025 for SIUO and ICLR 2025 for Cross-Modal Safety Transfer; venue status for the other recent work is not verified. This targeted search does not justify “first” or “unexplored” claims.

## What the saved v1 pilot says

The table reproduces the saved model-judge REFUSAL counts in `bundle (1)`. Each denominator is 240 outputs, not 240 independent datasets. A uses a related text model; B is VLM text-only; C is typographic image plus a generic prompt; D is the original text plus a blank image.

| VLM family | A: related LLM | B: VLM text | C: typography | D: blank image |
|---|---:|---:|---:|---:|
| Qwen2-VL-2B | 191/240 | 173/240 | 125/240 | 202/240 |
| Qwen2.5-VL-3B | 195/240 | 197/240 | 147/240 | 197/240 |

These are unvalidated judge labels. They are not verified safety rates. For C, 90 of the 125 REFUSAL-labelled 2B outputs and 39 of the 147 REFUSAL-labelled 3B outputs lack the v2 refusal cues in their first 200 characters. That is a reproducible disagreement diagnostic, not a measured false-positive rate. The heuristic can miss genuine refusals and cannot judge harmful compliance. D also has repeated responses: the most common exact response appears 187 times for 2B and 133 times for 3B. This motivates inspection for boilerplate behavior and over-refusal; it does not by itself prove either.

The matched UID order across A–D is useful, but label arrays bind only by position. A count-matched stale cache could silently attach labels to different responses. Both notebooks retain count-only label-cache reuse. Therefore reproducing the stored fractions verifies arithmetic, not semantic validity or provenance.

## What the recovered v2 bundle adds

The v2 ZIP at `/Users/aryamandev/Downloads/bundle.zip` is snapshotted by SHA-256 `8c7b9e183d2332073260c766acfda373038fff835d56ad3fa88e3fa96b29365e` under `.tools/vlm-research/external_runs/`. It reports 304 harmful examples per condition, sampled as 38 per each of the same eight scenarios. Exact UID order matches across A–E and there are no duplicate UIDs. The ZIP contains responses and separate label arrays, but not the item prompts/images, model revisions, prompt hashes, or response-bound annotation IDs.

| Model | A: related LLM | B: VLM text | C: text in image | D: blank image | E: v2 text control |
|---|---:|---:|---:|---:|---:|
| Qwen2-VL-2B | 71.7% | 65.5% | 14.5% | 77.0% | 44.1% |
| Qwen2.5-VL-3B | 76.0% | 74.0% | 43.1% | 76.3% | 65.1% |

The saved B−C differences are 51.0 and 30.9 percentage points. E−C is 29.6 and 22.0 points; B−E is 21.4 and 8.9 points. These are judge-label contrasts. Crucially, v2 E is **not** the phrase-matched control implied by its result label: the notebook builds E from the full original question in a generic “phrase of an activity” prompt, while C uses the TYPO prompt plus image. E−C therefore does not isolate image reading. v3 changes E to the rendered key phrase, making it a better control if its OCR and prompt records are validated.

The item-level B/C refusal correlations are positive (phi .240 and .455; within-scenario centered phi .168 and .326). Scenario rank correlations (.826 and .898) use only eight categories. Neither association tests whether an intervention that changes image safety causes text safety to move oppositely.

V2 includes a steering sweep only for the 2B model, with 120 harmful examples per arm and 24 benign text prompts. At coefficient 0, text/image/benign refusal labels are 58.3%/12.5%/0%; at 0.5 they are 80.0%/76.7%/37.5%; at 1.0 they are 98.3%/98.3%/100%. The random-direction control at 0.5 gives 58.3%/10.0%/0%. This is preliminary evidence that the text-derived refusal direction transfers to image inputs while also increasing refusal on benign prompts. It is not a clean utility measure, has no uncertainty intervals in the archive, and does not support a zero-sum text/image seesaw.

The v2 refusal gate changes a judge label to COMPLIANCE unless one listed cue occurs in the first 200 characters. Any agreement with that cue check is circular by construction. The ZIP contains no human annotations. Its label cache is reused on array length alone, so stale labels can survive changed outputs or rubrics. Treat these as exploratory refusal labels; keep `OTHER` and incomplete responses separate from harmful-compliance outcomes.

## Design issues to resolve

**Judge calibration comes first.** v2 forces a machine REFUSAL label to COMPLIANCE when the opening text lacks a listed cue. This can turn uncertain outputs into confident errors. Retain ambiguity for adjudication; separately annotate refusal, harmful actionable content, comprehension failure and incomplete generation. The existing analysis plan's human-calibration gate is a useful minimum, but overall agreement can hide poor performance on rare classes. Report per-class confusion, modality-specific disagreement, adjudication and uncertainty. Use an independent second rater on a shared subset where feasible. A stronger model is an additional rater, not ground truth.

**Match the actual content.** v2's E text control uses the full question, while the typography image uses a key phrase. E−C therefore mixes content, prompt and modality differences. Use exactly the rendered phrase in a matched text control, keeping the surrounding instruction identical. A full-question control can remain a separate arm. Blank-image D identifies image-presence effects only conditional on the chosen blank, image processor and prompt; it is not a complete visual baseline.

**Comprehension needs its own measurement.** Read-back with fixed image processing can expose OCR failures. However, a separate read-back prompt changes the task and can itself be affected by refusal. Conditioning only on successful read-back can select an easier subset. Report unconditional effects first, read-back-conditioned analyses second, and sensitivity to the prespecified comprehension rule. A prompt + OCR + residual arithmetic decomposition is descriptive unless causal identification assumptions are defended.

**A/B is not a clean visual-module ablation.** Related LLM/VLM checkpoints may differ in architecture, parameter count, pretraining and alignment. Record that contrast as descriptive; causal language about adding vision requires controlled checkpoints or training history beyond the model names.

**Prevent output and cache artifacts.** Freeze model and dataset revisions, code commit, item IDs, prompt hashes, judge/rubric version, image caps and decoding settings. Cache labels against UID + response hash + judge revision + rubric hash + decoding configuration. Record finish reasons and generated-token counts: a short response budget can change apparent harmfulness or refusal. Preserve every original output and annotation.

## Proposed study after the validation gate

Use the current frozen-model measurement study as the first stage, followed by a controlled intervention sweep only if needed to answer the professor's hypothesis. Keep original continual-training sample selection as a later, separately scoped extension.

For the first stage, estimate matched text/image differences with the corrected prompt controls, calibrated judgments, comprehension measurements and matched benign cases. State clearly whether the benchmark covers typography attacks or genuine visual-context harm. Typography-only results do not generalize to all multimodal safety.

For an inference-time seesaw test, freeze the checkpoint and choose the intervention family, layers and strengths on a disjoint development set. Compare baseline, the candidate intervention, norm-matched random-direction controls and a relevant prior method such as MARS or CMRM when technically compatible. Evaluate both text and image harm plus benign usefulness at every setting. Retain paired item identities across settings; never select the best layer on test results. Include another model family before claiming cross-architecture generality, with scope set by available compute rather than assumed hardware.

Use paired effect estimates and intervals. A stratified item bootstrap can preserve condition pairing and the fixed scenario balance; its inference is conditional on those scenarios. If generalizing to unseen scenarios, only eight scenario clusters make cluster-based uncertainty fragile, so report sensitivity rather than treating a cluster bootstrap as automatically reliable. Predeclare primary contrasts and multiplicity handling. Determine additional sample sizes from desired interval precision or power after calibration; a nominal threshold such as 300 alone does not guarantee adequate power.

Distinguish joint improvement, a local trade-off, no detectable effect, and inconclusive measurement. None should be converted into the desired story. To claim text preservation, use an explicit noninferiority/equivalence margin rather than a nonsignificant deterioration test. Further training requires its own checkpoint sequence and evaluation of both modalities after each controlled update.

## v3 intake and decisions

### Code review of the available v3 notebook

The v3 code substantially improves the measurement design: E is built from an OCR-derived image phrase instead of the full question; it adds read-back at the same configured pixel cap, multiple judges, teacher-forced opener scores, scenario-aware uncertainty and separate human audit/key files. It also acknowledges A/B training differences and read-back selection. These are implemented controls, not yet verified experimental outcomes. The pasted Claude transcript says this notebook was built but had not yet run on a GPU; no v3 result bundle was found.

The following limits remain visible in the code and should be checked against the actual completed run:

- **No intervention sweep:** A–E vary input conditions in fixed checkpoints. Item coupling and the decomposition do not directly test whether improving one modality harms the other. v3 can be a useful measurement study without answering the causal seesaw question alone.
- **Cue gating and missingness:** `refuse_arrays` requires opening refusal cues for two judges and maps unavailable/NA verdicts to zero refusal. That estimates a gated observable, not calibrated safety. Preserve raw verdicts and separately report the ungated result, gate disagreements and missing-label denominators. Guard adapters collapse every parsed “not refusal” into COMPLY; they do not establish harmfulness or comprehension.
- **Reference validation:** when Tesseract is unavailable, references have `validated=False` but `ref_ok=True`. The `REF_OK` mask used for `decomposition_ref_validated_only` then accepts those unvalidated references. Rename that subset as usable-reference-only or build a genuinely validated mask before presenting the analysis. A same-family stronger reader is not ground truth. Overrides are processed only when building a fresh reference cache, so the completed run's actual cache matters.
- **Cache identity:** judge caches still reuse solely by flattened label count. Prefix arrays are also loaded by filename without checking the item/prompt/model configuration. Recompute from preserved responses if the relevant identity is uncertain; a restart with the same counts is insufficient provenance.
- **Decomposition language:** `G = P + Cmp + R` is an exact partition of the measured mean difference, but “comprehension” and “residual routing failure” are not identified causal mechanisms. The read-back label is task-dependent; reference error and the prompt transformation can affect both partitions. Use descriptive names until intervention evidence supports the mechanism labels.
- **Benign coverage and calibration:** benign cases run through A/B/D, not typography C and matched E. They therefore do not measure over-refusal under all tested input formats. The blinded human CSV truncates responses at 700 characters, while chat judges inspect up to 1500; adjudication should use complete responses, particularly for refusal-then-compliance cases. Prefix likelihood over a chosen opener set is a judge-free proxy, not a validated safety measure.
- **Reproducibility:** exported metadata names models and the dataset but does not pin their revisions or bind outputs to prompt/rubric hashes. The bundle deliberately excludes full generations, so aggregate exports alone cannot support a complete independent output audit. Retain a controlled local provenance manifest and full outputs for authorized adjudication.

When completed v3 outputs become available, compare their manifest with this checklist before interpreting them. Record which controls existed before the run and which are post hoc. Reuse valid completed work; missing controls may require a focused follow-up rather than discarding the run. No modifications were made to Claude's notebooks or in-progress source plans by this assessment.

| v3 finding | Defensible interpretation |
|---|---|
| Gap disappears after calibrated judging or matched prompts | Evaluation artifacts explain the measured gap on this protocol |
| Gap persists with reliable comprehension and benign controls | Evidence of a modality-conditioned safety gap; mechanism still open |
| Image safety improves, text safety falls under a controlled intervention | Local seesaw evidence, conditional on models, data and intervention |
| Both improve and benign performance is preserved within declared margins | Counterexample to a universal seesaw in the tested setting |
| Harm refusal rises but benign performance deteriorates | Safety/usefulness cost; cannot label it a text/image seesaw from that alone |

Suggested working proposal title: **Testing Text–Image Safety Coupling in Small Vision–Language Models: Separating Intervention Trade-offs from Evaluation Artifacts.**

The contribution should be selected after valid results: a local trade-off characterization, an artifact-controlled measurement finding, or a joint-improvement result. The pipeline currently supports evidence intake and audit preparation. It has not completed human calibration, a council-generated manuscript, or a publication readiness assessment.

## Audit provenance

Consulted originals include `docs/ANALYSIS_PLAN_MODALITY_SAFETY.md`, `docs/MASTER_PLAN_MODALITY_SAFETY_PAPER.md`, `docs/PROJECT_PLAN_CROSS_BENCHMARK_EVALUATION.md`, `reports/VLM safety research gaps.md`, all three modality-tradeoff notebooks, both local v1 bundles and the v2 Downloads archive. Hashes and the v2 snapshot are recorded under `.tools/vlm-research/`. The machine-label-blind audit index contains pointers and response hashes, not completed labels; source filenames reveal model and condition. This review is post-v1/v2 and before any v3 result bundle. It is not retrospectively preregistered.
