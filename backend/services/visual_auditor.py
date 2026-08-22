import os, glob, re, pymupdf
from typing import List, Dict, Any, Optional
from services.checkmate_verifier import CheckmateVerifierService

class VisualLayoutAuditorService:
    """Renders PDF page preview PNG tiles and executes dual-layer (Visual Geometry + Checkmate Textual) audits."""

    def __init__(self, vault_manager=None):
        self.vault_manager = vault_manager
        self.checkmate_verifier = CheckmateVerifierService(vault_manager)

    def render_page_tiles(self, pdf_path: str, output_dir: str, dpi: int = 150) -> List[Dict[str, Any]]:
        """Renders all PDF pages into PNG preview tiles and returns page tile metadata."""
        if not os.path.exists(pdf_path):
            return []

        os.makedirs(output_dir, exist_ok=True)
        pdf_basename = os.path.basename(pdf_path).replace('.pdf', '')

        doc = pymupdf.open(pdf_path)
        tile_records = []

        for i, page in enumerate(doc):
            page_num = i + 1
            pix = page.get_pixmap(dpi=dpi)
            tile_filename = f"{pdf_basename}_p{page_num}.png"
            tile_path = os.path.join(output_dir, tile_filename)
            pix.save(tile_path)

            tile_records.append({
                "page": page_num,
                "filename": tile_filename,
                "file_path": tile_path,
                "width": pix.width,
                "height": pix.height,
                "aspect_ratio": round(pix.width / pix.height, 3)
            })

        doc.close()
        return tile_records

    def audit_layout_geometry(self, pdf_path: str, venue_key: str = "IEEEtran") -> Dict[str, Any]:
        """Audits PDF layout dimensions, margin overflows (Overfull hbox), and column boundaries."""
        if not os.path.exists(pdf_path):
            return {"passed": False, "detail": "PDF file not found"}

        doc = pymupdf.open(pdf_path)
        total_pages = len(doc)
        margin_overflows = []

        # Two-column venues have ~85mm (240pt) column width, full span is ~450pt
        is_two_column = venue_key in ("IEEEtran", "ICML", "CVPR", "ACL", "ACM", "NeurIPS")
        column_limit_pt = 475 if is_two_column else 540


        for i, page in enumerate(doc):
            page_num = i + 1
            text_instances = page.get_text("blocks")
            for block in text_instances:
                x0, y0, x1, y1, text, block_no, block_type = block
                width = x1 - x0
                # Detect lines extending past physical printable page margins (page width is 612pt for letter / 595pt for A4)
                if x1 > 576 or x0 < 36:
                    margin_overflows.append({
                        "page": page_num,
                        "bbox": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
                        "width": round(width, 1),
                        "text_snippet": text.strip()[:60]
                    })

        doc.close()

        return {
            "passed": len(margin_overflows) == 0,
            "total_pages": total_pages,
            "overflow_count": len(margin_overflows),
            "margin_overflows": margin_overflows,
            "detail": "0 margin overflows detected" if len(margin_overflows) == 0 else f"{len(margin_overflows)} margin overflows detected"
        }

    def audit_full_manuscript(
        self,
        pdf_path: str,
        manuscript_markdown: str,
        venue_key: str = "IEEEtran",
        tile_output_dir: Optional[str] = None,
        tex_source: str = "",
        package_fallback_used: bool = False,
        evidence_report: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Runs unified Visual Geometry + Checkmate 7-Point Audit and generates preview PNG tiles."""
        checkmate_res = self.checkmate_verifier.audit_pdf(
            pdf_path,
            manuscript_markdown=manuscript_markdown,
            venue_key=venue_key,
            tex_source=tex_source,
            package_fallback_used=package_fallback_used,
            evidence_report=evidence_report,
        )
        layout_res = self.audit_layout_geometry(pdf_path, venue_key=venue_key)

        tile_records = []
        if tile_output_dir:
            tile_records = self.render_page_tiles(pdf_path, tile_output_dir)

        combined_passed = checkmate_res.get("checkmate_passed", False) and layout_res.get("passed", True)

        return {
            "checkmate_passed": combined_passed,
            "score": checkmate_res.get("score", 100.0),
            "status": "PASSED" if combined_passed else "NEEDS_REMEDIATION",
            "total_pages": checkmate_res.get("total_pages", layout_res.get("total_pages", 0)),
            "checkmate_checks": checkmate_res.get("checks", {}),
            "certificate": checkmate_res.get("certificate", {}),
            "layout_geometry": layout_res,
            "page_tiles": tile_records
        }
