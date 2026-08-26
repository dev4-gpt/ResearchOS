"""Project recorded measurements back into the drafts, repeatably (ERR-072).

Every other generator in this directory is one-shot: ``ManuscriptEditor`` replaces
a span between two anchors and the replacement destroys the anchors, so a second
run reports "already rewritten, skipping" and does nothing. That was tolerable
while the job was a one-time migration off fabricated numbers. It stopped being
tolerable the moment an experiment was re-run: p1 and p3 were re-measured against
a cleaned corpus (ERR-071) and there was no supported way to bring the drafts back
into agreement with ``measurements.jsonl``.

The anchor here is not text in the manuscript. It is a sidecar under
``vault/04_Drafts/.sync/<stem>.json`` recording, for every metric, the exact
literal this pass last wrote and where. Re-syncing means: find the literal the
sidecar says is there, replace it with the literal the current measurement
renders to, and record the new one. The anchor therefore survives rewriting,
because rewriting is what updates it.

Two things this deliberately does not do:

* It does not touch prose that is not a number. If a value moves far enough that
  the surrounding sentence stops being true -- "improves" becoming "does not
  improve" -- no substitution can fix that, and the pass reports the sentence for
  an author to read rather than editing around it.
* It does not guess. An occurrence that two metrics could both claim, or a
  literal the sidecar cannot find, is refused and listed. A wrong number written
  confidently into a manuscript is the failure this whole pipeline exists to
  prevent; refusing is always the cheaper error.

Seeding, the first time, needs to know what the draft *used* to say, because the
draft is already stale by the time you need this. ``--seed-from <git-ref>`` reads
the measurements at that ref and matches their renderings against the draft.

    # what would change, and what cannot be resolved automatically
    backend/.venv/bin/python scripts/experiments/resync_manuscripts.py --seed-from HEAD~1

    # write it
    backend/.venv/bin/python scripts/experiments/resync_manuscripts.py --seed-from HEAD~1 --apply

    # later runs, once the sidecar exists
    backend/.venv/bin/python scripts/experiments/resync_manuscripts.py --apply

    # after reconciling a draft by hand, to capture spellings the seed missed
    backend/.venv/bin/python scripts/experiments/resync_manuscripts.py --reseed --apply

Always finish with ``scripts/run_submission_gate.py``. This pass and the gate check
different things: this one keeps the draft equal to the run, the gate checks that
every number in the draft resolves to a hashed artifact. A value this pass declines
to touch is exactly a value the gate should then refuse.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from typing import Dict, List, Optional, Tuple

# Deliberately not imported from scripts/experiments/harness.py: 'harness' is also
# a package under backend/, and which one wins depends on how the interpreter was
# started. The experiment scripts import it as __main__ from this directory and are
# fine; the test suite runs from the repository root and is not. This module needs
# one path constant, so it computes it rather than betting on import order.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DRAFTS = os.path.join(REPO_ROOT, "vault", "04_Drafts")
SIDECAR_DIR = os.path.join(DRAFTS, ".sync")
RUNS = os.path.join(REPO_ROOT, "runs")

# A rendering may be escaped for LaTeX ("46.34\%") or plain ("46.34%"), and the
# same value appears at different precisions in different sentences. Rather than
# guess which spelling a passage uses, we look for all of them and keep whichever
# the draft actually contains, so the replacement matches the local convention.
MAX_DECIMALS = 6


# ------------------------------------------------------------------ rendering

def render(value: float, decimals: int) -> str:
    """Render *value* at fixed precision, the way the manuscripts spell numbers."""
    if decimals == 0:
        return str(int(round(value)))
    return f"{value:.{decimals}f}"


def candidate_literals(value: float) -> List[Tuple[str, int]]:
    """Every (literal, decimals) spelling of *value* worth looking for.

    Ordered longest-first so that matching prefers the most specific spelling:
    '0.8739' must win over '0.87', or a substitution would leave '39' behind.

    A coarse rounding is only offered when it is either exact or long enough to
    identify itself. Rounding 9.86 to '10' is arithmetically defensible and
    editorially catastrophic: '10' appears in these manuscripts as a year, a
    section number and a count of things unrelated to the metric, and rewriting
    all of them to '13' because a guard rate moved is precisely the silent
    corruption this pass exists to avoid. Three digits, or exactness, is the
    price of being substituted.
    """
    seen: Dict[str, int] = {}
    for decimals in range(MAX_DECIMALS, -1, -1):
        lit = render(value, decimals)
        if abs(float(lit) - value) > 0.5 * 10 ** (-decimals):
            continue  # not a faithful rounding at this precision
        exact = float(lit) == value
        if not exact and sum(ch.isdigit() for ch in lit) < 3:
            continue
        seen.setdefault(lit, decimals)
        # The drafts write thousands as '36{,}032' so LaTeX sets the comma
        # correctly in maths mode. Without this spelling the AST-node count in
        # p3's abstract could not be matched at all, and stayed three re-runs
        # out of date while the appendix table beside it was current.
        grouped = grouped_spelling(lit)
        if grouped != lit:
            seen.setdefault(grouped, decimals)
    return sorted(seen.items(), key=lambda kv: (-len(kv[0]), kv[0]))


def grouped_spelling(literal: str) -> str:
    """'36032' -> '36{,}032'; anything under a thousand is returned unchanged."""
    sign = "-" if literal.startswith("-") else ""
    body = literal[1:] if sign else literal
    whole, dot, frac = body.partition(".")
    if len(whole) < 4:
        return literal
    return sign + f"{int(whole):,}".replace(",", "{,}") + dot + frac


# ---------------------------------------------------------------- data access

def load_measurements(run_id: str, text: Optional[str] = None) -> Dict[str, dict]:
    """Return {metric: record}. *text* overrides the on-disk file when replaying a ref."""
    if text is None:
        path = os.path.join(RUNS, run_id, "measurements.jsonl")
        if not os.path.exists(path):
            return {}
        text = open(path, encoding="utf-8").read()
    out: Dict[str, dict] = {}
    for line in text.splitlines():
        line = line.strip()
        if line:
            row = json.loads(line)
            out[row["metric"]] = row
    return out


def manifest_rows(run_id: str, text: Optional[str] = None) -> Dict[str, dict]:
    """Run metadata, shaped like measurements so the same machinery projects it.

    Eight drafts carry a "Reproducibility" table stating the wall-clock duration,
    the commit, the timestamp and the measurement count of the run that produced
    them. Those live in experiment_manifest.json, not measurements.jsonl, so this
    pass could not see them and nothing else re-synced them either -- p3's table
    claimed 10.293 s and revision 90967292066d several runs after both stopped
    being true. The provenance gate does not catch it because the gate only
    resolves claims against measurements; the stricter fact checker does, which is
    how it was found.

    Only numeric fields are returned. The commit hash and the timestamp are text,
    and substituting text by literal match is a different and more dangerous
    operation than substituting a number -- those stay a reported gap.
    """
    if text is None:
        path = os.path.join(RUNS, run_id, "experiment_manifest.json")
        if not os.path.exists(path):
            return {}
        text = open(path, encoding="utf-8").read()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    out: Dict[str, dict] = {}
    for field in ("duration_s", "measurement_count", "seed"):
        value = data.get(field)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            out[f"manifest_{field}"] = {"metric": f"manifest_{field}", "value": value}
    return out


def measurements_at_ref(run_id: str, ref: str) -> Dict[str, dict]:
    """Read one run's measurements as of *ref*, for seeding against a stale draft."""
    rel = os.path.relpath(os.path.join(RUNS, run_id, "measurements.jsonl"), REPO_ROOT)
    proc = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=REPO_ROOT,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return {}
    return load_measurements(run_id, proc.stdout)


