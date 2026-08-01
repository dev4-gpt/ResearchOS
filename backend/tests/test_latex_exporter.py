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
    assert "\\IEEEauthorblockN{Author One}" in tex_code
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
