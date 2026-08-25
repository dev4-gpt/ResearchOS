"""Claim Provenance Gate.

Every quantitative claim in a manuscript must trace to a recorded artifact before
that manuscript may be routed to a submission-grade venue.

The gap this closes: drafts carry precise-looking figures ("N = 500", "47.2%",
"p < 0.001", "Cohen's d = 1.14") that no run in ``runs/`` ever produced. Nothing in
the existing audit chain notices — CheckmateVerifierService scores structure and
citation-key resolution, not whether a number was ever measured. So the numbers
survive all the way into 108 venue packages.

Grounding is resolved against two stores, strongest first:

``EXPERIMENT``  the value matches a measurement in ``runs/<run_id>/measurements.jsonl``,
               which records the artifact and its sha256.
``CITATION``   the value is attributed in-sentence to a resolvable ``[[paper_id]]``,
               so the manuscript is reporting someone else's finding, not its own.
``UNGROUNDED`` neither. The paper asserts a measurement it cannot support.

This module reports and gates. It never invents a measurement to close a gap, and
it never rewrites a draft: remediation is the caller's decision, because "strip the
claim" and "go run the experiment" are not interchangeable.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple


# Preprint servers and directories publish without certifying that the reported
# numbers were measured. Every other venue is peer-reviewed, and its reviewers read
# an unattributed number as the authors' own measurement — so the gate applies to
# open-access journals exactly as it does to top conferences.
NON_CERTIFYING_VENUES = frozenset({"arXiv", "DOAJ"})


def certifies_measurement(venue_key: str) -> bool:
    """True when the venue's review treats reported numbers as the authors' own."""
    return venue_key not in NON_CERTIFYING_VENUES

GROUNDING_EXPERIMENT = "EXPERIMENT"
GROUNDING_CITATION = "CITATION"
GROUNDING_UNGROUNDED = "UNGROUNDED"


@dataclass
class QuantitativeClaim:
    """One numeric assertion lifted from a manuscript, with enough context to judge it."""

    claim_id: str
    raw: str
    value: Optional[float]
    unit: str
    kind: str
    line_no: int
    sentence: str
    cite_keys: List[str] = field(default_factory=list)
    grounding: str = GROUNDING_UNGROUNDED
    evidence: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProvenanceReport:
    draft: str
    run_id: str
    total_claims: int
    experiment_backed: int
    citation_backed: int
    ungrounded: int
    claims: List[QuantitativeClaim]
    measurements_found: int

    @property
    def grounded_ratio(self) -> float:
        if not self.total_claims:
            return 1.0
        return (self.experiment_backed + self.citation_backed) / self.total_claims

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["grounded_ratio"] = round(self.grounded_ratio, 4)
        return data


class ClaimProvenanceService:
    """Extracts quantitative claims from a draft and binds them to recorded evidence."""

    # Ordered: the first pattern that matches a span wins, so that a compound token
    # such as 'p < 0.001' is not also harvested as a bare decimal.
    _PATTERNS: Tuple[Tuple[str, str, str], ...] = (
        ("p_value", r"p\s*[<>=]\s*0?\.\d+", ""),
        ("effect_size", r"(?:Cohen's\s*)?\bd\s*=\s*-?\d+(?:\.\d+)?", ""),
        ("sample_size", r"\bN\s*=\s*\d[\d,{}\\]*", "n"),
        ("test_stat", r"\b[tFUZ]\s*\(\s*[\d,\s]+\)\s*=\s*-?\d+(?:\.\d+)?", ""),
        ("percentage", r"-?\d+(?:\.\d+)?\s*\\?%", "%"),
        ("percentage_points", r"[-+]?\d+(?:\.\d+)?\s*pp\b", "pp"),
        # Negative lookahead: '8x7B' names a model, it is not an eight-fold factor.
        ("factor", r"\d+(?:\.\d+)?\s*(?:\$\\times\$|×|x)\b(?!\s*\d)", "x"),
        # Only an escaped '\$' is currency. A bare '$' followed by digits is the
        # opening delimiter of inline math ("$1 - p_k$", "$20{,}000$"), and reading
        # those as prices produced a stream of phantom unbacked claims.
        ("currency", r"\\\$\s*\d+(?:\.\d+)?", "$"),
        ("duration", r"\d+(?:\.\d+)?\s*(?:ms|s|min|h)\b(?:/task)?", "time"),
        ("memory", r"\d+(?:\.\d+)?\s*(?:GB|MB|TB)\b", "bytes"),
        ("mass", r"\d+(?:\.\d+)?\s*kg\b", "kg"),
    )

    #: "95% CI" / "95% confidence interval" states the interval level, and a trial
    #: or resample count states an experimental parameter. Neither is a measured
    #: finding that needs its own artifact.
    _INTERVAL_LEVEL = re.compile(
        r"(?:95|90|99)\s*\\?%\s*(?:CI\b|confidence|credible|lower\s+bound|"
        r"upper\s+bound|interval|probability)",
        re.IGNORECASE,
    )

    _WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
    _CITE = re.compile(r"\\cite\{([^}]+)\}")
    # A claim attributed to prior work rather than measured here.
    _ATTRIBUTION = re.compile(
        r"\b(?:report(?:ed|s)?|observ(?:ed|es)|found|according to|shown by|"
        r"demonstrated by|per|follows?|prior work|baseline[sd]?\s+from|"
        # A requirement or specification carrying a citation is attributed to that
        # source; it states a target the cited work defines, not a result measured here.
        r"specif(?:y|ied|ication)|must\s+(?:provide|carry|satisfy|meet)|"
        r"require[sd]?|mandate[sd]?|target(?:ed)?\s+at)\b",
        re.IGNORECASE,
    )

    def __init__(self, vault_path: str = "vault", runs_root: str = "runs") -> None:
        self.vault_path = vault_path
        self.runs_root = runs_root

    # ------------------------------------------------------------------ claims

    def extract_claims(self, markdown: str) -> List[QuantitativeClaim]:
        """Harvest every numeric assertion, skipping structural/reference noise."""
        claims: List[QuantitativeClaim] = []
        seen_spans: List[Tuple[int, int, int]] = []

        for line_no, line in enumerate(markdown.split("\n"), start=1):
            if self._is_noise_line(line):
                continue
            cite_keys = self._WIKILINK.findall(line) + [
                k.strip()
                for group in self._CITE.findall(line)
                for k in group.split(",")
            ]
            for kind, pattern, unit in self._PATTERNS:
                for match in re.finditer(pattern, line):
                    span = (line_no, match.start(), match.end())
                    if self._overlaps(span, seen_spans):
                        continue
                    raw = match.group(0).strip()
                    if kind == "percentage" and self._INTERVAL_LEVEL.match(
                        line[match.start():match.start() + 30]
                    ):
                        continue
                    seen_spans.append(span)
                    claims.append(
                        QuantitativeClaim(
                            claim_id=f"C{len(claims) + 1:04d}",
                            raw=raw,
                            value=self._parse_value(raw),
                            unit=unit,
                            kind=kind,
                            line_no=line_no,
                            sentence=self._sentence_around(line, match.start()),
                            cite_keys=sorted(set(cite_keys)),
                        )
                    )
        return claims

    @staticmethod
    def _is_noise_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return True
        # Section numbering, YAML frontmatter and equation bodies are not claims.
        if stripped.startswith(("#", "---", "$$", "\\begin", "\\end", ">")):
            return True
        if re.match(r"^\s*\d+(\.\d+)*\s*$", stripped):
            return True
        return False

    @staticmethod
    def _overlaps(span: Tuple[int, int, int], seen: List[Tuple[int, int, int]]) -> bool:
        line_no, start, end = span
        return any(
            other_line == line_no and start < other_end and end > other_start
            for other_line, other_start, other_end in seen
        )

    @staticmethod
    def _parse_value(raw: str) -> Optional[float]:
        match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?", raw.replace("{,}", ","))
        if not match:
            return None
        try:
            return float(match.group(0).replace(",", ""))
        except ValueError:
            return None

    @staticmethod
    def _sentence_around(line: str, index: int) -> str:
        start = max(line.rfind(". ", 0, index) + 1, line.rfind("| ", 0, index) + 1, 0)
        end_candidates = [p for p in (line.find(". ", index), line.find(" |", index)) if p != -1]
        end = min(end_candidates) if end_candidates else len(line)
        return line[start:end].strip()[:400]

    # ------------------------------------------------------------- measurements

    def load_measurements(self, run_id: str) -> List[Dict[str, Any]]:
        """Read recorded measurements for a run. Absent file means nothing was measured."""
        path = os.path.join(self.runs_root, run_id, "measurements.jsonl")
        if not os.path.exists(path):
            return []
        records: List[Dict[str, Any]] = []
        with open(path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    records.append(json.loads(raw_line))
                except json.JSONDecodeError:
                    continue
        return records

    #: A claim is only backed by a measurement in a compatible unit. Without this,
    #: a bare "$1" matches any recorded value of 1.0 and reports itself as grounded,
    #: which is the exact false positive this service exists to prevent.
    _UNIT_COMPAT: Dict[str, frozenset] = {
        "%": frozenset({"%", "percent"}),
        "x": frozenset({"x", "factor", "exponent", "multiplier"}),
        "$": frozenset({"$", "usd"}),
        "n": frozenset({"n", "count", "messages", "hops", "instances", "tasks"}),
        "time": frozenset({"time", "s", "ms", "min", "h", "seconds"}),
        "bytes": frozenset({"bytes", "gb", "mb", "tb"}),
        "kg": frozenset({"kg"}),
        "pp": frozenset({"pp", "%"}),
        "": frozenset({"", "d", "t", "p", "exponent", "statistic"}),
    }

    @classmethod
    def _units_compatible(cls, claim_unit: str, record_unit: Optional[str]) -> bool:
        allowed = cls._UNIT_COMPAT.get(claim_unit)
        if allowed is None:
            return True
        return str(record_unit or "").strip().lower() in allowed

    @staticmethod
    def _matches_measurement(claim: QuantitativeClaim, record: Dict[str, Any]) -> bool:
        """A measurement backs a claim when the recorded value matches it numerically.

        Requires a real artifact reference: a measurement row with no artifact is an
        assertion in a different file, not evidence.
        """
        if not record.get("artifact") or not record.get("sha256"):
            return False
        if claim.value is None:
            return False
        # A sample/trial count is a stated experimental parameter, so it is backed
        # when a measurement was actually recorded over that many observations.
        if claim.kind == "sample_size" and claim.value is not None:
            try:
                if record.get("n") is not None and float(record["n"]) == claim.value:
                    return True
            except (TypeError, ValueError):
                pass
        if not ClaimProvenanceService._units_compatible(claim.unit, record.get("unit")):
            return False
        recorded_raw = record.get("value")
        if recorded_raw is None:
            return False
        try:
            recorded = float(recorded_raw)
        except (TypeError, ValueError):
            return False
        # A manuscript reporting "d = 2.13" for a measured 2.1339 is rounding
        # correctly, not asserting a different number. Accept the claim when the
        # recorded value rounds to it at the precision the claim was written to.
        fraction = re.search(r"\.(\d+)", claim.raw)
        decimals = len(fraction.group(1)) if fraction else 0
        try:
            if round(recorded, decimals) == round(claim.value, decimals):
                return True
        except (TypeError, ValueError):
            pass
        tolerance = max(abs(recorded) * 1e-6, 1e-9)
        return abs(recorded - claim.value) <= tolerance

    # ------------------------------------------------------------------- audit

    def classify(
        self,
        claims: List[QuantitativeClaim],
        measurements: List[Dict[str, Any]],
        known_citation_keys: Optional[set] = None,
    ) -> None:
        """Assign a grounding verdict to each claim, in place."""
        known = known_citation_keys if known_citation_keys is not None else set()
        for claim in claims:
            backing = next(
                (m for m in measurements if self._matches_measurement(claim, m)), None
            )
            if backing is not None:
                claim.grounding = GROUNDING_EXPERIMENT
                claim.evidence = f"{backing.get('artifact')}#{str(backing.get('sha256'))[:12]}"
                continue

            # Attribution only counts when the sentence both cites a resolvable key
            # and reads as reporting someone else's result.
            resolvable = [k for k in claim.cite_keys if not known or k in known]
            if resolvable and self._ATTRIBUTION.search(claim.sentence):
                claim.grounding = GROUNDING_CITATION
                claim.evidence = f"attributed to {resolvable[0]}"
                continue

            claim.grounding = GROUNDING_UNGROUNDED
            claim.evidence = None

    def audit_draft(
        self,
        draft_path: str,
        run_id: Optional[str] = None,
        known_citation_keys: Optional[set] = None,
    ) -> ProvenanceReport:
        """Full provenance audit for one manuscript."""
        with open(draft_path, "r", encoding="utf-8") as handle:
            markdown = handle.read()

        stem = os.path.splitext(os.path.basename(draft_path))[0]
        resolved_run_id = run_id or f"draft-{stem}"

        claims = self.extract_claims(markdown)
        measurements = self.load_measurements(resolved_run_id)
        self.classify(claims, measurements, known_citation_keys)

        return ProvenanceReport(
            draft=stem,
            run_id=resolved_run_id,
            total_claims=len(claims),
            experiment_backed=sum(c.grounding == GROUNDING_EXPERIMENT for c in claims),
            citation_backed=sum(c.grounding == GROUNDING_CITATION for c in claims),
            ungrounded=sum(c.grounding == GROUNDING_UNGROUNDED for c in claims),
            claims=claims,
            measurements_found=len(measurements),
        )

    # -------------------------------------------------------------------- gate

    def gate(self, report: ProvenanceReport, venue_key: str) -> Dict[str, Any]:
        """Decide whether this manuscript may be built for this venue.

        An empirical venue requires zero ungrounded claims. Everything else is
        allowed through with the unbacked claims named, so the caller can strip or
        reframe them deliberately.
        """
        blocking = [c for c in report.claims if c.grounding == GROUNDING_UNGROUNDED]
        certifies = certifies_measurement(venue_key)

        allowed = not (certifies and blocking)
        if allowed and not blocking:
            reason = "All quantitative claims trace to recorded evidence."
        elif allowed:
            reason = (
                f"{len(blocking)} unbacked claim(s) present; {venue_key} does not certify "
                "measurement, but they must still be stripped or attributed before release."
            )
        else:
            reason = (
                f"{venue_key} reviews reported measurements as the authors' own, and "
                f"{len(blocking)} claim(s) have no artifact in runs/{report.run_id}/."
            )

        return {
            "venue": venue_key,
            "allowed": allowed,
            "certifying_venue": certifies,
            "blocking_claim_count": len(blocking),
            "blocking_claims": [c.to_dict() for c in blocking[:25]],
            "reason": reason,
        }

    # ------------------------------------------------------------------ report

    def audit_all_drafts(
        self, drafts_dir: Optional[str] = None, known_citation_keys: Optional[set] = None
    ) -> Dict[str, ProvenanceReport]:
        """Audit every manuscript in the drafts directory."""
        directory = drafts_dir or os.path.join(self.vault_path, "04_Drafts")
        reports: Dict[str, ProvenanceReport] = {}
        for name in sorted(os.listdir(directory)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(directory, name)
            reports[os.path.splitext(name)[0]] = self.audit_draft(
                path, known_citation_keys=known_citation_keys
            )
        return reports

    @staticmethod
    def render_markdown(reports: Dict[str, ProvenanceReport]) -> str:
        """Human-readable provenance summary for the vault."""
        lines = [
            "# Claim Provenance Report",
            "",
            "Every quantitative claim in each manuscript, resolved against recorded",
            "evidence. `EXPERIMENT` means a measurement artifact in `runs/<run_id>/`",
            "matches the value; `CITATION` means the sentence attributes it to a cited",
            "source; `UNGROUNDED` means the manuscript asserts a measurement it cannot",
            "support.",
            "",
            "| Manuscript | Claims | Experiment | Citation | Ungrounded | Grounded % |",
            "|:---|---:|---:|---:|---:|---:|",
        ]
        for stem, report in sorted(reports.items()):
            lines.append(
                f"| {stem} | {report.total_claims} | {report.experiment_backed} | "
                f"{report.citation_backed} | {report.ungrounded} | "
                f"{report.grounded_ratio * 100:.1f}% |"
            )

        for stem, report in sorted(reports.items()):
            unbacked = [c for c in report.claims if c.grounding == GROUNDING_UNGROUNDED]
            if not unbacked:
                continue
            lines += ["", f"## {stem} — {len(unbacked)} ungrounded", ""]
            for claim in unbacked[:40]:
                lines.append(f"- **L{claim.line_no}** `{claim.raw}` — {claim.sentence[:150]}")
        return "\n".join(lines) + "\n"