def draft_path(stem: str) -> str:
    return os.path.join(DRAFTS, f"{stem}.md")


def sidecar_path(stem: str) -> str:
    return os.path.join(SIDECAR_DIR, f"{stem}.json")


def run_ids() -> Dict[str, str]:
    """{draft stem: run_id} for every run that has a matching draft."""
    out: Dict[str, str] = {}
    if not os.path.isdir(RUNS):
        return out
    for run_id in sorted(os.listdir(RUNS)):
        stem = run_id[len("draft-"):] if run_id.startswith("draft-") else run_id
        if os.path.exists(draft_path(stem)):
            out[stem] = run_id
    return out


# -------------------------------------------------------------------- seeding

def protected_spans(text: str) -> List[Tuple[int, int]]:
    """Ranges no measurement may ever be substituted into.

    Quoted source material is the dangerous one. The related-work sections embed
    abstracts verbatim as ``**Title** [[key]] reports: ...``, and one of them is
    GPT-3's, which contains the number 175. p3 records 175 mutants for one
    operator; without this guard a re-sync would have rewritten a cited paper's
    "175-billion parameter" to "172-billion" -- inventing a fact inside a
    quotation, attributed to someone else, in a manuscript. Citation keys carry
    digits too, and a fenced block is someone's literal output.
    """
    spans: List[Tuple[int, int]] = []

    # YAML frontmatter holds pipeline metadata -- publisher_value_score, and the
    # checkmate_score of 100.0 that this project already knows is a false green.
    # Neither is a measurement, and both collide with real percentages.
    if text.startswith("---\n"):
        close = text.find("\n---", 4)
        spans.append((0, close + 4 if close > 0 else len(text)))

    fence = re.compile(r"^```", re.M)
    marks = [m.start() for m in fence.finditer(text)]
    for open_at, close_at in zip(marks[::2], marks[1::2]):
        spans.append((open_at, text.index("\n", close_at) if "\n" in text[close_at:] else len(text)))

    for match in re.finditer(r"\[\[[^\]]*\]\]", text):
        spans.append(match.span())

    for line_match in re.finditer(r"^.*$", text, re.M):
        line = line_match.group()
        if line.startswith(">"):
            spans.append(line_match.span())
            continue
        quote = re.search(r"\]\]\s*reports:", line)
        if quote:
            spans.append((line_match.start() + quote.end(), line_match.end()))
    return spans


