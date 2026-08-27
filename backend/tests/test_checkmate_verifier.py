"""Regression tests for Checkmate's false-green failure modes.

Every test here corresponds to an input Checkmate once certified as
APPROVED_FOR_HUMAN_REVIEW even though the property being asserted was never
verified: an artifact with no manuscript in it, an evidence audit that never
ran, a defect the audit itself detected but scored past, and a TeX source that
was never supplied.
"""

import os
import sys

import pytest

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from services.checkmate_verifier import (  # noqa: E402
    MIN_RENDERED_CHARS,
    CheckmateVerifierService,
    extract_markdown_tables,
    missing_rendered_tables,
)


VALID_TEX = r"""\documentclass[journal]{IEEEtran}
\begin{document}
\title{A Study of Things}
\author{Aryaman Dev}
\maketitle
\begin{abstract}
An abstract long enough to satisfy the completeness test.
\end{abstract}
Body.
\end{document}
"""

PASSING_EVIDENCE = {
    "status": "passed",
    "failed_count": 0,
    "fact_check_score": 100.0,
    "blocking_errors": [],
}


def _write_pdf(path, lines):
    """Emit a one-page PDF whose text layer is exactly `lines`."""

    def esc(text):
        return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

    body = "BT /F1 11 Tf 72 720 Td 14 TL\n"
    for line in lines:
        body += f"({esc(line)}) Tj T*\n"
    body += "ET"

    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [4 0 R] /Count 1 >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 3 0 R >> >> /Contents 5 0 R >>",
        f"<< /Length {len(body)} >>\nstream\n{body}\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{index} 0 obj\n{obj}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode()
    path.write_bytes(bytes(out))
    return str(path)


def _substantive_lines(extra=()):
    """A text layer long enough to clear the artifact-fidelity floor."""
    lines = [
        "A Study of Things",
        "Aryaman Dev",
        "Abstract-An abstract long enough to satisfy the completeness test.",
        "I. INTRODUCTION",
    ]
    filler = ("This sentence carries ordinary manuscript prose so the rendered "
              "artifact contains a plausible amount of extractable text.")
    while sum(len(line) for line in lines) < MIN_RENDERED_CHARS + 500:
        lines.append(filler)
    return lines + list(extra)


@pytest.fixture
def verifier():
    return CheckmateVerifierService(None)


def test_hollow_artifact_is_not_certified(tmp_path, verifier):
    """An eight-line stub with no data, tables, or references must not pass.

    Before the fix this exact input scored 100.0 and returned
    APPROVED_FOR_HUMAN_REVIEW, because every check was an absence check.
    """
    pdf = _write_pdf(tmp_path / "hollow.pdf", [
        "A Study of Things",
        "Aryaman Dev",
        "Abstract-We improved throughput by 47.3 percent on 500 enterprise codebases.",
        "I. INTRODUCTION",
        "Things are important. We studied them. They got better.",
    ])
    report = verifier.audit_pdf(
        pdf, manuscript_markdown="# A Study of Things\n", venue_key="IEEEtran",
        tex_source=VALID_TEX, evidence_report=PASSING_EVIDENCE,
    )

    assert report["checkmate_passed"] is False
    assert "artifact_fidelity" in report["failed_checks"]
    assert report["certificate"]["decision"] == "REMEDIATION_REQUIRED"


def test_missing_evidence_report_fails_closed(tmp_path, verifier):
    """No evidence audit is not a passing evidence audit."""
    pdf = _write_pdf(tmp_path / "no_evidence.pdf", _substantive_lines())
    report = verifier.audit_pdf(
        pdf, manuscript_markdown="# T\n", venue_key="IEEEtran", tex_source=VALID_TEX,
    )

    grounding = report["checks"]["evidence_grounding"]
    assert grounding["passed"] is False
    assert "not run" in grounding["detail"].lower()
    assert report["checkmate_passed"] is False


def test_evidence_report_with_failed_claims_fails(tmp_path, verifier):
    """A report carrying failed claims cannot pass on its status string alone."""
    pdf = _write_pdf(tmp_path / "ungrounded.pdf", _substantive_lines())
    report = verifier.audit_pdf(
        pdf, manuscript_markdown="# T\n", venue_key="IEEEtran", tex_source=VALID_TEX,
        evidence_report={"status": "NOT_RUN", "failed_count": 726,
                         "fact_check_score": 0.0, "blocking_errors": ["726 claims ungrounded"]},
    )

    assert report["checks"]["evidence_grounding"]["passed"] is False
    assert report["checkmate_passed"] is False


def test_detected_defect_is_never_certified(tmp_path, verifier):
    """A flagged synthetic bibliography used to be scored past at 91.7."""
    pdf = _write_pdf(tmp_path / "fake_bib.pdf", _substantive_lines([
        "REFERENCES",
        "[1] Author and Team. Foundational research study: Agentic Systems.",
        "    Journal of Enterprise AI Infrastructure, 2026.",
    ]))
    report = verifier.audit_pdf(
        pdf, manuscript_markdown="# T\n", venue_key="IEEEtran", tex_source=VALID_TEX,
        evidence_report=PASSING_EVIDENCE,
    )

    assert report["checks"]["real_bibliography"]["passed"] is False
    assert report["checkmate_passed"] is False
    assert report["certificate"]["decision"] == "REMEDIATION_REQUIRED"


