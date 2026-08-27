"""p10: measure what the provenance gate misses, instead of waiting to find out.

The gate decides whether a manuscript may be submitted. Every hole in it so far
was found by a person reading carefully at the right moment -- 726 unbacked
claims, a citation to a paper on research ethics committees standing in for a
hardware specification, an audit scoring 100.0 on a stub. That is not a strategy.

This runs an adversary against the gate itself. Take the nine manuscripts, whose
claims all currently resolve; apply transformations that should each break one
claim; and count how often the gate notices. The output is a detection rate per
operator, which is a description of the gate's coverage and is recorded like any
other measurement, with an artifact and a digest, so it is subject to the gate in
turn.

Nothing is generated and no model is consulted. Every mutation is a deterministic
edit under a fixed seed, and every verdict is ClaimProvenanceService's own
classification. Mutants exist only in memory -- no draft is written.

Two results are expected to be bad, and are the point of running it:
mu_rebind and mu_attribute attack the two behaviours already known to be
unchecked -- that a claim binds to a value and a unit without regard to what the
sentence says it measures, and that an attribution verb beside a resolvable key
is accepted without asking whether the source supports the figure.

    backend/.venv/bin/python scripts/experiments/p10_adversarial_provenance.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

# Import order matters: backend/ contains a package also called `harness`, so it
# must not be on the path until the experiment harness has been resolved from
# this directory. Putting backend first makes `import harness` find the wrong
# module, which fails loudly here and would fail silently in something subtler.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import REPO_ROOT, ExperimentRecorder  # noqa: E402

sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))
from services.claim_mutations import (  # noqa: E402
    MUST_CATCH, OPERATORS, generate,
)
from services.claim_provenance import ClaimProvenanceService  # noqa: E402

SEED = 20260825
DRAFTS = os.path.join(REPO_ROOT, "vault", "04_Drafts")

#: Plausible-sounding metric descriptions for mu_rebind. Drawn from this corpus's
#: own vocabulary so the rewritten sentence reads like something the paper might
#: have said -- an implausible one would be an unfairly easy target.
METRIC_VOCAB = (
    "Byzantine agreement rate", "syntactic validity of generated mutants",
    "share of queries left unchanged by diffusion", "pre-filter rejection rate",
    "safety-invariant hold rate", "single-file patch rate",
)


def load(service: ClaimProvenanceService, stem: str):
    path = os.path.join(DRAFTS, f"{stem}.md")
    text = open(path, encoding="utf-8").read()
    measurements = service.load_measurements(f"draft-{stem}")
    claims = service.extract_claims(text)
    service.classify(claims, measurements)
    return text, claims, measurements


def detected(service: ClaimProvenanceService, mutant, baseline_ungrounded: int) -> bool:
    """True when the gate refuses something about the mutant that it accepted before."""
    claims = service.extract_claims(mutant.text)
    service.classify(claims, mutant.measurements)
    return sum(1 for c in claims if c.grounding == "UNGROUNDED") > baseline_ungrounded


#: The floor CI enforces. Set from a measured run, not chosen: it exists so a
#: change that weakens the gate fails the build, and it may only move upward.
BASELINE_PATH = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
    "vault", "00_System", "gate_detection_baseline.json")

#: How far a rate may drift before it counts as a regression, in percentage
#: points. The denominator is the number of mutants an operator could build from
#: the current manuscripts, so editing a paragraph changes it: adding a section
#: to p1 moved mu_transplant from 60.00% to 59.52% and the floor called that the
#: gate getting weaker. It was not. A tolerance keeps the check sensitive to a
#: real loss of coverage while ignoring the corpus breathing underneath it --
#: and the must-catch operators are exempt, because there a single escape means
#: the instrument is broken and no tolerance applies.
RATE_TOLERANCE_PP = 5.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="exit non-zero if detection fell below the recorded "
                             "baseline, or if a must-catch operator escaped. For CI.")
    parser.add_argument("--set-baseline", action="store_true",
                        help="record the current rates as the floor to defend")
    args = parser.parse_args()

    print("=== p10: adversarial provenance ===\n")
    service = ClaimProvenanceService(
        vault_path=os.path.join(REPO_ROOT, "vault"),
        runs_root=os.path.join(REPO_ROOT, "runs"),
    )

    stems = sorted(f[:-3] for f in os.listdir(DRAFTS) if f.endswith(".md"))
    corpus: Dict[str, Any] = {}
    all_claims: List[Any] = []
    citation_keys: set = set()

    for stem in stems:
        text, claims, measurements = load(service, stem)
        if not measurements:
            continue
        grounded = [c for c in claims if c.grounding == "EXPERIMENT"]
        if not grounded:
            continue
        corpus[stem] = {
            "text": text, "claims": claims, "measurements": measurements,
            "baseline_ungrounded": sum(1 for c in claims
                                       if c.grounding == "UNGROUNDED"),
        }
        all_claims.extend(grounded)
        for claim in claims:
            citation_keys.update(claim.cite_keys)

    print(f"  {len(corpus)} manuscript(s), {len(all_claims)} grounded claim(s), "
          f"{len(citation_keys)} resolvable citation key(s)")
    if not corpus:
        print("  nothing to attack.")
        return 1

    rec = ExperimentRecorder(
        run_id="draft-adversarial-provenance",
        paper="adversarial_provenance",
        description=("Mutation testing of the claim-provenance gate: deterministic "
                     "edits that should break a grounded claim, scored by whether "
                     "the gate refuses them."),
        seed=SEED,
    )

    results: Dict[str, Dict[str, int]] = {}
    escapes: List[dict] = []

    print(f"\n  {'operator':16}{'mutants':>9}{'detected':>10}{'escaped':>9}{'rate':>9}")
    for operator in OPERATORS:
        made = caught = 0
        for index, (stem, entry) in enumerate(sorted(corpus.items())):
            foreign = [c for c in all_claims if c not in entry["claims"]]
            mutants = generate(
                operator, entry["text"], entry["claims"], entry["measurements"],
                seed=SEED + index, attempts=10,
                metric_vocab=list(METRIC_VOCAB),
                foreign_claims=foreign,
                citation_keys=citation_keys,
            )
            for mutant in mutants:
                mutant.draft = stem
                made += 1
                if detected(service, mutant, entry["baseline_ungrounded"]):
                    caught += 1
                else:
                    escapes.append({
                        "operator": operator, "draft": stem,
                        "target": mutant.target, "edit": mutant.description,
                    })

        results[operator] = {"mutants": made, "detected": caught,
                             "escaped": made - caught}
        if not made:
            # An operator that produced nothing has not been measured. Printing
            # 0.00% would read as "the gate caught none of them", which is the
            # opposite of what happened.
            print(f"  {operator:16}{'--':>9}{'--':>10}{'--':>9}{'not exercised':>15}")
            continue
        rate = caught / made * 100.0
        flag = ""
        if operator in MUST_CATCH and caught < made:
            flag = "   <- should have been caught"
        print(f"  {operator:16}{made:>9}{caught:>10}{made - caught:>9}"
              f"{rate:>8.2f}%{flag}")

    total_made = sum(r["mutants"] for r in results.values())
    total_caught = sum(r["detected"] for r in results.values())
    if not total_made:
        print("\n  no mutants generated; not recording a measurement.")
        return 1
    overall = total_caught / total_made * 100.0

    art, sha = rec.save_artifact("adversarial_provenance.json", {
        "seed": SEED,
        "manuscripts": sorted(corpus),
        "grounded_claims": len(all_claims),
        "per_operator": results,
        "escapes": escapes,
    })

    for operator, counts in results.items():
        if not counts["mutants"]:
            continue
        rec.record(f"gate_detection_{operator}",
                   round(counts["detected"] / counts["mutants"] * 100.0, 2), "%",
                   art, sha,
                   f"share of {operator} mutants the provenance gate refused",
                   n=counts["mutants"])

    rec.record("gate_detection_rate", round(overall, 2), "%", art, sha,
               "share of all mutants the provenance gate refused", n=total_made)
    rec.record("gate_mutants_generated", total_made, "n", art, sha,
               "deliberately broken manuscripts built for this run")
    rec.record("gate_escapes", total_made - total_caught, "n", art, sha,
               "mutants the gate accepted as grounded", n=total_made)

    print(f"\n  overall detection rate: {overall:.2f}% of {total_made} mutants "
          f"over {len(all_claims)} grounded claims")
    print(f"  escape set written to artifacts/adversarial_provenance.json")

    unsound = [op for op in MUST_CATCH
               if results[op]["mutants"] and results[op]["escaped"]]
    if unsound:
        print(f"\n  WARNING: {', '.join(unsound)} should be caught in full. An escape "
              f"there is a defect in the gate or in this harness, not a coverage "
              f"finding -- investigate before trusting the rest of the table.")

    rec.finalize()

    # --- the floor -------------------------------------------------------
    current = {op: (c["detected"] / c["mutants"] * 100.0)
               for op, c in results.items() if c["mutants"]}
    if args.set_baseline:
        os.makedirs(os.path.dirname(BASELINE_PATH), exist_ok=True)
        json.dump({"overall": round(overall, 2),
                   "per_operator": {k: round(v, 2) for k, v in current.items()}},
                  open(BASELINE_PATH, "w", encoding="utf-8"), indent=2, sort_keys=True)
        print(f"\n  baseline written to {os.path.relpath(BASELINE_PATH, REPO_ROOT)}")

    if args.check:
        regressions: List[str] = []
        for operator in MUST_CATCH:
            counts = results.get(operator, {})
            if counts.get("mutants") and counts["escaped"]:
                regressions.append(
                    f"{operator} let {counts['escaped']} mutant(s) through; it must "
                    f"catch all of them")
        if os.path.exists(BASELINE_PATH):
            baseline = json.load(open(BASELINE_PATH, encoding="utf-8"))
            for operator, floor in baseline.get("per_operator", {}).items():
                now = current.get(operator)
                if now is not None and now < floor - RATE_TOLERANCE_PP:
                    regressions.append(
                        f"{operator} detection fell from {floor:.2f}% to {now:.2f}% "
                        f"(tolerance {RATE_TOLERANCE_PP:.0f}pp)")
            if overall < baseline.get("overall", 0.0) - RATE_TOLERANCE_PP:
                regressions.append(
                    f"overall detection fell from {baseline['overall']:.2f}% "
                    f"to {overall:.2f}% (tolerance {RATE_TOLERANCE_PP:.0f}pp)")
        else:
            print("\n  no baseline recorded; run with --set-baseline first.")

        if regressions:
            print("\n  CHECK FAILED. The gate got weaker:")
            for line in regressions:
                print(f"    - {line}")
            return 1
        print("\n  CHECK PASSED. Detection has not regressed.")

    print("\n  NOTE: this rate describes THIS gate against THIS corpus. It is not a")
    print("  claim about provenance checking in general, and it must not be raised")
    print("  by adding operators the gate happens to catch -- which is why the")
    print("  per-operator breakdown is reported and not just the total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
