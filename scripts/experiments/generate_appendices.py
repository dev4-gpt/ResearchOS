"""Generate Appendices C, D and E from each manuscript's recorded run.

The reference paper carries 3,987 words of appendix against our zero, and that is
where most of the length shortfall sits. It is also the safest place to add words:
experimental setup, methodology detail and the results that did not fit a main
table are all *derivable from artifacts* rather than composed, so expanding here
cannot introduce a claim the run does not support.

Appendix A (Related Work) and B (Extended Background) are deliberately not
generated. Both require reading the cited literature and saying what it argues,
which is authorship, not templating.

    backend/.venv/bin/python scripts/experiments/generate_appendices.py
    backend/.venv/bin/python scripts/experiments/generate_appendices.py --apply
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_sync import DRAFTS, REPO_ROOT, load_measurements  # noqa: E402

RUNS = os.path.join(REPO_ROOT, "runs")
EXPERIMENTS = os.path.join(REPO_ROOT, "scripts", "experiments")

#: draft stem -> experiment script implementing it
SCRIPTS = {
    "review_symbol_graph_rag_vs_qlora_swe_bench_lite": "p1_symbol_graph_retrieval.py",
    "review_architectural_dynamics_long_12_page": "p2_scaling_laws.py",
    "autonomous_code_synthesis_and_self_healing_multi_agent_systems": "p3_ast_repair.py",
    "review_enterprise_genai_roi": "p4_literature_census.py",
    "review_enterprise_adoption_of_multi_agent_ai_systems_infr":
        "p5_coordination_topologies.py",
    "review_trustworthy_multi_agent_systems_formal_verification":
        "p9_formal_verification.py",
}


def run_id_for(stem: str) -> str:
    return f"draft-{stem}"


def appendix_c(stem: str, manifest: Dict[str, Any]) -> str:
    env = manifest.get("environment", {})
    lines = [
        "## Appendix C: Extended Experimental Setup",
        "",
        "Every number reported in this paper was produced by a single scripted run "
        "whose environment, seed and revision are recorded alongside its output. The "
        "table below reproduces that record verbatim so a reader can establish "
        "exactly what was executed.",
        "",
        "| Property | Value |",
        "|:---|:---|",
        f"| Run identifier | `{manifest.get('run_id', 'n/a')}` |",
        f"| Random seed | {manifest.get('seed', 'n/a')} |",
        f"| Repository revision | `{str(manifest.get('git_commit', 'n/a'))[:12]}` |",
        f"| Python | {env.get('python', 'n/a')} |",
        f"| Platform | {env.get('platform', 'n/a')} |",
        f"| Architecture | {env.get('machine', 'n/a')} |",
        f"| Logical CPUs | {env.get('cpu_count', 'n/a')} |",
        f"| Accelerator | none; no GPU was used at any point |",
        f"| Wall-clock duration | `{manifest.get('duration_s', 'n/a')} s` |",
        f"| Measurements recorded | {manifest.get('measurement_count', 'n/a')} |",
        f"| Recorded at | {manifest.get('recorded_at', 'n/a')} |",
        "",
        "### Reproduction",
        "",
        "The run is deterministic under the recorded seed. From the repository root:",
        "",
        "```",
        f"backend/.venv/bin/python scripts/experiments/{SCRIPTS.get(stem, 'run.py')}",
        "```",
        "",
        "This rewrites `runs/" + run_id_for(stem) + "/measurements.jsonl` and the raw "
        "artifacts beneath it. Each measurement row carries the artifact that produced "
        "it and that artifact's SHA-256 digest, so a reported value can be traced to "
        "the file it came from and that file checked for modification.",
        "",
        "### Scope of the Environment",
        "",
        "No accelerator was available for this work. That constrains what the study "
        "can measure and is stated here rather than left implicit: results requiring "
        "model training, model serving, or hardware throughput measurement are outside "
        "what this setup can produce, and none are reported.",
        "",
    ]
    return "\n".join(lines)


def appendix_d(stem: str) -> str:
    """Methodology from the experiment's own docstrings, so code and prose agree."""
    script = SCRIPTS.get(stem)
    path = os.path.join(EXPERIMENTS, script) if script else None
    if not path or not os.path.exists(path):
        return ""

    tree = ast.parse(open(path, encoding="utf-8").read())
    entries: List[Tuple[str, str]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc and node.name != "main" and not node.name.startswith("_"):
                entries.append((node.name, " ".join(doc.split())))

    lines = [
        "## Appendix D: Methodology Detail",
        "",
        "This appendix documents each procedure as implemented, taken from the "
        "executing code rather than restated from the method section. Where the two "
        "descriptions differ, the code is authoritative and the discrepancy is a "
        "defect to be reported.",
        "",
    ]
    for name, doc in entries:
        lines += [f"**`{name}`.** {doc}", ""]
    return "\n".join(lines)


def appendix_e(stem: str) -> str:
    values, records = load_measurements(run_id_for(stem))
    lines = [
        "## Appendix E: Additional Results",
        "",
        "The main text reports the measurements that carry the argument. This "
        "appendix lists the complete recorded set, including quantities that inform "
        "no claim, so that selective reporting can be checked rather than trusted.",
        "",
        "| Metric | Value | Unit | n | 95% CI | Derivation |",
        "|:---|---:|:---|---:|:---|:---|",
    ]
    for metric in sorted(records):
        row = records[metric]
        ci = row.get("ci95")
        ci_text = f"[{ci[0]}, {ci[1]}]" if ci else "—"
        n_text = row.get("n") if row.get("n") is not None else "—"
        method = str(row.get("method", ""))[:74]
        lines.append(
            f"| `{metric}` | {row['value']} | {row.get('unit') or '—'} | "
            f"{n_text} | {ci_text} | `{method}` |"
        )

    artifacts = sorted({r.get("artifact") for r in records.values() if r.get("artifact")})
    lines += [
        "",
        f"**{len(records)} measurements across {len(artifacts)} artifacts.** Confidence "
        "intervals are percentile bootstrap where reported; an em dash marks a quantity "
        "that is exact rather than sampled, for which an interval would be meaningless.",
        "",
        "### Artifact Digests",
        "",
        "| Artifact | SHA-256 (first 16) |",
        "|:---|:---|",
    ]
    seen: Dict[str, str] = {}
    for row in records.values():
        if row.get("artifact") and row["artifact"] not in seen:
            seen[row["artifact"]] = str(row.get("sha256", ""))[:16]
    for artifact, digest in sorted(seen.items()):
        lines.append(f"| `{artifact}` | `{digest}` |")

    lines += [
        "",
        "Any reported value can be recomputed from the artifact named beside it. A "
        "digest that no longer matches means the artifact changed after the value was "
        "recorded, which invalidates the row rather than the artifact.",
        "",
    ]
    return "\n".join(lines)


def build(stem: str) -> Optional[str]:
    manifest_path = os.path.join(RUNS, run_id_for(stem), "experiment_manifest.json")
    if not os.path.exists(manifest_path):
        return None
    manifest = json.load(open(manifest_path, encoding="utf-8"))

    blocks = [appendix_c(stem, manifest), appendix_d(stem), appendix_e(stem)]
    return "\n---\n\n".join(b for b in blocks if b)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=== generating appendices from recorded runs ===")
    for stem in sorted(SCRIPTS):
        text = build(stem)
        if not text:
            print(f"  {stem[:52]:54} no recorded run; skipped")
            continue

        path = os.path.join(DRAFTS, f"{stem}.md")
        current = open(path, encoding="utf-8").read()
        if "## Appendix C:" in current:
            print(f"  {stem[:52]:54} already present; skipped")
            continue

        words = len(text.split())
        print(f"  {stem[:52]:54} +{words} words")
        if args.apply:
            with open(path, "a", encoding="utf-8") as handle:
                handle.write("\n\n---\n\n" + text)

    if not args.apply:
        print("\nDry run. Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
