# Connected VLM safety research task

`blissful-bose` and `Safety Alignment for VLMs Research` are aliases of the same local research workspace and GitHub repository, `dev4-gpt/blissful-bose`. The original continual-training idea, the professor's seesaw hypothesis, and the current measurement proposal are distinct stages of that project. The connection does not choose a scientific conclusion.

The intake reads the sibling workspace without editing it. It records file hashes, snapshots consulted inputs locally, checks saved response/label structure, and prepares a scenario-balanced audit index that omits the machine labels. File names reveal conditions, so this is judge-label blinding, not full model/condition blinding. Audit indices are not completed human annotations.

Run from the repository root:

```sh
backend/.venv/bin/python scripts/run_vlm_research_pipeline.py --ingest-pdfs
```

`VLM_RESEARCH_PATH` overrides the sibling folder. Preparation requires its origin to match `dev4-gpt/blissful-bose`. Local PDFs are deduplicated by file hash and all pages are extracted into paper notes; bibliography and figures still require verification. Existing matching notes are preserved. PDF ingestion is optional and only exposed by the local command.

- `GET /api/research/projects/vlm-safety`: connection, project focus and latest intake, including changed consulted files.
- `POST /api/research/projects/vlm-safety/prepare`: new structural audit and audit index; optional `sample_per_group` between 1 and 100 (default 30).
- `integrations/research_projects.json`: fixed project inputs and research question.
- `.tools/vlm-research/runs/`: ignored local reports and audit indices.
- `.tools/vlm-research/inputs/`: ignored, hash-addressed input snapshots.
- `.tools/vlm-research/external_runs/`: audited v2 ZIP snapshots indexed in project status.
- `vault/02_Concepts/`: research-task notes and the seesaw proposal assessment.

## End-to-end research phase

Open **Feynman Workbench → Blissful Bose · VLM** for the connected project view. The tab uses the existing VLM status and intake endpoints; it does not write into the sibling project. **Run read-only intake** hashes and snapshots consulted files, checks saved response/label structure, and creates the blinded audit index. It does not run notebook code, judge responses, start a GPU job, or edit a manuscript.

The project moves through these gates:

1. **Connect the canonical project.** Verify that the local workspace exists and its origin is `dev4-gpt/blissful-bose`.
2. **Freeze and inspect evidence.** Save a content-addressed input snapshot; keep smoke, pilot, v2, and later runs distinct. Refresh intake when consulted files change.
3. **Validate safety labels with people.** Independently annotate a stratified sample, compare annotators with each other and candidate judges, and adjudicate disagreement. Do not treat cue matching or model labels as ground truth.
4. **Run the controlled measurement study.** Review v3 provenance and repair phrase-validation/cache issues; finalize matched text controls, comprehension checks, benign utility controls, exclusions, and scenario-aware analysis before unblinding.
5. **Test the intervention-induced seesaw.** In a separate preregistered study, sweep a specified intervention on paired text/image items, with a baseline, control direction, benign utility outcomes, and declared uncertainty/non-inferiority margins. An input-format gap alone does not establish a seesaw.
6. **Decide whether a paper is supported.** Confirm novelty and source metadata, then run the council, adversarial/statistical review, fact-check, and venue gate. Draft only claims supported by validated evidence; negative or inconclusive results remain valid outcomes.

The panel reports completed intake facts and keeps human calibration, new model runs, causal intervention, and publication as explicit gates. Passing one gate never implies that a later one passed. The first deliverable is a validated measurement result; the causal seesaw is a subsequent research phase, not a conclusion assumed by the plan.

For a completed v3 notebook output directory, `scripts/prepare_vlm_annotation.py <OUT_DIR>` can build separate randomized annotator and restricted-key files under ignored `.tools/vlm-research/annotations/`. It restores full responses from local generation files and refuses export unless the complete response SHA-256 and normalized CSV text both match the condition/UID key. Share only the `for_annotators/annotation_packet.csv`; keep `restricted/` private until labels are locked. The builder has passed a synthetic fixture, but it cannot run on study data until the v3 audit files, full generation files, and results manifest exist together in an access-controlled local output directory.

The local `bundle/` and `bundle (1)/` folders are a smoke run and a larger v1 pilot. A separately delivered v2 ZIP has now been imported from Downloads. v3 code is present, but the user-provided Claude transcript says v3 had not yet run on a GPU; no v3 output bundle was found at this intake. The pilot cue diagnostic is explicitly pinned to the v2 cue list so adding v3 code cannot silently change that comparison. New outputs require a fresh explicit intake; no recurring monitoring is configured. Staleness checks cover consulted files, not newly added files.

Audit a separately delivered ZIP without extracting into the research repository:

```sh
backend/.venv/bin/python scripts/audit_vlm_bundle.py /path/to/bundle.zip \
  --notebook ../blissful-bose/notebooks/vlm_modality_tradeoff_v2.ipynb
```

The command validates member paths, records a content hash and local archive copy, checks row/label counts and UID pairing, and writes an audit summary. The API's project status lists imported archive hashes and snapshot paths. ZIP members are parsed in memory; their contents are not executed.

The service never turns a refusal-cue mismatch into a harm label. Its status remains `MEASUREMENT_VALIDATION_REQUIRED`, with human calibration unperformed and manuscript readiness false. It does not launch GPU jobs, execute notebooks, read authenticated Claude sessions, run the council, or publish a manuscript. The current deliverable is a proposal assessment and reproducible evidence intake.
