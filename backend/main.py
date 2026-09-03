import os
import re
import json
import asyncio
import threading
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response, FileResponse, JSONResponse

from pydantic import BaseModel
from dotenv import load_dotenv

# Load env variables from root or backend folder
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv()

from services.vault import VaultManager
from services.fact_checker import FactCheckerService
from agents.council import CouncilOrchestrator
from services.latex_exporter import LaTeXExporterService
from services.pdf_qa import PDFQualityAssurance
from services.release_controller import ReleaseController
from services.venue_profiles import SUPPORTED_VENUES, VENUE_PROFILES
from services.evidence_ledger import EvidenceLedger
from services.user_profile import UserProfileService
from agents.venue_advisor import VenueAdvisorAgent
from services.checkmate_verifier import CheckmateVerifierService
from services.publisher_readiness import PublisherReadinessService
from services.publisher_jobs import PublisherReadinessJobManager
from domain.models import RunManifest, citation_key

app = FastAPI(title="ResearchingOS API", description="Backend server for multi-agent academic research council")

# Add CORS Middleware to connect with Vite React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend port. For local, * is fine.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service classes
vault_path = os.getenv("VAULT_PATH", "../vault")
vault_manager = VaultManager(vault_path)
fact_checker = FactCheckerService(vault_manager)
orchestrator = CouncilOrchestrator(vault_path)
pdf_qa = PDFQualityAssurance()
release_controller = ReleaseController()
evidence_ledger = EvidenceLedger(os.path.join(os.path.dirname(vault_manager.vault_path), "runs"))
user_profile_service = UserProfileService(vault_manager.vault_path)
venue_advisor_agent = VenueAdvisorAgent(vault_manager.vault_path)
checkmate_verifier = CheckmateVerifierService(vault_manager)
publisher_readiness_service = PublisherReadinessService(vault_manager)
publisher_readiness_jobs = PublisherReadinessJobManager(publisher_readiness_service)

from services.error_ledger import ErrorLedgerService
error_ledger_service = ErrorLedgerService()

from agents.meta_review_council import MetaReviewCouncil
meta_review_council = MetaReviewCouncil(vault_path)

# In-memory log store for streaming active research runs and meta-reviews
# key: project_id, value: asyncio.Queue containing log dicts
log_queues: Dict[str, asyncio.Queue] = {}

class ResearchRequest(BaseModel):
    topic: str
    target_venue: Optional[str] = "IEEEtran"
    target_length: Optional[str] = "short_camera_ready"  # "short_camera_ready" (4p) | "full_journal" (12p)

class SaveFileRequest(BaseModel):
    category: str
    filename: str
    content: str
    frontmatter: Dict[str, Any]
    trigger_readiness: bool = False

class VenueRecommendRequest(BaseModel):
    title: str
    abstract: str = ""
    topic_keywords: List[str] = []

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    expertise_areas: Optional[List[str]] = None
    citation_count: Optional[int] = None
    h_index: Optional[int] = None
    o1a_criteria_met: Optional[List[str]] = None
    target_timeline: Optional[str] = None
    submission_goals: Optional[str] = None
    publication_history: Optional[List[Dict[str, Any]]] = None

@app.get("/")
def root_index():
    return {
        "name": "ResearchingOS Multi-Agent Engine",
        "status": "online",
        "frontend_url": "http://127.0.0.1:3000",
        "swagger_docs": "http://127.0.0.1:8000/docs",
        "api_health": "http://127.0.0.1:8000/api/health",
        "vault_files": "http://127.0.0.1:8000/api/vault/files",
        "system_design_primer": "https://github.com/donnemartin/system-design-primer"
    }

@app.get("/api/health")
def health_check():
    gemini_key = bool(os.getenv("GEMINI_API_KEY"))
    nim_key = bool(os.getenv("NVIDIA_NIM_API_KEY") or os.getenv("NVIDIA_API_KEY"))
    run_mode = os.getenv("RESEARCHINGOS_RUN_MODE", "auto").strip().lower()
    return {
        "status": "healthy",
        "gemini_api_configured": gemini_key,
        "nvidia_nim_configured": nim_key,
        "vault_path": vault_manager.vault_path,
        "run_mode": run_mode,
        "is_dry_run": orchestrator.is_dry_run,
    }

@app.get("/api/vault/files")
def get_vault_files(category: Optional[str] = None):
    """Lists files in the vault. If category is specified, returns only that category."""
    try:
        categories = ["papers", "concepts", "debates", "drafts"]
        if category:
            if category not in categories:
                raise HTTPException(status_code=400, detail="Invalid category")
            return vault_manager.list_files(category)

        result = {}
        for cat in categories:
            result[cat] = vault_manager.list_files(cat)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/read")
def read_vault_file(category: str, filename: str):
    """Reads a file's content and metadata from the vault."""
    try:
        data = vault_manager.read_markdown(category, filename)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vault/write")
