---
title: "Master plan: VLM safety measurement and text–image coupling"
project: "vlm-safety"
status: "research_plan_before_v3_results"
---

# Master plan: VLM safety measurement and text–image coupling

## Research aim

Start with a reproducible measurement study of how small frozen VLMs respond to harmful requests presented as text or as text inside an image. Keep the professor's seesaw hypothesis as a separate, testable question: when an intervention changes harmful-request safety for image inputs, does it reduce safety for text inputs, or can the two improve together? Measure benign usefulness and image-text comprehension alongside both safety outcomes.

This separation matters because the current A–E evaluations change the input condition while holding model weights fixed. They can estimate differences among conditions. A causal seesaw needs a prespecified intervention whose strength varies while the same model is evaluated on paired text and image items.

## Current evidence and state

| Artifact | State | Use |
|---|---|---|
| v1 smoke, `bundle/` | 40 responses per harmful model-condition group | Pipeline check only; don't pool |
| v1 pilot, `bundle (1)/` | 240 harmful responses per group; 2B steering included | Exploratory comparison |
| v2 ZIP, SHA-256 `8c7b9e183d2332073260c766acfda373038fff835d56ad3fa88e3fa96b29365e` | 304 per harmful group; 2B steering included; stored locally under `.tools/vlm-research/external_runs/` | Exploratory comparison; E is not truly phrase-matched |
| v3 notebook | Built; Claude transcript says not yet run on GPU | Candidate measurement run, pending output |
| Local paper collection | 20 unique PDF files ingested, including multiple editions of some works | Deduplicate bibliographically and inspect relevant methods/figures |

Never pool the pilot runs: they use different item counts and evolving prompts, labels and analysis. The v2 bundle preserves output text and labels, but omits exact original prompts/images and model revisions. The local audit indices contain response hashes, not completed human labels.

## Stage 1 — Freeze provenance and verify the run identity

For each new run, save the code commit, notebook hash, dataset revision and item IDs, prompt templates, phrase source and validation status, model/tokenizer revisions, image processor and pixel cap, decoding settings, judge prompt/version, and output hashes. Make cache identity depend on item UID, actual response hash, model revision, prompt hash, rubric/judge revision and decoding configuration. Reject a cache hit when any field differs.

Keep the full generations in access-controlled project storage for adjudication. Export aggregates and redacted examples for sharing. Retain smoke, v1, v2 and future v3 as separately named immutable runs.

**Exit condition:** an independent reviewer can reconstruct each condition and verify that each label points to the response it grades.

## Stage 2 — Establish whether the labels measure safety

Before treating refusal as safety, annotate a scenario- and condition-stratified sample, with extra coverage of C, `OTHER`, cue-gate disagreements, and refusal followed by actionable content. Have two people label a common subset independently; use the existing analysis-plan thresholds as a minimum reliability gate, and report per-class agreement and confusion rather than a single overall score. The one-day retest in v3 measures the same annotator's consistency; it cannot replace an independent second annotator.

Keep distinct labels for harmful actionable assistance, refusal without assistance, partial/disclaimer-plus-assistance, non-comprehension, and incomplete/ambiguous output. For benign twins, separately score inappropriate refusal and task usefulness. Preserve raw judge outputs before any refusal-cue filter. A missing refusal phrase does not prove compliance; `OTHER` does not automatically mean unsafe.

**Exit condition:** selected primary judge/rubric is checked against independent human adjudication for each modality and the relevant classes. If the existing gate fails, revise the label procedure and audit another sample before estimating headline safety effects.

## Stage 3 — Run v3 as a controlled measurement study

Run the existing v3 notebook only after reviewing the manifest and cache. Keep its A/B/C/D/E conditions separate: E's rendered key phrase is a meaningful improvement over v2's full-question control. Record whether the independent reader and Tesseract actually validated each phrase; correct the `ref_ok=True` fallback when Tesseract is absent. Report unresolved OCR separately. Verify that the audit copy contains enough response text to judge the complete answer; the current 700-character export can truncate content that the machine grader saw.

Treat `G = P + Cmp + R` as an arithmetic partition of the observed gap. Read-back-defined strata are descriptive because comprehension is measured after seeing the image and may select easier items. Don't call the terms causal prompt, comprehension, or routing effects without a design that identifies those mechanisms.