def locate(text: str, literal: str) -> List[int]:
    """Offsets of *literal* in *text*, excluding matches that are not the quantity.

    '103' occurs inside '1039' and inside '0.1034'; neither is the number we
    recorded, and substituting into one corrupts an unrelated value. Quoted
    source text is excluded outright -- see :func:`protected_spans`.
    """
    guarded = protected_spans(text)
    hits: List[int] = []
    start = 0
    while True:
        idx = text.find(literal, start)
        if idx < 0:
            return hits
        start = idx + 1
        end = idx + len(literal)
        before = text[idx - 1] if idx else ""
        after = text[end:end + 1]
        if before.isdigit() or before == "." or after.isdigit() or after == ".":
            continue
        if any(a <= idx < b for a, b in guarded):
            continue
        hits.append(idx)


def seed(old: Dict[str, dict], text: str) -> List[dict]:
    """Match old measurement renderings against the draft.

    One anchor per distinct literal, listing every (metric, field) that renders to
    it. Sharing is normal and mostly harmless: twelve retrieval metrics share the
    sample size 103, and they will go on sharing it. Whether a shared literal is
    actually ambiguous cannot be decided here -- it depends on whether the
    claimants still agree once the measurements move -- so that judgement is left
    to :func:`resync`, which has the new values in hand.
    """
    claims: Dict[Tuple[int, int], List[Tuple[str, str, int]]] = {}
    for metric, record in sorted(old.items()):
        for field in ("value", "n"):
            raw = record.get(field)
            if raw is None or isinstance(raw, bool):
                continue
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            for literal, decimals in candidate_literals(value):
                if len(literal) < 2:
                    continue  # a bare digit matches everything and means nothing
                for off in locate(text, literal):
                    span = (off, off + len(literal))
                    if any(a < span[1] and span[0] < b and (a, b) != span for a, b in claims):
                        continue  # overlaps a longer, more specific match already taken
                    claims.setdefault(span, []).append((metric, field, decimals))

    merged: Dict[str, dict] = {}
    for (start, end), owners in sorted(claims.items()):
        literal = text[start:end]
        anchor = merged.setdefault(literal, {"literal": literal, "claims": [], "lines": []})
        anchor["lines"].append(text.count("\n", 0, start) + 1)
        for metric, field, decimals in owners:
            entry = {"metric": metric, "field": field, "decimals": decimals}
            if entry not in anchor["claims"]:
                anchor["claims"].append(entry)
    return [merged[k] for k in sorted(merged, key=lambda s: (-len(s), s))]


