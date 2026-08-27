"""Triage the flagged-citation backlog, and remember the decisions (ERR-062).

`CitationRelevanceService` scores vocabulary overlap between a sentence and the
work it cites. That is a triage signal and nothing more: it flags InstructGPT and
GPT-3, whose relevance is contextual, and it cannot tell a weak citation from a
false one. Because nothing recorded a decision, every run re-flagged the same 103
occurrences and the list could only ever grow.

Two things are added here.

**A decision record.** `vault/00_System/citation_decisions.json` holds one entry
per reviewed occurrence -- keep, remove, or needs-author -- with the reason. The
report then lists only what nobody has ruled on, so the backlog can actually
reach zero.

**A misattribution detector.** This is the part worth automating, because it is
not a judgement call. When the prose names a paper, a system or an author --
"Switch Transformer [[k]]", "Adapter layers [[k]]", "Aghajanyan et al. [[k]]" --
and the work `k` resolves to contains none of those words, the citation is not
weak, it is wrong. Seventeen of these were in the corpus. "Adapter layers" cited
GPT-3; "Paged attention" cited a paper on sparse autoencoders; "Byzantine fault
tolerance" cited one on fine-tuning CLIP.

What this deliberately will not do is choose a replacement. The scorer's own
suggestions included replacing InstructGPT with "Automated Fracture Image
Captioning" and a program-repair claim with "Comparative Analysis of Deep
Learning Models for Breast Cancer Classification" (ERR-062, R62). Removing a
false attribution is always an improvement and needs no literature search;
choosing the right source is authorship and is left alone. A claim that loses its
citation keeps its text and becomes unattributed, which is the honest state.

    backend/.venv/bin/python scripts/review_citations.py
    backend/.venv/bin/python scripts/review_citations.py --remove-misattributions --apply
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from typing import Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))

from services.citation_relevance import CitationRelevanceService  # noqa: E402

DRAFTS = os.path.join(REPO_ROOT, "vault", "04_Drafts")
DECISIONS = os.path.join(REPO_ROOT, "vault", "00_System", "citation_decisions.json")
REPORT = os.path.join(REPO_ROOT, "vault", "00_System", "CITATION_REVIEW.md")

# Words that carry no identity, so their presence in a title proves nothing.
STOP = {
    "the", "a", "an", "of", "for", "and", "in", "on", "with", "to", "our", "we", "this",
    "that", "is", "are", "as", "by", "from", "its", "their", "using", "via", "be", "it",
    "these", "those", "each", "all", "not", "but", "which", "can", "may", "has", "have",
    "been", "at", "or", "if", "such", "see", "section", "appendix", "table", "figure",
    "theorem", "lemma", "corollary", "eq", "equation", "figures", "tables",
}

# A named artefact sitting immediately before a citation. The capital is what makes
# it a name rather than prose; up to three trailing words catch "Switch Transformer",
# "Personalized PageRank diffusion", "Vision Transformer backbone".
# The trailing characters are "anything that is not a space or a bracket" rather
# than an ASCII class, because model names are full of unicode: an earlier version
# spelled out [A-Za-z0-9./+-] and so could not see "Mixtral 8x7B" when the x is a
# multiplication sign, which is exactly one of the misattributed citations.
NAMED = re.compile(r"([A-Z][^\s\[\]]*(?:[- ][A-Za-z0-9][^\s\[\]]*){0,3})\s*\[\[([^\]]+)\]\]")


def tokens(text: str) -> set:
    return {t for t in re.split(r"[^a-z0-9]+", text.lower())
            if t and t not in STOP and len(t) > 2}


def load_decisions() -> dict:
    if os.path.exists(DECISIONS):
        return json.load(open(DECISIONS, encoding="utf-8"))
    return {"decisions": {}}


def decision_id(stem: str, key: str, name: str) -> str:
    """Identify a decision by what it is about, not by line number.

    Line numbers move every time a draft is re-synced or a section is expanded.
    Keying on them would silently un-review everything after the first edit.
    """
    return f"{stem}::{key}::{name.lower()}"


def find_misattributions(service: CitationRelevanceService, notes: dict) -> list:
    """Occurrences where the prose names something the cited title does not contain."""
    rows = []
    for path in sorted(glob.glob(os.path.join(DRAFTS, "*.md"))):
        stem = os.path.basename(path)[:-3]
        for line_no, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
            for name, key in NAMED.findall(line):
                note = service._lookup(notes, key.strip())
                title = (note or {}).get("title", "")
                if not title:
                    continue          # unresolved keys are the citation checker's job
                # A maths fragment is not a name. Widening the pattern to catch
                # unicode model names also let it capture things like
                # 'L_{\text{full}}$)', and a symbol has no business being
                # compared against a paper title.
                if re.search(r"[$\\{}^_]", name):
                    continue
                named = tokens(name)
                if not named or named & tokens(title):
                    continue
                rows.append({"draft": stem, "line": line_no, "name": name.strip(),
                             "key": key.strip(), "title": title})
    return rows


def strip_citation(line: str, name: str, key: str) -> str:
    """Remove one '[[key]]' that follows *name*, leaving the sentence readable."""
    pattern = re.compile(re.escape(name) + r"(\s*)\[\[" + re.escape(key) + r"\]\]")
    out = pattern.sub(lambda m: name, line, count=1)
    return re.sub(r" {2,}", " ", out).replace(" .", ".").replace(" ,", ",")



def strip_key(key: str, flagged_lines: dict, every_occurrence: bool = False) -> Tuple[int, int]:
    """Remove '[[key]]' citations. Returns (occurrences removed, drafts touched).

    By default this removes only the occurrences the relevance scorer actually
    flagged, not every appearance of the key. The distinction is not academic: a
    first version removed whole keys and took 76 citations when 40 were flagged,
    because these keys also appear in positions the scorer rated relevant.
    Distinct citation counts halved -- p1 went 16 to 10 against a 15-30 target --
    for occurrences nobody had objected to. Ruling that a source is a poor fit for
    one sentence is not the same as ruling it has no place in the paper.

    Pass every_occurrence=True for the stronger ruling, when the source genuinely
    does not belong in the corpus at all.

    Either way this deletes the *citation*, never the vault note. Nothing treats a
    missing note as a broken link, so deleting the note would leave the manuscript
    citing a source that no longer exists and the bibliography rendering an empty
    entry. The note records a paper that does exist; the defect is that a sentence
    points at it.
    """
    removed = drafts = 0
    pattern = re.compile(r"\s*\[\[" + re.escape(key) + r"\]\]")
    for path in sorted(glob.glob(os.path.join(DRAFTS, "*.md"))):
        stem = os.path.basename(path)[:-3]
        targets = flagged_lines.get((stem, key), set())
        if not every_occurrence and not targets:
            continue
        lines = open(path, encoding="utf-8").read().splitlines(keepends=True)
        hits = 0
        for idx, line in enumerate(lines):
            if not every_occurrence and (idx + 1) not in targets:
                continue
            found = len(pattern.findall(line))
            if not found:
                continue
            cleaned = pattern.sub("", line)
            cleaned = re.sub(r" {2,}", " ", cleaned).replace(" .", ".").replace(" ,", ",")
            lines[idx] = cleaned
            hits += found
        if hits:
            open(path, "w", encoding="utf-8").write("".join(lines))
            removed += hits
            drafts += 1
    return removed, drafts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remove-misattributions", action="store_true",
                        help="strip citations whose prose names a different work")
    parser.add_argument("--remove-key", metavar="KEY", nargs="*", default=[],
                        help="strip every occurrence of these citation keys from every "
                             "draft. The unit of decision is the key, not the occurrence: "
                             "28 keys carry all 83 flagged citations, and a source that "
                             "does not belong in this corpus does not belong in it 13 "
                             "times over.")
    parser.add_argument("--all-occurrences", action="store_true",
                        help="with --remove-key, strip every appearance of the key "
                             "rather than only the flagged ones. The stronger ruling: "
                             "this source has no place in the paper at all.")
    parser.add_argument("--keep-key", metavar="KEY", nargs="*", default=[],
                        help="record these keys as reviewed-and-kept, retiring their "
                             "flags without touching the drafts")
    parser.add_argument("--by-key", action="store_true",
                        help="list the open flags grouped by cited work, which is the "
                             "shape the decision actually has")
    parser.add_argument("--apply", action="store_true", help="write the drafts and the record")
    args = parser.parse_args()

    service = CitationRelevanceService(vault_path=os.path.join(REPO_ROOT, "vault"))
    notes = service.load_notes()
    record = load_decisions()

    misattributed = find_misattributions(service, notes)
    print(f"=== misattributed citations: {len(misattributed)} ===")
    for row in misattributed:
        print(f"  {row['draft'][:30]:30} L{row['line']:<5} \"{row['name']}\"")
        print(f"       -> {row['key']:36} = {row['title'][:56]}")

    if args.remove_misattributions and misattributed:
        by_draft = {}
        for row in misattributed:
            by_draft.setdefault(row["draft"], []).append(row)

        removed = 0
        for stem, rows in sorted(by_draft.items()):
            path = os.path.join(DRAFTS, f"{stem}.md")
            lines = open(path, encoding="utf-8").read().splitlines(keepends=True)
            for row in rows:
                idx = row["line"] - 1
                before = lines[idx]
                after = strip_citation(before, row["name"], row["key"])
                if after == before:
                    print(f"  ! {stem} L{row['line']}: could not locate, left alone")
                    continue
                lines[idx] = after
                removed += 1
                record["decisions"][decision_id(stem, row["key"], row["name"])] = {
                    "decision": "removed",
                    "reason": (f"prose names {row['name']!r}; key resolves to "
                               f"{row['title'][:70]!r}, which is a different work"),
                    "draft": stem, "key": row["key"], "name": row["name"],
                }
            if args.apply:
                open(path, "w", encoding="utf-8").write("".join(lines))
        print(f"\n{removed} false attribution(s) "
              f"{'removed' if args.apply else 'would be removed'}.")
        if args.apply:
            os.makedirs(os.path.dirname(DECISIONS), exist_ok=True)
            json.dump(record, open(DECISIONS, "w", encoding="utf-8"),
                      indent=2, sort_keys=True)
            print(f"Decisions recorded in {os.path.relpath(DECISIONS, REPO_ROOT)}")

    if args.by_key:
        results_ = service.audit_all(DRAFTS)
        ruled = {d["key"] for d in record["decisions"].values()
                 if d["decision"] == "keep" and d.get("draft") == "*"}
        flagged_ = [(st, u) for st, us in results_.items() for u in us
                    if u.verdict not in ("relevant", "strong") and u.key not in ruled]
        groups: dict = {}
        for st, u in flagged_:
            groups.setdefault((u.key, u.title), []).append((st, u))
        print(f"\n=== {len(flagged_)} open flag(s) across {len(groups)} cited work(s) ===")
        for (key, title), rows in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            where = sorted({st[:30] for st, _ in rows})
            print(f"\n[{len(rows):>2}x] {title[:62]}")
            print(f"       {key}")
            print(f"       in: {', '.join(where)}")
            print(f"       e.g. {' '.join(rows[0][1].context.split())[:100]}")
        print("\nDecide per key:")
        print("  --remove-key <KEY> ... --apply     strip it from every draft")
        print("  --keep-key   <KEY> ... --apply     record it as reviewed, change nothing")

    flagged_lines: dict = {}
    if args.remove_key:
        for st, us in service.audit_all(DRAFTS).items():
            for u in us:
                if u.verdict not in ("relevant", "strong"):
                    flagged_lines.setdefault((st, u.key), set()).add(u.line_no)

    for key in args.remove_key:
        removed, drafts = (strip_key(key, flagged_lines, args.all_occurrences)
                           if args.apply else (0, 0))
        note = (f"{removed} occurrence(s) in {drafts} draft(s)" if args.apply
                else "(dry run; add --apply)")
        print(f"  remove-key {key}: {note}")
        if args.apply:
            record["decisions"][f"key::{key}"] = {
                "decision": "removed", "draft": "*", "key": key, "name": "(whole key)",
                "title": "", "reason": "removed from every draft by author decision",
            }

    for key in args.keep_key:
        print(f"  keep-key {key}: recorded as reviewed")
        if args.apply:
            record["decisions"][f"key::{key}"] = {
                "decision": "keep", "draft": "*", "key": key, "name": "(whole key)",
                "title": "", "reason": "reviewed and kept by author decision",
            }

    if args.apply and (args.remove_key or args.keep_key):
        os.makedirs(os.path.dirname(DECISIONS), exist_ok=True)
        json.dump(record, open(DECISIONS, "w", encoding="utf-8"), indent=2, sort_keys=True)

    # What is left for a human. Removed occurrences are gone from the drafts, so
    # they simply do not appear here any more; the record exists so the same call
    # is not made twice, and so a "keep" ruling can retire a flag without deleting
    # anything.
    results = service.audit_all(DRAFTS)
    flagged = [(stem, u) for stem, us in results.items() for u in us
               if u.verdict not in ("relevant", "strong")]
    # A ruling recorded per key applies to every draft, and stores "*" as the
    # draft. Matching on the pair alone silently ignored those, so nine keeps
    # were written to the record and the report still listed all 43 as open.
    kept_keys = {d["key"] for d in record["decisions"].values()
                 if d["decision"] == "keep" and d.get("draft") == "*"}
    kept_pairs = {(d["draft"], d["key"]) for d in record["decisions"].values()
                  if d["decision"] == "keep" and d.get("draft") != "*"}
    open_items = [(st, u) for st, u in flagged
                  if u.key not in kept_keys and (st, u.key) not in kept_pairs]

    print(f"\nflagged now: {len(flagged)}   ruled 'keep': {len(flagged) - len(open_items)}"
          f"   still needing an author: {len(open_items)}")
    print(f"decisions on record: {len(record['decisions'])}")

    if args.apply:
        write_report(open_items, record)
        print(f"Report rewritten: {os.path.relpath(REPORT, REPO_ROOT)}")
    return 0


def write_report(open_items: list, record: dict) -> None:
    """Rewrite CITATION_REVIEW.md as the open list, not the whole history.

    The previous report listed every flagged occurrence on every run and appended
    a block of suggested replacements. Both were counterproductive: the list could
    not shrink, and the suggestions were the thing that had to be refused --
    'Automated Fracture Image Captioning' offered in place of InstructGPT.
    """
    removed = [d for d in record["decisions"].values() if d["decision"] == "removed"]
    lines = [
        "# Citation Review",
        "",
        "Citations flagged by `CitationRelevanceService` as having little topical",
        "overlap with the sentence citing them. The scorer measures vocabulary, not",
        "whether a source supports a claim, so this is triage and not a verdict: it",
        "flags foundational citations whose relevance is contextual.",
        "",
        "Decisions are recorded in `citation_decisions.json` and subtracted here, so",
        "this list can reach zero. **No replacement is suggested.** Lexical similarity",
        "cannot judge whether a source supports a claim, and when it was asked to try",
        "it proposed replacing InstructGPT with a paper on fracture image captioning",
        "(ERR-062, R62).",
        "",
        f"## Resolved automatically: {len(removed)} false attributions removed",
        "",
        "These were not weak citations. In each, the prose named a paper, a system or",
        "an author, and the key resolved to a different work entirely -- 'Adapter",
        "layers' citing GPT-3, 'Paged attention' citing a sparse-autoencoder paper,",
        "'Byzantine fault tolerance' citing one on fine-tuning CLIP. The citation was",
        "deleted and the sentence left standing without attribution, which is the",
        "honest state; supplying the correct source is authorship.",
        "",
        "| Manuscript | Named in prose | Key | Resolved to |",
        "|:---|:---|:---|:---|",
    ]
    for d in sorted(removed, key=lambda d: (d["draft"], d["name"])):
        title = d.get("title", "")[:56]
        lines.append(f"| {d['draft'][:34]} | {d['name'][:34]} | `{d['key'][:34]}` | {title} |")

    lines += [
        "",
        f"## Open: {len(open_items)} occurrences needing an author decision",
        "",
        "Keep, remove, or replace. To retire one without changing the draft, add a",
        '`\"decision\": \"keep\"` entry for it in `citation_decisions.json`.',
        "",
        "| Manuscript | Line | Score | Cited work | Citing context |",
        "|:---|---:|---:|:---|:---|",
    ]
    for stem, u in sorted(open_items, key=lambda r: (r[0], r[1].line_no)):
        context = " ".join(u.context.split())[:90]
        lines.append(f"| {stem[:34]} | {u.line_no} | {u.score:.4g} | "
                     f"{u.title[:44]} | {context} |")
    lines.append("")
    open(REPORT, "w", encoding="utf-8").write("\n".join(lines))


if __name__ == "__main__":
    raise SystemExit(main())