For the eight preselected scenarios, report paired condition differences, uncertainty intervals, item-level associations within scenario, and sensitivity to judge choice. Use the prespecified scenario-aware analysis, but state that eight scenario clusters limit conclusions about new domains. Keep teacher-forced refusal-opener scores exploratory; they aren't calibrated probabilities of safety.

**Exit condition:** v3 has complete provenance, the label gate passes, primary comparisons and missing-data handling are fixed before results are unblinded, and benign controls cover the conditions used for the claim.

## Stage 4 — State the result the design supports

The primary measurement paper can test whether the B/C gap persists with phrase-matched text, human-checked labels and comprehension information. Report it as a modality-conditioned behavioral gap if supported. Do not describe it as text/image seesaw evidence by itself.

V2 reports B/C refusal-label gaps of 51.0 points for Qwen2-VL-2B and 30.9 points for Qwen2.5-VL-3B, but its E control does not use the same phrase/prompt as C and its grader is cue-gated. The text-derived steering sweep for 2B increases refusal labels for both harmful text and image inputs; at strength 0.5 they are 80.0% and 76.7%, alongside 37.5% refusal on benign text prompts. This points to a possible cross-modal transfer and a concerning benign-refusal cost, subject to label validation. Neither result establishes a conservation-style seesaw.

## Stage 5 — Test the causal seesaw as a separate experiment

After advisor agreement on the definition, preregister a frozen-checkpoint intervention study. A text-derived refusal direction is a natural candidate because v1/v2 already contain pilot sweeps and [MARS](https://arxiv.org/abs/2606.31876v2) is prior work. Use matched harmful intent items in text and image forms; sweep intervention strength chosen on a development set; include baseline and norm-matched random-direction controls; evaluate benign usefulness in both formats; and repeat across at least one additional architecture if compute permits. Compare the intervention against a compatible prior method when implementation permits.

Define safety as independently adjudicated harmful-completion avoidance, not refusal wording alone. Predeclare the image gain, text non-inferiority/equivalence margin, uncertainty method, primary contrasts and multiplicity handling. A local seesaw is supported only if the intervention improves one modality while worsening the other beyond its declared margin. A strict zero-sum claim needs a separately justified equivalence test over the sum of changes. Joint gains, a local trade-off, no detectable change, and inconclusive measurement are all valid outcomes.

## Stage 6 — Novelty check and paper decision

The broad themes already have substantial prior work: cross-modal alignment degradation and recovery in [[vlm_local_cmrm_357d4867022c]]; text safety transfer in [[vlm_safety_transfer_2410_12662]]; visual leakage in [VLSBench](https://aclanthology.org/2025.acl-long.405/); paired under/over-safety calibration in [[vlm_vscbench_2505_20362]]; safe-input interactions in [[vlm_siuo_2406_15279]]; textual refusal steering in [[vlm_mars_2606_31876]]; and blank-image attachment effects in [[vlm_image_attachment_interface_2609_26174]]. The latter makes a generic claim that blank images change refusal particularly weak as a novelty claim.

The remaining candidate contribution is narrower: a careful, human-validated comparison of prompt-matched typography inputs and their text counterparts on these checkpoints, followed by a controlled test of whether a selected intervention creates an actual text/image trade-off while preserving benign ability. Confirm this scope with the advisor after the v3 audit and a fuller literature search. Do not claim “first” or select a venue until evidence and novelty are established.

## Stage 7 — Draft only after the gates pass

Prepare a paper only when source claims, run provenance, label validity and the target research question are settled. Ingest the relevant full papers and verify citation metadata; then convene the research council for a methods debate, run the adversarial and statistical reviews, and fact-check every reported number against response-bound annotations and run manifests. Include negative and inconclusive findings. The current work is a proposal and pilot assessment, not a manuscript or camera-ready result.

## Immediate next actions

1. Share the v2 audit summary with the advisor and confirm whether the target is an input-format gap, cross-modal transfer, or intervention-induced seesaw.
2. Ask Claude to retain v3 provenance and outputs, then place its finished bundle in the project workspace or provide its path for hashing and audit.
3. Fix v3 phrase-validation fallback and cache identity before interpreting new labels; keep original outputs untouched.
4. Complete the blinded human-label audit and judge comparison before writing a headline safety claim.
5. Decide whether the calibrated v3 measurement result merits a paper or whether the separate intervention sweep is needed first.