def test_leaked_meta_prompt_tags_are_never_certified(tmp_path, verifier):
    """Internal persona tags in a camera-ready PDF must block the certificate."""
    pdf = _write_pdf(tmp_path / "meta_leak.pdf", _substantive_lines([
        "[Chairman Synthesis] [Red Team] [Peer Review] Senior Systems Engineer",
    ]))
    report = verifier.audit_pdf(
        pdf, manuscript_markdown="# T\n", venue_key="IEEEtran", tex_source=VALID_TEX,
        evidence_report=PASSING_EVIDENCE,
    )

    assert report["checks"]["zero_meta_leakage"]["passed"] is False
    assert report["checkmate_passed"] is False


def test_absent_tex_source_does_not_pass_the_syntax_check(tmp_path, verifier):
    """"100% sound and balanced" was reported for a source never supplied."""
    pdf = _write_pdf(tmp_path / "no_tex.pdf", _substantive_lines())
    report = verifier.audit_pdf(
        pdf, manuscript_markdown="# T\n", venue_key="IEEEtran", tex_source="",
        evidence_report=PASSING_EVIDENCE,
    )

    syntax = report["checks"]["clean_tex_syntax"]
    assert syntax["passed"] is False
    assert "No TeX source" in syntax["detail"]


def test_stripped_tables_are_detected():
    """The historical defect: table rows deleted between Markdown and LaTeX."""
    markdown = (
        "## Results\n\n"
        "| Pipeline depth | Permutations sound | Mean stage index |\n"
        "|:---:|:---:|:---:|\n"
        "| 2 | 73.60 | 0.00 |\n"
        "| 12 | 9.22 | 0.75 |\n"
    )
    rendered_without_table = "Results\nWe report the outcome of the composition study.\n"
    rendered_with_table = (
        "Results\nPipeline depth Permutations sound Mean stage index\n"
        "2 73.60 0.00\n12 9.22 0.75\n"
    )

    assert missing_rendered_tables(markdown, rendered_without_table)
    assert missing_rendered_tables(markdown, rendered_with_table) == []


def test_ascii_diagrams_in_code_fences_are_not_tables():
    """Pipe-drawn architecture diagrams must not be mistaken for tables."""
    markdown = (
        "```\n"
        "+-------------------------------+\n"
        "|  Tier 1: Perceptual Routing   |\n"
        "|  - Fast Intent Dispatcher     |\n"
        "+-------------------------------+\n"
        "```\n"
    )

    assert extract_markdown_tables(markdown) == []
    assert missing_rendered_tables(markdown, "unrelated body text") == []


def test_abstract_terminator_is_case_sensitive(tmp_path, verifier):
    """A line starting with a year is not the end of the abstract.

    IGNORECASE on the whole pattern made [A-Z] match lowercase, so an abstract
    reading "...appeared in\n2023 or later" was reported truncated mid-sentence.
    """
    pdf = _write_pdf(tmp_path / "year_wrap.pdf", _substantive_lines([
        "Of the corpus, 68.63 percent appeared in",
        "2023 or later, spread across 714 distinct venues.",
    ]))
    report = verifier.audit_pdf(
        pdf, manuscript_markdown="# T\n", venue_key="IEEEtran", tex_source=VALID_TEX,
        evidence_report=PASSING_EVIDENCE,
    )

    assert report["checks"]["complete_abstract"]["passed"] is True


def test_corrupt_error_ledger_is_not_silently_reinitialised(tmp_path):
    """A truncated ledger used to load as an empty one, discarding 77 incidents."""
    from services.error_ledger import ErrorLedgerService

    ledger = tmp_path / "system_error_ledger.json"
    ErrorLedgerService(str(ledger))
    raw = ledger.read_text(encoding="utf-8")
    ledger.write_text(raw[: len(raw) // 2], encoding="utf-8")

    with pytest.raises(RuntimeError, match="could not be read"):
        ErrorLedgerService(str(ledger))

    # The corrupted file must survive for recovery rather than be overwritten.
    assert ledger.read_text(encoding="utf-8") == raw[: len(raw) // 2]


def test_unreadable_drafts_fail_the_dissimilarity_audit():
    """Drafts that could not be read were silently dropped and scored 0% overlap."""

    class UnreadableVault:
        vault_path = "vault"

        def list_files(self, category):
            return [{"filename": "a.md"}, {"filename": "b.md"}]

        def read_markdown(self, category, filename):
            raise IOError("iCloud placeholder not materialised")

    report = CheckmateVerifierService(UnreadableVault()).audit_pairwise_vault_dissimilarity()

    assert report["passed"] is False
    assert report["unreadable_drafts"] == ["a.md", "b.md"]
