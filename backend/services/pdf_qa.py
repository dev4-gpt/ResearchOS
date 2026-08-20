from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


FORBIDDEN_ARTIFACTS = ("¡", "¿", "[?]", "�", "TODO", "FIXME")


class PDFQualityAssurance:
    def inspect_text(self, text: str, *, profile: Optional[dict] = None) -> Dict[str, Any]:
        errors = []
        for token in FORBIDDEN_ARTIFACTS:
            if token in text:
                errors.append(f"Forbidden PDF artifact detected: {token}")
        if profile:
            for token in profile.get("forbidden_tokens", []):
                if token in text:
                    errors.append(f"Venue-forbidden token detected: {token}")
            lowered = text.lower()
            for section in profile.get("required_sections", []):
                if section.lower() not in lowered:
                    errors.append(f"Required venue section is missing: {section}")
        if re.search(r"(?:/Users/|/home/|[A-Za-z]:\\)", text):
            errors.append("Local filesystem path leaked into PDF text.")
        return {"status": "passed" if not errors else "failed", "errors": sorted(set(errors))}

    def inspect_pdf(self, pdf_path: str, *, profile: Optional[dict] = None) -> Dict[str, Any]:
        path = Path(pdf_path)
        errors = []
        if not path.exists() or path.stat().st_size == 0:
            return {"status": "failed", "errors": ["PDF is missing or empty."]}
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            result = self.inspect_text(text, profile=profile)
            errors.extend(result["errors"])
            if len(reader.pages) == 0:
                errors.append("PDF contains no pages.")
            max_limit = max(profile.get("page_limit", 0), profile.get("long_page_limit", 0), profile.get("short_page_limit", 0)) or 20
            if len(reader.pages) > max_limit:
                errors.append(f"PDF has {len(reader.pages)} pages; limit is {max_limit}.")
        except Exception as exc:
            errors.append(f"PDF inspection failed: {exc}")
        return {"status": "passed" if not errors else "failed", "errors": sorted(set(errors))}

    def inspect_tex(self, tex: str, *, profile: Optional[dict] = None) -> Dict[str, Any]:
        errors = []
        if "\\begin{document}" not in tex or "\\end{document}" not in tex:
            errors.append("TeX document boundaries are incomplete.")
        if re.search(r"\\cite\{\s*\}", tex):
            errors.append("Empty citation command detected.")
        if profile:
            for token in profile.get("forbidden_tokens", []):
                if token in tex:
                    errors.append(f"Venue-forbidden token detected in TeX: {token}")
            lowered = tex.lower()
            for section in profile.get("required_sections", []):
                if section.lower() not in lowered:
                    errors.append(f"Required venue section is missing: {section}")
        return {"status": "passed" if not errors else "failed", "errors": errors}
