import io
import re
import httpx
from typing import Dict, Any, Optional
from pypdf import PdfReader

class PDFExtractionService:
    def __init__(self, timeout: float = 20.0):
        self.client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": "ResearchingOS/0.1 (Academic PDF Ingestion)"}
        )

    def extract_text_from_url(self, pdf_url: str, max_pages: int = 25) -> Dict[str, Any]:
        """Downloads a PDF from a URL and extracts structured section text."""
        if not pdf_url:
            return {"success": False, "error": "No PDF URL provided", "full_text": ""}

        # Normalize arXiv URL if it's an abstract link
        if "arxiv.org/abs/" in pdf_url:
            pdf_url = pdf_url.replace("arxiv.org/abs/", "arxiv.org/pdf/")
        if not pdf_url.endswith(".pdf") and "arxiv.org/pdf/" not in pdf_url:
            pdf_url += ".pdf"

        try:
            response = self.client.get(pdf_url)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"HTTP status {response.status_code} fetching PDF",
                    "full_text": ""
                }

            return self.extract_text_from_bytes(response.content, max_pages=max_pages)
        except Exception as e:
            return {"success": False, "error": str(e), "full_text": ""}

    def extract_text_from_bytes(self, pdf_bytes: bytes, max_pages: int = 25) -> Dict[str, Any]:
        """Parses PDF bytes into structured markdown sections."""
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            total_pages = len(reader.pages)
            pages_to_read = min(total_pages, max_pages)

            raw_pages = []
            for i in range(pages_to_read):
                page_text = reader.pages[i].extract_text() or ""
                raw_pages.append(page_text)

            combined_text = "\n\n".join(raw_pages)
            cleaned_text = self._clean_pdf_text(combined_text)
            sections = self._parse_sections(cleaned_text)

            return {
                "success": True,
                "page_count": total_pages,
                "pages_read": pages_to_read,
                "full_text": cleaned_text[:35000],  # Smart truncation for model context budget
                "sections": sections,
                "error": None
            }
        except Exception as e:
            return {"success": False, "error": str(e), "full_text": ""}

    def _clean_pdf_text(self, text: str) -> str:
        """Cleans headers, footers, duplicate whitespace, and references."""
        # Strip line breaks inside sentences
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove common arXiv header lines
        text = re.sub(r'arXiv:\d{4}\.\d{4,5}v\d+\s+\[[\w\.-]+\]\s+\d+\s+\w+\s+\d{4}', '', text)
        return text.strip()

    def _parse_sections(self, text: str) -> Dict[str, str]:
        """Parses text into major academic section blocks."""
        headings = [
            "abstract", "introduction", "related work", "method", "methodology",
            "system architecture", "experiments", "results", "discussion", "conclusion"
        ]
        
        sections: Dict[str, str] = {}
        lines = text.split("\n")
        current_section = "overview"
        section_buffer = []

        for line in lines:
            line_clean = line.strip().lower()
            matched_heading = None
            for h in headings:
                if line_clean == h or re.match(fr'^\d*[\.\s]*{h}$', line_clean):
                    matched_heading = h
                    break
            
            if matched_heading:
                if section_buffer:
                    sections[current_section] = "\n".join(section_buffer).strip()
                current_section = matched_heading.replace(" ", "_")
                section_buffer = [line]
            else:
                section_buffer.append(line)

        if section_buffer:
            sections[current_section] = "\n".join(section_buffer).strip()

        return sections