# ------------------------------------------------------------------ rewriting

def resync(stem: str, anchors: List[dict],
           new: Dict[str, dict]) -> Tuple[str, List[dict], List[dict]]:
    """Apply every anchor whose measurement moved.

    Returns (text, changes, blocked). An anchor is blocked when its claimants no
    longer agree -- p@5 for both systems was 94.17 and is now 97.58 and 98.39, so
    the single spelling the draft uses has to become two, and only an author can
    say which sentence gets which.
    """
    text = open(draft_path(stem), encoding="utf-8").read()
    changes: List[dict] = []
    blocked: List[dict] = []

    # Longest literals first: rewriting '0.87' before '0.8739' would corrupt it.
    for anchor in sorted(anchors, key=lambda a: -len(a["literal"])):
        old_literal = anchor["literal"]
        wanted: Dict[str, List[str]] = {}
        missing: List[str] = []
        for claim in anchor["claims"]:
            record = new.get(claim["metric"])
            raw = None if record is None else record.get(claim["field"])
            if raw is None:
                missing.append(f"{claim['metric']}.{claim['field']}")
                continue
            # Replace in the spelling the passage already uses: a value written
            # '36{,}032' must come back grouped, or the substitution silently
            # changes how LaTeX typesets it.
            spelled = render(float(raw), claim["decimals"])
            if "{,}" in old_literal:
                spelled = grouped_spelling(spelled)
            wanted.setdefault(spelled, []).append(claim["metric"])

        if len(wanted) > 1:
            blocked.append({"literal": old_literal, "lines": anchor["lines"],
                            "reason": "claimants disagree",
                            "detail": "; ".join(f"{v} <- {', '.join(sorted(m))}"
                                                for v, m in sorted(wanted.items()))})
            continue
        if not wanted:
            blocked.append({"literal": old_literal, "lines": anchor["lines"],
                            "reason": "no longer recorded",
                            "detail": ", ".join(missing)})
            continue

        new_literal = next(iter(wanted))
        if new_literal == old_literal:
            continue
        if missing:
            # Some claimants vanished and the survivors agree. Take the survivors,
            # but say which ones went, because a metric disappearing from a run is
            # itself worth noticing.
            blocked.append({"literal": old_literal, "lines": anchor["lines"],
                            "reason": "partially recorded, applied from survivors",
                            "detail": ", ".join(missing)})

        hits = locate(text, old_literal)
        if not hits:
            blocked.append({"literal": old_literal, "lines": anchor["lines"],
                            "reason": "literal not present; draft edited by hand",
                            "detail": ""})
            continue
        for off in reversed(hits):
            text = text[:off] + new_literal + text[off + len(old_literal):]
        changes.append({"metric": ", ".join(sorted({c["metric"] for c in anchor["claims"]})),
                        "lines": anchor["lines"], "was": old_literal,
                        "now": new_literal, "occurrences": len(hits)})
        anchor["literal"] = new_literal
    return text, changes, blocked


REPRODUCIBILITY_ROWS = {
    "Run identifier": lambda m: m.get("run_id"),
    "Random seed": lambda m: m.get("seed"),
    "Repository revision": lambda m: (m.get("git_commit") or "")[:12] or None,
    "Wall-clock duration": lambda m: (f"{m['duration_s']:.3f} s"
                                      if isinstance(m.get("duration_s"), (int, float)) else None),
    "Measurements recorded": lambda m: m.get("measurement_count"),
    "Recorded at": lambda m: m.get("recorded_at"),
}


