import pytest
from services.latex_exporter import LaTeXExporterService

def test_latex_export_service_basic():
    exporter = LaTeXExporterService()
    title = "Test Systematic Review"
    authors = ["Author One", "Author Two"]
    abstract = "This is a test abstract for IEEEtran export."
    body = "# Introduction\n\nThis is a test section with [[paper_1]] reference and **bold text**."

    tex_code = exporter.markdown_to_ieeetran(title, authors, abstract, body)

    assert "\\title{Test Systematic Review}" in tex_code
    assert "Author One" in tex_code
    assert "\\begin{abstract}" in tex_code
    assert "\\cite{paper_1}" in tex_code
    assert "\\textbf{bold text}" in tex_code

def test_bibtex_generation():
    exporter = LaTeXExporterService()
    papers = [
        {
            "filename": "crossref_10.2139_ssrn.5260645.md",
            "frontmatter": {
                "title": "Thinking Like A Lawyer In The Age Of Generative AI",
                "authors": ["Daniel Schwarcz", "Dongyeop Kang"],
                "published": "2025-05-20",
                "url": "https://doi.org/10.2139/ssrn.5260645"
            }
        }
    ]

    bib_code = exporter.generate_bibtex(papers)

    assert "@article{crossref_10_2139_ssrn_5260645," in bib_code
    assert "Thinking Like A Lawyer In The Age Of Generative AI" in bib_code
    assert "Daniel Schwarcz and Dongyeop Kang" in bib_code


def test_display_math_preserves_cases_rows_exponents_and_column_fit():
    exporter = LaTeXExporterService()
    body = r"""
# Formula checks

The exponent $k^*$ must remain math, not Markdown emphasis.

$$\text{Verify}(T', C_{\text{inv}}) = \begin{cases} 1, & \text{if } C_{\text{inv}} \\ 0, & \text{otherwise} \end{cases}$$

$$\text{SecurityPass}(T') = \bigwedge_{i=1}^m (\text{NoUnsafePointer}(T') \land \text{SanitizedInputs}(T') \land \text{NoBufferOverflow}(T'))$$
"""
    tex_code = exporter.markdown_to_ieeetran("Math Safety", ["Author"], "Abstract", body)

    assert "k^*" in tex_code
    assert "\\resizebox{\\columnwidth}{!}" in tex_code
    assert "\\\\ 0" in tex_code
    assert "Nested equation environment inside resizebox" not in exporter.validate_latex_source(tex_code)
    assert exporter.validate_latex_source(tex_code) == []


# --- ACM / acmart author topmatter (ERR-046) --------------------------------
# The acmart branch used to emit a bare ``\author{first_author}``: no
# ``\affiliation``, no ``\email``, and every co-author dropped. acmart accepts
# that source silently, so ACM packages built and shipped with blank author
# metadata that every ACM venue requires.

ACM_BODY = (
    "# A Study\n\n## Executive Abstract\n\n"
    "An abstract long enough to survive the exporter's sentence trimming.\n\n"
    "## Introduction\n\nBody text.\n"
)
ACM_DETAILS = {
    "affiliation": "Pennsylvania State University",
    "email": "asd5520@psu.edu",
}


def _acm_topmatter(tex_code):
    """The source between \\title and \\begin{abstract} — acmart's author block."""
    return tex_code[tex_code.index("\\title"):tex_code.index("\\begin{abstract}")]


def test_acm_emits_affiliation_and_email_for_the_author():
    exporter = LaTeXExporterService()
    tex_code = exporter.markdown_to_venue_latex(
        "ACM", "A Study", ["Aryaman Singh Dev"], "Executive Abstract",
        ACM_BODY, author_details=ACM_DETAILS,
    )
    topmatter = _acm_topmatter(tex_code)

    assert "\\author{Aryaman Singh Dev}" in topmatter
    assert "\\affiliation{" in topmatter
    assert "\\institution{Pennsylvania State University}" in topmatter
    assert "\\email{asd5520@psu.edu}" in topmatter
    # acmart is order-sensitive: \affiliation and \email belong to the \author
    # that precedes them, and all three must precede \maketitle.
    assert (topmatter.index("\\author{")
            < topmatter.index("\\affiliation{")
            < topmatter.index("\\email{"))
    assert topmatter.index("\\email{") < tex_code.index("\\maketitle")


def test_acm_emits_a_full_block_for_every_author_not_just_the_first():
    exporter = LaTeXExporterService()
    tex_code = exporter.markdown_to_venue_latex(
        "ACM", "A Study", ["Aryaman Singh Dev", "Second Author"],
        "Executive Abstract", ACM_BODY, author_details=ACM_DETAILS,
    )
    topmatter = _acm_topmatter(tex_code)

    assert "\\author{Aryaman Singh Dev}" in topmatter
    assert "\\author{Second Author}" in topmatter
    assert topmatter.count("\\affiliation{") == 2
    assert topmatter.count("\\email{asd5520@psu.edu}") == 2


def test_acm_affiliation_always_carries_a_country():
    """acmart raises a hard class Error on an affiliation with no \\country."""
    exporter = LaTeXExporterService()

    supplied = exporter.markdown_to_venue_latex(
        "ACM", "A Study", ["Aryaman Singh Dev"], "Executive Abstract", ACM_BODY,
        author_details={**ACM_DETAILS, "country": "USA"},
    )
    assert "\\country{USA}" in supplied

    unset = exporter.markdown_to_venue_latex(
        "ACM", "A Study", ["Aryaman Singh Dev"], "Executive Abstract", ACM_BODY,
        author_details=ACM_DETAILS,
    )
    # Missing identity is surfaced loudly in the typeset PDF, never dropped.
    assert "\\country{[COUNTRY NOT SET]}" in unset


def test_acm_surfaces_placeholder_identity_instead_of_shipping_it():
    exporter = LaTeXExporterService()
    tex_code = exporter.markdown_to_venue_latex(
        "ACM", "A Study", ["Aryaman Singh Dev"], "Executive Abstract", ACM_BODY,
        author_details={"affiliation": "Your Institution", "email": ""},
    )
    assert "\\institution{[AFFILIATION NOT SET]}" in tex_code
    assert "[CONTACT EMAIL NOT SET]" in tex_code


def test_acm_abstract_precedes_maketitle_as_acmart_requires():
    exporter = LaTeXExporterService()
    tex_code = exporter.markdown_to_venue_latex(
        "ACM", "A Study", ["Aryaman Singh Dev"], "Executive Abstract", ACM_BODY,
        author_details=ACM_DETAILS,
    )
    assert tex_code.index("\\end{abstract}") < tex_code.index("\\maketitle")


def test_acm_anonymous_export_omits_identifying_metadata():
    exporter = LaTeXExporterService()
    tex_code = exporter.markdown_to_venue_latex(
        "ACM", "A Study", ["Aryaman Singh Dev"], "Executive Abstract", ACM_BODY,
        author_details=ACM_DETAILS, anonymize=True,
    )
    assert "\\author{Anonymous Authors}" in tex_code
    assert "Pennsylvania State University" not in tex_code
    assert "asd5520@psu.edu" not in tex_code
    assert "\\affiliation{" not in tex_code
