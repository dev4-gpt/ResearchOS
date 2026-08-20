import pytest
from services.latex_exporter import LaTeXExporterService

def test_venue_latex_export_neurips():
    exporter = LaTeXExporterService()
    code = exporter.markdown_to_venue_latex(
        "NeurIPS",
        "Test NeurIPS Paper",
        ["Penn State Author"],
        "This is a test abstract.",
        "## 1. Introduction\nThis is a test introduction.\n\n## 2. Methods\nTest methods."
    )
    assert "\\usepackage[final]{neurips_2026}" in code
    assert "\\section{Introduction}" in code
    assert "NeurIPS Paper Checklist" in code

def test_venue_latex_export_icml():
    exporter = LaTeXExporterService()
    code = exporter.markdown_to_venue_latex(
        "ICML",
        "Test ICML Paper",
        ["Penn State Author"],
        "This is a test abstract.",
        "## 1. Methodology\nTest method."
    )
    assert "\\usepackage{icml2026}" in code
    assert "Test ICML Paper" in code

def test_venue_latex_export_cvpr():
    exporter = LaTeXExporterService()
    code = exporter.markdown_to_venue_latex(
        "CVPR",
        "Test CVPR Paper",
        ["Penn State Author"],
        "Abstract",
        "Body"
    )
    assert "\\usepackage{cvpr}" in code

def test_venue_latex_export_acl():
    exporter = LaTeXExporterService()
    code = exporter.markdown_to_venue_latex(
        "ACL",
        "Test ACL Paper",
        ["Penn State Author"],
        "Abstract",
        "Body"
    )
    assert "\\usepackage[review]{acl}" in code

def test_multi_venue_bundle():
    exporter = LaTeXExporterService()
    bundle = exporter.export_multi_venue_bundle(
        "Test Bundle Paper",
        ["Penn State Author"],
        "Abstract",
        "Body"
    )
    assert "NeurIPS" in bundle
    assert "ICML" in bundle
    assert "CVPR" in bundle
    assert "ACL" in bundle
    assert "IEEEtran" in bundle
    assert "ACM" in bundle
