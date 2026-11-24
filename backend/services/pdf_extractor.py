import io
import re
import httpx
from urllib.parse import urlsplit, urlunsplit
from typing import Dict, Any, Optional
from pypdf import PdfReader

class PDFExtractionService:
    ALLOWED_HOSTS = {'arxiv.org', 'export.arxiv.org', 'pmc.ncbi.nlm.nih.gov', 'europepmc.org'}
    MAX_PDF_BYTES = 20 * 1024 * 1024

    def __init__(self, timeout: float = 20.0):
        self.client = httpx.Client(
            timeout=timeout,
            follow_redirects=False,
            trust_env=False,
            headers={"User-Agent": "ResearchingOS/0.1 (Academic PDF Ingestion)"}
        )

    def extract_text_from_url(self, pdf_url: str, max_pages: int = 25) -> Dict[str, Any]:
        """Downloads a PDF from a URL and extracts structured section text."""
        if not pdf_url:
            return {"success": False, "error": "No PDF URL provided", "full_text": ""}

        # Paper metadata is untrusted. Never fetch arbitrary hosts, local URLs,
        # credentials or redirects; unsupported repositories retain abstracts.
        try:
            parsed = urlsplit(pdf_url)
            if (parsed.scheme != 'https' or parsed.hostname not in self.ALLOWED_HOSTS
                    or parsed.port not in (None, 443) or parsed.username or parsed.password):
                raise ValueError('Unsupported PDF origin')
            path = parsed.path
            if parsed.hostname in {'arxiv.org', 'export.arxiv.org'}:
                path = path.replace('/abs/', '/pdf/', 1)
            pdf_url = urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, ''))
        except ValueError:
            return {'success': False, 'error': 'Unsupported PDF origin', 'full_text': ''}

        try:
            with self.client.stream('GET', pdf_url) as response:
                if response.status_code != 200:
                    return {'success': False, 'error': f'HTTP status {response.status_code} fetching PDF', 'full_text': ''}
                body = bytearray()
                for chunk in response.iter_bytes():
                    body.extend(chunk)
                    if len(body) > self.MAX_PDF_BYTES:
                        return {'success': False, 'error': 'PDF exceeds byte limit', 'full_text': ''}
            return self.extract_text_from_bytes(bytes(body), max_pages=max_pages)
        except Exception:
            return {"success": False, "error": 'PDF download failed', "full_text": ""}

    def extract_text_from_bytes(self, pdf_bytes: bytes, max_pages: int = 25) -> Dict[str, Any]:
        """Parses PDF bytes into structured markdown sections."""
        try:
            if len(pdf_bytes) > self.MAX_PDF_BYTES or not 1 <= max_pages <= 100:
                return {'success': False, 'error': 'PDF input exceeds extraction limits', 'full_text': ''}
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