def sync_reproducibility_table(run_id: str, text: str) -> Tuple[str, List[dict]]:
    """Rewrite the Reproducibility table's rows from the run manifest.

    These rows are anchored on their label -- '| Wall-clock duration | ... |' --
    rather than on the value they currently hold. That is the right anchor here
    and the wrong one everywhere else: a label makes the row unambiguous, which
    is what lets this safely rewrite the commit hash and the timestamp as well as
    the numbers. Literal matching could not do that, and literal matching is also
    why these rows went stale in the first place -- the values live in
    experiment_manifest.json, so the measurement-driven pass never saw them.

    p3's table claimed a wall-clock of 10.293 s and revision 90967292066d, both
    several runs out of date, while the provenance gate reported the manuscript
    fully grounded. The gate resolves claims against measurements and this is not
    a measurement; it is a statement about the run, and it was simply never
    checked by anything.
    """
    path = os.path.join(RUNS, run_id, "experiment_manifest.json")
    if not os.path.exists(path):
        return text, []
    try:
        manifest = json.load(open(path, encoding="utf-8"))
    except json.JSONDecodeError:
        return text, []

    changes: List[dict] = []
    lines = text.splitlines(keepends=True)
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != 2 or cells[0] not in REPRODUCIBILITY_ROWS:
            continue
        wanted = REPRODUCIBILITY_ROWS[cells[0]](manifest)
        if wanted is None:
            continue
        # Preserve the row's own backtick convention rather than imposing one.
        ticked = cells[1].startswith("`") and cells[1].endswith("`")
        rendered = f"`{wanted}`" if ticked else str(wanted)
        if rendered == cells[1]:
            continue
        lines[idx] = line.replace(cells[1], rendered, 1)
        changes.append({"metric": f"manifest:{cells[0]}", "was": cells[1],
                        "now": rendered, "lines": [idx + 1]})
    return "".join(lines), changes


def stale_prose(text: str, changes: List[dict]) -> List[str]:
    """Sentences whose wording may no longer follow from the numbers around them.

    A substitution cannot turn 'improves' into 'does not improve'. Flagging the
    direction words near a changed value is the cheapest way to make sure a human
    reads the ones that matter.
    """
    direction = re.compile(
        r"\b(improv\w*|degrad\w*|outperform\w*|better|worse|higher|lower|"
        r"increase\w*|decrease\w*|gain\w*|reduc\w*|negative|positive)\b", re.I)
    lines = text.splitlines()
    flagged: List[str] = []
    for change in changes:
        for line_no in change["lines"]:
            idx = line_no - 1
            for line in lines[max(0, idx - 1):idx + 2]:
                if direction.search(line) and line.strip() and line.strip() not in flagged:
                    flagged.append(line.strip())
    return flagged