def write_vault_file(request: SaveFileRequest):
    """Saves/edits a file in the vault (HITL updates)."""
    try:
        path = vault_manager.save_markdown(
            request.category,
            request.filename,
            request.content,
            request.frontmatter
        )
        response: Dict[str, Any] = {"status": "success", "saved_path": path}
        if request.category == "drafts" and request.trigger_readiness:
            response["readiness_job"] = publisher_readiness_jobs.start(target_filename=request.filename, trigger="draft_save")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/graph")
def get_vault_graph():
    """Gets the structured nodes and edges from vault markdown files."""
    try:
        graph = vault_manager.get_knowledge_graph()
        return graph
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/fact-check")
def fact_check_vault_file(category: str, filename: str):
    """Performs real-time citation and grounding audit on any vault file and updates frontmatter."""
    try:
        data = vault_manager.read_markdown(category, filename)
        content = data.get("content", "")
        frontmatter = data.get("frontmatter", {}) or {}
        source_records = _source_records()
        report = fact_checker.audit_document(content, source_records=source_records)

        frontmatter["fact_check_score"] = str(report.get("fact_check_score", "0.0"))
        frontmatter["verification_status"] = str(report.get("status", "needs_review"))
        frontmatter["verification_matrix"] = str(report.get("verification_matrix", {}))
        vault_manager.save_markdown(category, filename, content, frontmatter)

        return {
            "status": "success",
            "category": category,
            "filename": filename,
            "audit": report
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _source_records() -> Dict[str, str]:
    """Return source text keyed by canonical citation key for claim-level audits."""
    records: Dict[str, str] = {}
    for item in vault_manager.list_files("papers"):
        try:
            data = vault_manager.read_markdown("papers", item["filename"])
            meta = data.get("frontmatter", {}) or {}
            text = data.get("content", "")
            for key in (item["filename"], meta.get("id", ""), meta.get("title", "")):
                if key:
                    records[citation_key(str(key))] = text
        except Exception:
            continue
    return records


def _paper_data() -> List[Dict[str, Any]]:
    papers = []
    for item in vault_manager.list_files("papers"):
        data = vault_manager.read_markdown("papers", item["filename"])
        data["filename"] = item["filename"]
        papers.append(data)
    return papers


def _fact_check_draft(content: str) -> Dict[str, Any]:
    """Run the same source-backed claim gate used by Publisher Readiness."""
    records = _source_records()
    return fact_checker.audit_document(
        content,
        source_texts=list(records.values()),
        source_records=records,
    )

@app.get("/api/vault/checkmate-audit")
def checkmate_audit(
    filename: str = Query("review_enterprise_adoption_of_multi_agent_ai_systems_infr.md", description="Manuscript filename in drafts"),
    venue: str = Query("IEEEtran", description="Target academic venue")
):
    """Executes The Checkmate Layer multi-modal PDF audit and auto-persists certificate scores."""
    try:
        base = os.path.basename(filename.strip().replace(" ", ""))
        clean_filename = base if base.endswith(".md") else f"{base}.md"
        file_path = os.path.join(vault_manager.vault_path, "04_Drafts", clean_filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Manuscript draft '{clean_filename}' not found in Vault drafts.")

        parsed = vault_manager.read_markdown("drafts", clean_filename)
        frontmatter = parsed.get("frontmatter", {}) or {}
        body = parsed.get("content", "")
        evidence_report = _fact_check_draft(body)

        # Export/compile PDF to verify camera-ready compilation
        from services.latex_exporter import LaTeXExporterService
        latex_service = LaTeXExporterService(vault_manager)
        title = frontmatter.get("title", "Enterprise Adoption of Multi-Agent AI Systems")
        authors = frontmatter.get("authors", ["Aryaman Dev"])
        abstract_match = re.search(r'#+\s*(?:\d+[\.\s]*)?(?:Executive\s+)?Abstract\n+([\s\S]*?)(?=\n+#|\Z)', body, re.IGNORECASE)
        abstract = abstract_match.group(1).strip() if abstract_match else "Executive Abstract"

        papers_data = _paper_data()
        bib_code = latex_service.generate_bibtex(papers_data, manuscript_content=body)
        tex_code = latex_service.markdown_to_venue_latex(venue, title, authors, abstract, body)
        pdf_name = f"{clean_filename.replace('.md', '')}_{venue}.pdf"
        pdf_path = os.path.join(vault_manager.vault_path, "04_Drafts", pdf_name)

        # Compile PDF afresh to ensure camera-ready compliance
        pdf_bytes = latex_service.compile_pdflatex(tex_code, bib_code=bib_code, allow_package_fallback=True)
        if not pdf_bytes:
            log_tail = getattr(latex_service, "last_build_log", "")[-1200:]
            raise HTTPException(status_code=422, detail=f"PDF compilation failed preflight; stale PDF was not audited.\n{log_tail}")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)


        # Execute 7-point Checkmate audit
        audit_res = checkmate_verifier.audit_pdf(
            pdf_path,
            manuscript_markdown=body,
            venue_key=venue,
            tex_source=tex_code,
            package_fallback_used=latex_service.last_compile_used_package_fallback,
            evidence_report=evidence_report,
        )

        # Update frontmatter metadata
        if audit_res.get("checkmate_passed"):
            frontmatter["checkmate_score"] = str(audit_res.get("score", 100.0))
            frontmatter["checkmate_status"] = "PASSED"
            frontmatter["checkmate_date"] = audit_res.get("certificate", {}).get("timestamp", "")
            vault_manager.save_markdown("drafts", clean_filename, body, frontmatter=frontmatter)

        return {
            "success": True,
            "filename": clean_filename,
            "venue": venue,
            "checkmate": audit_res
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/backtest/preview-tiles")
def get_preview_tiles(
    filename: str = Query("autonomous_code_synthesis_and_self_healing_multi_agent_systems.md", description="Manuscript filename"),
    venue: str = Query("IEEEtran", description="Target academic venue")
):
    """Renders PDF pages as high-resolution PNG preview tiles and returns visual layout geometry audit."""
    try:
        from services.visual_auditor import VisualLayoutAuditorService
        from services.latex_exporter import LaTeXExporterService

        base = os.path.basename(filename.strip().replace(" ", ""))
        clean_filename = base if base.endswith(".md") else f"{base}.md"
        parsed = vault_manager.read_markdown("drafts", clean_filename)
        body = parsed.get("content", "")
        evidence_report = _fact_check_draft(body)
        frontmatter = parsed.get("frontmatter", {}) or {}
        title = frontmatter.get("title", clean_filename.replace(".md", ""))
        authors = frontmatter.get("authors") or ["Aryaman Singh Dev"]
        author_details = {"affiliation": "Pennsylvania State University", "email": "asd5520@psu.edu"}

        exporter = LaTeXExporterService(vault_manager)
        auditor = VisualLayoutAuditorService(vault_manager)

        papers_data = _paper_data()
        bib_code = exporter.generate_bibtex(papers_data, manuscript_content=body)
        tex_code = exporter.markdown_to_venue_latex(venue, title, authors, "Executive Abstract", body, author_details=author_details)

        pdf_bytes = exporter.compile_pdflatex(tex_code, bib_code=bib_code, allow_package_fallback=True)
        pdf_name = f"{clean_filename.replace('.md', '')}_{venue}.pdf"
        pdf_path = os.path.join(vault_manager.vault_path, "04_Drafts", pdf_name)
        if not pdf_bytes:
            log_tail = getattr(exporter, "last_build_log", "")[-1200:]
            raise HTTPException(status_code=422, detail=f"Preview compilation failed; stale page tiles were not reused.\n{log_tail}")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        tile_dir = os.path.join(vault_manager.vault_path, "04_Drafts", "preview_tiles")
        audit_data = auditor.audit_full_manuscript(
            pdf_path,
            body,
            venue_key=venue,
            tile_output_dir=tile_dir,
            tex_source=tex_code,
            package_fallback_used=exporter.last_compile_used_package_fallback,
            evidence_report=evidence_report,
        )

        return {
            "success": True,
            "filename": clean_filename,
            "venue": venue,
            "audit": audit_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/backtest/preview-tile-image/{filename:path}/{venue}/{page_num}")
def stream_preview_tile_image(filename: str, venue: str, page_num: int):
    """Streams binary PNG tile image for inline visual rendering in the frontend modal."""
    try:
        clean_filename = os.path.basename(filename.strip().replace(" ", "")).replace(".md", "")
        tile_name = f"{clean_filename}_{venue}_p{page_num}.png"
        tile_path = os.path.join(vault_manager.vault_path, "04_Drafts", "preview_tiles", tile_name)
        if not os.path.exists(tile_path):
            raise HTTPException(status_code=404, detail=f"Preview tile '{tile_name}' not found.")
        return FileResponse(tile_path, media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vault/backtest/auto-remediate")
def auto_remediate_manuscript(
    filename: str = Query("review_autonomous_code_synthesis_and_self_healing_multi_a.md"),
    venue: str = Query("IEEEtran")
):
    """Triggers the Closed-Loop Self-Healing DAG Graph until 100.0 Checkmate score is achieved."""
    try:
        from harness.closed_loop_backtest import ClosedLoopBacktestHarness
        harness = ClosedLoopBacktestHarness(vault_manager)
        result = harness.run_closed_loop(filename, venue_key=venue, max_iters=3)
        return {
            "success": True,
            "filename": filename,
            "venue": venue,
            "result": result
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/backtest")
@app.post("/api/vault/backtest")

def run_backtest_suite(
    filename: Optional[str] = Query(None, description="Optional specific draft filename to test"),
    venues: Optional[List[str]] = Query(None, description="Optional list of venue keys")
):
    """Executes automated multi-venue PDF compilation and Checkmate verifier backtest across vault drafts."""
    try:
        report = checkmate_verifier.run_multi_venue_backtest(target_filename=filename, venues=venues)
        return report
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/publisher/readiness")
@app.post("/api/vault/publisher/readiness")
def run_publisher_readiness_suite(
    filename: Optional[str] = Query(None, description="Optional specific draft filename; omit to test every draft"),
    venues: Optional[List[str]] = Query(None, description="Optional venue keys; omit to test every supported venue"),
    wait: bool = Query(False, description="Run synchronously for CLI/compatibility callers; UI uses background jobs"),
):
    """Runs the HITL Publisher release matrix: every selected draft x every venue.

    This endpoint is intentionally fail-closed. It checks PDF quality, exact/high
    copied-prose overlap with sibling drafts, and substantive research value before
    reporting a venue as ready for human review.
    """
    try:
        if wait:
            return publisher_readiness_service.run(target_filename=filename, venues=venues)
        job = publisher_readiness_jobs.start(target_filename=filename, venues=venues, trigger="manual")
        return JSONResponse(status_code=202, content={"success": True, "job": job})
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/publisher/readiness/status")
def get_publisher_readiness_status(job_id: Optional[str] = Query(None)):
    """Returns the current background readiness job and completed report, if available."""
    job = publisher_readiness_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="No publisher readiness job found")
    return {"success": True, "job": job}

@app.get("/api/vault/publisher/readiness/bundle")
def download_publisher_readiness_bundle():
    """Downloads only artifacts whose latest readiness matrix marked them publish-ready."""
    import io
    import zipfile

    manifest_path = os.path.join(vault_manager.vault_path, "04_Drafts", "exports", "publisher_readiness_manifest.json")
    if not os.path.exists(manifest_path):
        raise HTTPException(status_code=404, detail="Run publisher readiness before requesting a verified bundle")
    try:
        with open(manifest_path, "r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        ready_results = [result for result in manifest.get("results", []) if result.get("publish_ready")]
        if not ready_results:
            raise HTTPException(status_code=409, detail="No verified publish-ready artifacts are available")

        exports_dir = os.path.realpath(os.path.join(vault_manager.vault_path, "04_Drafts", "exports"))
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            bundle.writestr("publisher_readiness_manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
            stage_events_path = manifest.get("stage_events_path")
            if stage_events_path and os.path.exists(stage_events_path):
                safe_stage_path = os.path.realpath(stage_events_path)
                runs_root = os.path.realpath(os.path.join(vault_manager.vault_path, "04_Drafts", "backtest_runs"))
                if safe_stage_path.startswith(runs_root + os.sep):
                    bundle.write(safe_stage_path, arcname="stage_events.jsonl")
                    run_manifest_path = os.path.join(os.path.dirname(safe_stage_path), "manifest.json")
                    if os.path.exists(run_manifest_path):
                        bundle.write(run_manifest_path, arcname="run_manifest.json")
            included = set()
            for result in ready_results:
                for key in ("pdf_path", "tex_path", "bib_path"):
                    path = result.get(key)
                    if not path:
                        continue
                    safe_path = os.path.realpath(path)
                    if not safe_path.startswith(exports_dir + os.sep) or not os.path.exists(safe_path) or safe_path in included:
                        continue
                    included.add(safe_path)
                    bundle.write(safe_path, arcname=os.path.relpath(safe_path, exports_dir))
        archive.seek(0)
        headers = {"Content-Disposition": "attachment; filename=researchingos-publish-ready-bundle.zip"}
        return Response(content=archive.read(), media_type="application/zip", headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/export-latex")
def export_latex(filename: str = "review_systematic_review_meta_taxonomy_of_generative_ai_i.md"):
    """Generates compilable IEEEtran LaTeX and BibTeX from a vault manuscript draft."""
    try:
        from services.latex_exporter import LaTeXExporterService
        exporter = LaTeXExporterService(vault_manager)

        clean_filename = os.path.basename(filename.strip().replace(" ", ""))
        if not clean_filename.endswith(".md"): clean_filename += ".md"

        draft = vault_manager.read_markdown("drafts", clean_filename)
        title = draft["frontmatter"].get("title", "Systematic Review Manuscript")
        frontmatter = draft.get("frontmatter", {}) or {}
        authors = frontmatter.get("authors", [])
        author_details = {
            "affiliation": frontmatter.get("affiliation", ""),
            "email": frontmatter.get("email", ""),
        }
        content = draft["content"]

        abstract_match = content.split("## Executive Abstract\n\n")
        abstract = abstract_match[1].split("\n\n## ")[0] if len(abstract_match) > 1 else "Systematic Review of Enterprise Generative AI."

        tex_code = exporter.markdown_to_ieeetran(
            title, authors, abstract, content, author_details=author_details
        )

        papers_data = _paper_data()
        bib_code = exporter.generate_bibtex(papers_data, manuscript_content=content)

        return {
            "success": True,
            "filename": clean_filename,
            "tex_filename": clean_filename.replace(".md", "_IEEEtran.tex"),
            "bib_filename": "references.bib",
            "tex_code": tex_code,
            "bib_code": bib_code
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/export-venue-latex")
def export_venue_latex(filename: str, venue: Optional[str] = "NeurIPS"):
    """Exports manuscript in specific venue format (NeurIPS, ICML, CVPR, ACL, IEEEtran, ACM) or multi-path bundle."""
    try:
        clean_filename = os.path.basename(filename.strip().replace(" ", ""))
        if not clean_filename.endswith(".md"): clean_filename += ".md"

        doc_data = vault_manager.read_markdown("drafts", clean_filename)
        content = doc_data.get("content", "")
        frontmatter = doc_data.get("frontmatter", {})
        title = frontmatter.get("title", clean_filename.replace(".md", ""))
        authors = frontmatter.get("authors", [])
        author_details = {
            "affiliation": frontmatter.get("affiliation", ""),
            "email": frontmatter.get("email", ""),
        }

        abstract_match = content.split("## Executive Abstract\n\n")
        abstract = abstract_match[1].split("\n\n## ")[0] if len(abstract_match) > 1 else "Systematic Literature Review."

        exporter = LaTeXExporterService(vault_manager)
        papers_data = _paper_data()
        bib_code = exporter.generate_bibtex(papers_data, manuscript_content=content)

        # Ensure exports directory exists in vault
        exports_dir = os.path.join(vault_manager.vault_path, "04_Drafts", "exports")
        os.makedirs(exports_dir, exist_ok=True)

        if venue == "ALL":
            bundle = exporter.export_multi_venue_bundle(
                title, authors, abstract, content, author_details=author_details
            )
            for v_key, v_code in bundle.items():
                with open(os.path.join(exports_dir, f"{clean_filename.replace('.md', '')}_{v_key}.tex"), "w", encoding="utf-8") as f:
                    f.write(v_code)
            with open(os.path.join(exports_dir, "references.bib"), "w", encoding="utf-8") as f:
                f.write(bib_code)
            return {
                "success": True,
                "filename": clean_filename,
                "venue": "ALL",
                "bundle": bundle,
                "bib_code": bib_code
            }

        selected_venue = venue or "NeurIPS"
        profile = VENUE_PROFILES.get(selected_venue)
        tex_code = exporter.markdown_to_venue_latex(
            selected_venue,
            title,
            authors,
            abstract,
            content,
            author_details=author_details,
            anonymize=profile.anonymized_review if profile else None,
        )

        # Save vault copy
        with open(os.path.join(exports_dir, f"{clean_filename.replace('.md', '')}_{selected_venue}.tex"), "w", encoding="utf-8") as f:
            f.write(tex_code)
        with open(os.path.join(exports_dir, "references.bib"), "w", encoding="utf-8") as f:
            f.write(bib_code)

        return {
            "success": True,
            "filename": clean_filename,
            "venue": selected_venue,
            "tex_filename": f"{clean_filename.replace('.md', '')}_{selected_venue}.tex",
            "bib_filename": "references.bib",
            "tex_code": tex_code,
            "bib_code": bib_code
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/export-venue-pdf")
def export_venue_pdf(filename: str = Query(...), venue: str = Query("IEEEtran")):
    """Compiles LaTeX into PDF using local pdflatex and returns application/pdf binary download."""
    from fastapi.responses import Response
    from services.latex_exporter import LaTeXExporterService
    try:
        clean_filename = os.path.basename(filename.strip().replace(" ", ""))
        if not clean_filename.endswith(".md"): clean_filename += ".md"

        draft = vault_manager.read_markdown("drafts", clean_filename)
        if not draft:
            raise HTTPException(status_code=404, detail="Manuscript draft not found")

        content = draft.get("content", "")
        meta = draft.get("frontmatter", {}) or draft.get("metadata", {})
        title = meta.get("title", clean_filename.replace(".md", "").replace("_", " ").title())
        authors = meta.get("authors") or ["Aryaman Singh Dev"]
        author_details = {
            "affiliation": meta.get("affiliation") or "Pennsylvania State University",
            "email": meta.get("email") or "asd5520@psu.edu",
        }


        abstract_match = re.search(r'#+\s*(?:\d+[\.\s]*)?(?:Executive\s+)?Abstract\n+([\s\S]*?)(?=\n+#|\Z)', content, re.IGNORECASE)
        abstract = abstract_match.group(1).strip() if abstract_match else "Systematic Literature Review."

        papers_data = _paper_data()
        exporter = LaTeXExporterService(vault_manager)
        bib_code = exporter.generate_bibtex(papers_data, manuscript_content=content)
        selected_venue = venue or "IEEEtran"
        profile = VENUE_PROFILES.get(selected_venue)
        tex_code = exporter.markdown_to_venue_latex(
            selected_venue,
            title,
            authors,
            abstract,
            content,
            author_details=author_details,
            anonymize=profile.anonymized_review if profile else None,
        )
        tex_report = pdf_qa.inspect_tex(tex_code, profile=profile.model_dump() if profile else None)
        if tex_report["errors"]:
            raise HTTPException(status_code=422, detail={"stage": "tex_qa", "errors": tex_report["errors"]})

        fact_audit = fact_checker.audit_document(content, source_records=_source_records())
        bibliography_report = fact_checker.validate_bibliography(content, bib_code)
        peer_review = meta.get("peer_review", {}) if isinstance(meta, dict) else {}
        if isinstance(peer_review, str):
            import ast
            try:
                peer_review = ast.literal_eval(peer_review)
            except Exception:
                peer_review = {}
        run_id = f"draft-{filename.replace('.md', '')}"
        synthetic_val = meta.get("synthetic", False)
        synthetic = synthetic_val.lower() in ("true", "1") if isinstance(synthetic_val, str) else bool(synthetic_val)

        manifest = RunManifest(
            run_id=run_id,
            topic=str(meta.get("topic", title)),
            canonical_venue=selected_venue,
            venue_cycle=profile.cycle if profile else None,
            synthetic=synthetic,
        )
        decision = release_controller.evaluate(
            manifest=manifest,
            fact_audit=fact_audit,
            bibliography_report=bibliography_report,
            qa_report={"status": "passed", "errors": []},
            peer_review=peer_review,
            synthetic=synthetic,
        )
        print("BUILD DECISION STATUS:", decision.status)
        print("BUILD DECISION ERRORS:", decision.errors)
        pdf_bytes = exporter.compile_pdflatex(
            tex_code,
            bib_code=bib_code,
            allow_package_fallback=True
        )

        if not pdf_bytes:
            log_tail = getattr(exporter, "last_build_log", "")[-1000:]
            raise HTTPException(status_code=500, detail=f"PDF compilation failed or pdflatex encountered an error.\n{log_tail}")

        exports_dir = os.path.join(vault_manager.vault_path, "04_Drafts", "exports")
        os.makedirs(exports_dir, exist_ok=True)
        pdf_path = os.path.join(exports_dir, f"{filename.replace('.md', '')}_{venue}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        # Execute Checkmate audit
        report = checkmate_verifier.audit_pdf(
            pdf_path,
            manuscript_markdown=content,
            venue_key=venue,
            tex_source=tex_code,
            package_fallback_used=exporter.last_compile_used_package_fallback,
            evidence_report=_fact_check_draft(content),
        )
        if report.get("checkmate_passed"):
            meta["checkmate_score"] = str(report.get("score", 100.0))
            meta["checkmate_status"] = "PASSED"
            meta["checkmate_date"] = report.get("certificate", {}).get("timestamp", "")
            vault_manager.save_markdown("drafts", filename, content, frontmatter=meta)

        headers = {
            "Content-Disposition": f'attachment; filename="{filename.replace(".md", "")}_{venue}.pdf"'
        }
        return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"TRACEBACK: {tb}")

@app.get("/api/vault/peer-review")
def get_peer_review(filename: str = Query(...)):
    """Returns automated conference peer review audit report and scores for a draft manuscript."""
    try:
        draft = vault_manager.read_markdown("drafts", filename)
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        meta = draft.get("frontmatter", {}) or draft.get("metadata", {})
        peer_review = meta.get("peer_review", {
            "schema_valid": False,
            "overall_decision": "REJECT",
            "scores": {},
            "key_strengths": [],
            "fatal_weaknesses": ["No structured peer-review audit is available."],
            "required_revisions": ["Run the peer-review audit before release."],
        })
        return {
            "success": True,
            "filename": filename,
            "peer_review": peer_review
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/research/topics")
def get_curated_topics():
    """Returns curated high-impact academic research topics for systematic reviews."""
    try:
        from services.topic_recommender import TopicRecommenderService
        recommender = TopicRecommenderService()
        return {
            "success": True,
            "topics": recommender.list_curated_topics()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/harness/state")
def get_harness_state():
    """Returns the Prime Agent harness durable memory state and trajectory telemetry."""
    try:
        from harness.continual_memory import ContinualMemoryManager
        memory = ContinualMemoryManager()
        return {
            "success": True,
            "state": memory.state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_agent_pipeline_sync(topic: str, project_id: str, loop: asyncio.AbstractEventLoop):
    """Runs the research pipeline synchronously in a separate thread and pushes logs to async queue."""
    def log_callback(log_data: Dict[str, Any]):
        # Push log data to queue via thread-safe call
        asyncio.run_coroutine_threadsafe(
            log_queues[project_id].put(log_data),
            loop
        )

    try:
        orchestrator.run_research(topic, log_callback)
    except Exception as e:
        # Push error log
        import time
        error_log = {
            "projectId": project_id,
            "timestamp": time.time(),
            "stage": "Error",
            "agent": "System",
            "message": f"Execution failed with exception: {str(e)}",
            "data": {"success": False}
        }
        asyncio.run_coroutine_threadsafe(
            log_queues[project_id].put(error_log),
            loop
        )
    finally:
        # Push sentinel None to indicate end of stream
        asyncio.run_coroutine_threadsafe(
            log_queues[project_id].put(None),
            loop
        )

@app.post("/api/research/start")
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Triggers the agent research pipeline and returns a streamable project ID."""
    import time
    project_id = f"proj_{int(time.time())}"

    # Initialize async queue for this project
    log_queues[project_id] = asyncio.Queue()

    # Get current event loop to pass to thread
    loop = asyncio.get_running_loop()

    # Run the orchestrator in a background thread so we don't block FastAPI
    thread = threading.Thread(
        target=run_agent_pipeline_sync,
        args=(request.topic, project_id, loop)
    )
    thread.daemon = True
    thread.start()

    return {"status": "started", "project_id": project_id}

@app.get("/api/research/stream/{project_id}")
async def stream_research_logs(project_id: str):
    """Server-Sent Events endpoint streaming real-time agent debate logs."""
    if project_id not in log_queues:
        raise HTTPException(status_code=404, detail="Active project stream not found")

    async def event_generator():
        queue = log_queues[project_id]
        try:
            while True:
                log_data = await queue.get()
                if log_data is None:  # Sentinel reached, end stream
                    yield "event: end\ndata: EOF\n\n"
                    break

                # Format SSE chunk
                # double newline is required to flush the buffer
                yield f"data: {json.dumps(log_data)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            # Clean up queue when client disconnects or stream ends
            if project_id in log_queues:
                del log_queues[project_id]

    return StreamingResponse(event_generator(), media_type="text/event-stream")


class MetaReviewRequest(BaseModel):
    filename: str
    target_venue: Optional[str] = "IEEEtran"
    target_length: Optional[str] = "full_journal"
    save_to_vault: Optional[bool] = True


@app.get("/api/vault/drafts")
def list_vault_drafts():
    """Lists all available markdown drafts in vault/04_Drafts with metadata."""
    drafts = []
    files = vault_manager.list_files("drafts")
    for item in files:
        fname = item["filename"] if isinstance(item, dict) else item
        if fname.endswith(".md"):
            try:
                doc = vault_manager.read_markdown("drafts", fname)
                meta = doc.get("frontmatter", {}) or {}
                content = doc.get("content", "")
                words = len(content.split())
                citations = len(set(re.findall(r'\[\[([^\]]+)\]\]', content)))
                tables = len(re.findall(r'\\begin\{tabular\}', content))
                equations = len(re.findall(r'\\begin\{equation\}|\$\$', content))
                drafts.append({
                    "filename": fname,
                    "title": meta.get("title", fname.replace(".md", "").replace("_", " ").title()),
                    "target_venue": meta.get("target_venue", "IEEEtran"),
                    "target_length": meta.get("target_length", "full_journal"),
                    "words": words,
                    "citations": citations,
                    "tables": tables,
                    "equations": equations,
                    "status": meta.get("status", "draft"),
                    "frontmatter": meta
                })
            except Exception:
                continue
    return {"drafts": drafts}


def run_meta_review_sync(filename: str, target_venue: str, target_length: str, save_to_vault: bool, project_id: str, loop: asyncio.AbstractEventLoop):
    def log_callback(stage: str, agent: str, message: str, data: Optional[Dict[str, Any]] = None):
        log_entry = {
            "projectId": project_id,
            "timestamp": int(time.time() * 1000),
            "stage": stage,
            "agent": agent,
            "message": message,
            "data": data
        }
        if project_id in log_queues:
            asyncio.run_coroutine_threadsafe(
                log_queues[project_id].put(log_entry),
                loop
            )

    try:
        meta, content = vault_manager.read_markdown("drafts", filename)
        result = meta_review_council.run_alignment_cycle(
            draft_content=content,
            target_venue=target_venue,
            target_length=target_length,
            log_callback=log_callback,
            is_dry_run=orchestrator.is_dry_run
        )

        if save_to_vault and result.get("success"):
            updated_meta = dict(meta)
            updated_meta.update({
                "target_venue": target_venue,
                "target_length": target_length,
                "tier_2_meta_reviewed": True,
                "meta_review_decision": result.get("decision", "STRONG ACCEPT"),
                "citations_count": result.get("final_citations", 0),
                "words_count": result.get("final_words", 0)
            })
            vault_manager.save_markdown("drafts", filename, result["revised_draft"], frontmatter=updated_meta)
            log_callback("Storage", "Cross-Venue Publisher & Sanitizer", f"Saved revised release manuscript to vault/04_Drafts/{filename}")

    except Exception as e:
        log_callback("Error", "Meta-Review Council Chair", f"Tier 2 alignment error: {str(e)}")
    finally:
        if project_id in log_queues:
            asyncio.run_coroutine_threadsafe(
                log_queues[project_id].put(None),
                loop
            )


@app.post("/api/research/meta-review")
async def start_meta_review(request: MetaReviewRequest, background_tasks: BackgroundTasks):
    """Triggers the Tier 2 Meta-Review and Cross-Venue Alignment Council."""
    project_id = f"meta_{int(time.time())}"
    log_queues[project_id] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    thread = threading.Thread(
        target=run_meta_review_sync,
        args=(request.filename, request.target_venue, request.target_length, request.save_to_vault, project_id, loop)
    )
    thread.daemon = True
    thread.start()

    return {"status": "started", "project_id": project_id}


@app.get("/api/research/meta-review/stream/{project_id}")
async def stream_meta_review_logs(project_id: str):
    """Server-Sent Events endpoint streaming real-time Tier 2 meta-review logs."""
    if project_id not in log_queues:
        raise HTTPException(status_code=404, detail="Active meta-review stream not found")

    async def event_generator():
        queue = log_queues[project_id]
        try:
            while True:
                log_data = await queue.get()
                if log_data is None:
                    yield "event: end\ndata: EOF\n\n"
                    break
                yield f"data: {json.dumps(log_data)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            if project_id in log_queues:
                del log_queues[project_id]

    return StreamingResponse(event_generator(), media_type="text/event-stream")

from services.o1a_tracker import O1AEvidenceTrackerService
from services.latex_exporter import VENUE_SPECS

o1a_tracker = O1AEvidenceTrackerService(vault_manager)

@app.get("/api/venues")
def get_venue_specs():
    """Returns technical specs and pinned release profiles for target venues."""
    return {
        "venue_order": list(SUPPORTED_VENUES),
        "venues": VENUE_SPECS,
        "release_profiles": {k: v.model_dump() for k, v in VENUE_PROFILES.items()},
    }


# ─────────────────────────────────────────────────────────────────────────────
# VENUE ADVISOR AGENT ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/venues/recommend")
def recommend_venues(request: VenueRecommendRequest):
    """
    Venue Advisor Agent: Recommends publication venues ranked by topic fit,
    user profile match, acceptance probability, and O-1A criterion value.
    """
    try:
        portfolio = user_profile_service.get_portfolio_summary()
        result = venue_advisor_agent.recommend(
            title=request.title,
            abstract=request.abstract,
            topic_keywords=request.topic_keywords,
            portfolio=portfolio,
        )
        return {"success": True, **result}
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"Venue advisor error: {traceback.format_exc()}")


@app.get("/api/user/profile")
def get_user_profile():
    """Returns the current user's publication profile for venue matching."""
    try:
        profile = user_profile_service.load()
        return {"success": True, "profile": profile}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/user/profile")
def update_user_profile(update: UserProfileUpdate):
    """Updates the user's publication profile. Merges with existing values."""
    try:
        profile = user_profile_service.load()
        updates = update.model_dump(exclude_none=True)
        profile.update(updates)
        saved = user_profile_service.save(profile)
        return {"success": True, "profile": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/venues/knowledge")
def get_venue_knowledge():
    """Returns the full venue knowledge base used by the advisor agent."""
    from agents.venue_advisor import VENUE_KNOWLEDGE
    return {"success": True, "venues": VENUE_KNOWLEDGE}

@app.get("/api/o1a/audit")
def get_o1a_audit():
    """Reports documented portfolio evidence; does not determine immigration eligibility."""
    drafts = vault_manager.list_files("drafts")
    manuscripts = []
    for d in drafts:
        meta = vault_manager.read_markdown("drafts", d["filename"])
        if meta and meta.get("frontmatter"):
            manuscripts.append({
                "id": d["filename"].replace(".md", ""),
                "title": meta["frontmatter"].get("title", d["filename"]),
                "venue": meta["frontmatter"].get("venue", "IEEE/ACM Journal"),
                "fact_check_score": float(meta["frontmatter"].get("fact_check_score", 0.0)),
                "citations": int(meta["frontmatter"].get("citations", 0)),
                "peer_review": meta["frontmatter"].get("peer_review")
            })

    audit_result = o1a_tracker.audit_o1a_readiness(manuscripts)
    dossier_md = o1a_tracker.generate_legal_dossier_markdown(manuscripts)
    audit_result["legal_dossier_markdown"] = dossier_md
    return audit_result

@app.get("/api/vault/system-error-ledger")
def get_system_error_ledger():
    """Returns the persistent System Error Ledger and quality prevention rules."""
    return {
        "success": True,
        "ledger": error_ledger_service.get_ledger_summary()
    }

@app.get("/api/harness/status")
def get_prime_harness_status():
    """Returns operational telemetry for Prime Agent Harness infrastructure."""
    from harness.prime_harness import prime_agent_harness
    return {"success": True, **prime_agent_harness.get_harness_status()}

if __name__ == "__main__":
    import uvicorn
    # Read configuration from environment loaded via python-dotenv
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"Starting uvicorn server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
