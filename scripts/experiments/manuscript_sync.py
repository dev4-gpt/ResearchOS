"""Rewrite manuscript sections from recorded measurements.

Typing numbers into a manuscript by hand is how a paper drifts away from its
evidence: p3's mutant count moved from 940 to 943 between two runs of the same
script, and only a regeneration step caught it. This module replaces named
passages with text rendered from ``measurements.jsonl``, so the manuscript and
the run cannot disagree.

Substitution uses ``@@token@@`` rather than :meth:`str.format`, because the
manuscripts are full of LaTeX braces that ``format`` reads as field names.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DRAFTS = os.path.join(REPO_ROOT, "vault", "04_Drafts")
RUNS = os.path.join(REPO_ROOT, "runs")


def load_measurements(run_id: str) -> Tuple[Dict[str, float], Dict[str, Any]]:
    """Return {metric: value} and {metric: full record} for one run."""
    values: Dict[str, float] = {}
    records: Dict[str, Any] = {}
    path = os.path.join(RUNS, run_id, "measurements.jsonl")
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            values[row["metric"]] = row["value"]
            records[row["metric"]] = row
    return values, records


def load_artifact(run_id: str, name: str) -> Any:
    with open(os.path.join(RUNS, run_id, "artifacts", name), encoding="utf-8") as handle:
        return json.load(handle)


def fill(template: str, context: Dict[str, Any]) -> str:
    """Substitute @@token@@ placeholders. Leaves LaTeX braces untouched."""
    out = template
    for key, value in context.items():
        out = out.replace(f"@@{key}@@", str(value))
    return out


def ci_text(record: Dict[str, Any], decimals: int = 2) -> str:
    """Render a recorded confidence interval, or an empty string if none."""
    ci = record.get("ci95")
    if not ci:
        return ""
    return f"[{ci[0]:.{decimals}f}, {ci[1]:.{decimals}f}]"


class ManuscriptEditor:
    """Span-replacement over a draft, anchored on stable text markers."""

    def __init__(self, stem: str):
        self.path = os.path.join(DRAFTS, f"{stem}.md")
        self.stem = stem
        self.text = open(self.path, encoding="utf-8").read()
        self._edits: List[str] = []

    def already_rewritten(self, sentinel: str) -> bool:
        """True when a previous run already applied this rewrite.

        The rewrites consume their own anchors, so without this a second run
        crashes on a missing marker rather than doing nothing.
        """
        if sentinel in self.text:
            print(f"  {self.stem}: already rewritten, skipping")
            return True
        return False

    def replace_span(self, start_marker: str, end_marker: str, replacement: str,
                     label: str = "") -> "ManuscriptEditor":
        """Replace everything from start_marker up to (not including) end_marker."""
        start = self.text.index(start_marker)
        end = self.text.index(end_marker, start + len(start_marker))
        self.text = self.text[:start] + replacement + self.text[end:]
        self._edits.append(label or start_marker[:40])
        return self

    def replace_to_end(self, start_marker: str, replacement: str,
                       label: str = "") -> "ManuscriptEditor":
        """Replace from start_marker to the end of the document."""
        start = self.text.index(start_marker)
        self.text = self.text[:start] + replacement
        self._edits.append(label or start_marker[:40])
        return self

    def swap(self, old: str, new: str, required: bool = True) -> "ManuscriptEditor":
        if old not in self.text:
            if required:
                raise ValueError(f"{self.stem}: text not found: {old[:70]!r}")
            return self
        self.text = self.text.replace(old, new)
        self._edits.append(old[:40])
        return self

    def assert_absent(self, needles: List[str]) -> "ManuscriptEditor":
        """Fail loudly if a retired fabricated figure survived the rewrite."""
        # Check both spellings: values appear escaped in exported .tex and plain in
        # the Markdown source, and checking only one let '38.7%' survive as '38.7\\%'
        # was searched for.
        variants = []
        for needle in needles:
            variants.append(needle)
            variants.append(needle.replace("\\%", "%"))
            variants.append(needle.replace("%", "\\%"))
        leftover = sorted({n for n in variants if n in self.text})
        if leftover:
            raise AssertionError(f"{self.stem}: stale claims still present: {leftover}")
        return self

    def save(self) -> None:
        open(self.path, "w", encoding="utf-8").write(self.text)
        print(f"  {self.stem}: {len(self._edits)} edits applied")