# ----------------------------------------------------------------------- main

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="write the drafts and the sidecars (default: report only)")
    parser.add_argument("--seed-from", metavar="GITREF",
                        help="build sidecars by matching the draft against measurements "
                             "at this ref (use when a draft is already stale)")
    parser.add_argument("--only", metavar="STEM", help="restrict to one draft")
    parser.add_argument("--check", action="store_true",
                        help="exit non-zero if any draft disagrees with its recorded "
                             "run, or if anything needs an author. For CI.")
    parser.add_argument("--reseed", action="store_true",
                        help="rebuild the sidecar from the draft as it stands. Use after "
                             "reconciling a draft by hand, to capture spellings the "
                             "previous seed could not match.")
    parser.add_argument("--seed-also", metavar="METRIC=OLDVALUE", nargs="*", default=[],
                        help="bootstrap a metric that did not exist at the seed ref, by "
                             "giving the value the draft currently states. Needed once "
                             "per metric that a run only ever printed: p1 quoted its "
                             "corpus size in prose for months without recording it, so "
                             "there is nothing at any ref to match against.")
    args = parser.parse_args()

    seed_also: Dict[str, float] = {}
    for pair in args.seed_also:
        metric, _, raw = pair.partition("=")
        seed_also[metric] = float(raw)

    os.makedirs(SIDECAR_DIR, exist_ok=True)
    targets = run_ids()
    if args.only:
        targets = {k: v for k, v in targets.items() if args.only in k}
        if not targets:
            print(f"no draft matching {args.only!r}")
            return 2

    total_changes = 0
    total_unresolved = 0
    print("=== re-syncing manuscripts from recorded measurements ===")
    for stem, run_id in targets.items():
        new = load_measurements(run_id)
        if not new:
            continue
        text = open(draft_path(stem), encoding="utf-8").read()

        side = sidecar_path(stem)
        if args.reseed:
            # Rebuild the anchors against what the draft says now. Valid only when
            # the draft is already in agreement with the run -- after a manual
            # reconciliation, say -- because it takes the draft's spellings as
            # correct. It finds nothing to change by construction; the point is to
            # capture spellings the previous seed could not see.
            anchors = seed(new, text)
        elif args.seed_from:
            old = measurements_at_ref(run_id, args.seed_from)
            if not old:
                print(f"  {stem[:52]:52} no measurements at {args.seed_from}")
                continue
            for metric, value in seed_also.items():
                if metric in new:
                    old[metric] = {"metric": metric, "value": value}
            anchors = seed(old, text)
        elif os.path.exists(side):
            anchors = json.load(open(side, encoding="utf-8"))["anchors"]
        else:
            print(f"  {stem[:52]:52} no sidecar; run with --seed-from")
            continue

        updated, changes, blocked = resync(stem, anchors, new)
        # Run metadata is anchored on its row label, not on its current value, so
        # it is projected separately from the measurement-driven substitutions.
        updated, meta_changes = sync_reproducibility_table(run_id, updated)
        changes = changes + meta_changes
        total_changes += len(changes)
        total_unresolved += len(blocked)

        status = f"{len(changes):>3} updated"
        if blocked:
            status += f", {len(blocked)} need a decision"
        print(f"  {stem[:52]:52} {status}")

        def where(lines: List[int]) -> str:
            head = ", ".join(f"L{n}" for n in lines[:4])
            return head + (f" +{len(lines) - 4}" if len(lines) > 4 else "")

        for change in changes:
            print(f"      {change['was']} -> {change['now']:<12} "
                  f"{change['metric'][:60]:<60} {where(change['lines'])}")
        for item in blocked:
            print(f"      HOLD {item['literal']!r} ({item['reason']}) {where(item['lines'])}")
            if item["detail"]:
                print(f"           {item['detail']}")

        anchored = {c["metric"] for a in anchors for c in a["claims"]}
        orphans = sorted(set(new) - anchored)
        if orphans:
            # A recorded metric with no anchor is not necessarily a problem -- plenty
            # inform no sentence. But it is the only warning you get for a value the
            # draft states as a single digit: 'improves 5 and degrades 5' cannot be
            # anchored, because a bare '5' matches everything, so it silently stayed
            # at 5 while the run moved to 1 and 7. Say so, and let someone look.
            print(f"      -- {len(orphans)} recorded metric(s) not anchored anywhere in "
                  f"this draft; a single-digit value cannot be tracked automatically:")
            print(f"         {', '.join(orphans[:12])}"
                  + (f" +{len(orphans) - 12} more" if len(orphans) > 12 else ""))

        prose = stale_prose(updated, changes)
        if prose:
            print(f"      -- read these {len(prose)} line(s): a number moved underneath them")
            for line in prose[:8]:
                print(f"         {line[:150]}")

        if args.apply:
            open(draft_path(stem), "w", encoding="utf-8").write(updated)
            json.dump({"stem": stem, "run_id": run_id, "anchors": anchors},
                      open(side, "w", encoding="utf-8"), indent=2, sort_keys=True)

    print(f"\n{total_changes} value(s) re-synced, {total_unresolved} needing a decision.")
    if args.check:
        # For CI. A draft that disagrees with its run is exactly as wrong as a
        # claim with no artifact behind it, and until now only the second had a
        # non-zero exit code to say so.
        if total_changes or total_unresolved:
            print("\nCHECK FAILED. A draft disagrees with its recorded run.\n"
                  "  Re-sync it:  backend/.venv/bin/python "
                  "scripts/experiments/resync_manuscripts.py --apply\n"
                  "  Anything listed as HOLD needs an author, not a re-run.")
            return 1
        print("\nCHECK PASSED. Every draft agrees with its recorded run.")
        return 0
    if not args.apply:
        print("Report only. Re-run with --apply to write.")
    else:
        print("Verify with: backend/.venv/bin/python scripts/run_submission_gate.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
