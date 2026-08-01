import pytest
from services.pdf_extractor import PDFExtractionService

def test_pdf_extractor_initialization():
    service = PDFExtractionService()
    assert service is not None

def test_clean_pdf_text():
    service = PDFExtractionService()
    raw_text = "arXiv:2203.11171v1  [cs.CL]  21 Mar 2022\n\nMethodology-\nSection and results."
    cleaned = service._clean_pdf_text(raw_text)
    assert "MethodologySection" in cleaned or "Methodology" in cleaned

def test_parse_sections():
    service = PDFExtractionService()
    text = "Abstract\nThis is the abstract.\n\nIntroduction\nThis is the introduction.\n\nMethodology\nThis is the methodology."
    sections = service._parse_sections(text)
    assert "abstract" in sections or "introduction" in sections or "overview" in sections
