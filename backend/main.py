import _langsmith_stub  # noqa: F401 -- must run before anything imports langchain_core; see ERR-097

import os
import re
import json
import hashlib
import time
import asyncio
import threading
import sys
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Request, Header
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
from services.access_control import OperatorAccess, origins, validate_configuration
from services.request_limits import RequestBodyLimit
from services.durable_jobs import JobStore, DurableWorker, JobConflict, QueueFull, TERMINAL, run_isolated_job
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, Field
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

@asynccontextmanager
async def app_lifespan(app):
    validate_configuration()
    job_worker.start()
    try:
        publisher_readiness_jobs.boot()
        yield
    finally:
        job_worker.stop()
        publisher_readiness_jobs.worker.stop()

app = FastAPI(lifespan=app_lifespan, title="ResearchingOS API", description="Backend server for multi-agent academic research council")
from openresearch_api import router as openresearch_router
app.include_router(openresearch_router)
from research_skills_api import router as research_skills_router
app.include_router(research_skills_router)
from vlm_research_api import router as vlm_research_router
app.include_router(vlm_research_router)
from reproducibility_api import router as reproducibility_router
app.include_router(reproducibility_router)
from research_engines_api import router as research_engines_router
app.include_router(research_engines_router)
from paperorchestra_api import router as paperorchestra_router
app.include_router(paperorchestra_router)

# Add CORS Middleware to connect with Vite React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestBodyLimit)
app.add_middleware(OperatorAccess)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[h.strip() for h in os.getenv(
    'RESEARCHINGOS_HOSTS', 'localhost,127.0.0.1,[::1]').split(',') if h.strip()])

@app.get('/api/session')
@app.post('/api/session')
def operator_session():
    return {'authenticated': True}


@app.delete('/api/session')
def operator_logout():
    return {'authenticated': False}

# Initialize service classes
vault_path = os.getenv("VAULT_PATH", "../vault")
vault_manager = VaultManager(vault_path)
if os.path.exists(vault_manager.vault_path):
    app.mount("/vault", StaticFiles(directory=vault_manager.vault_path, html=True), name="vault")
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

from services.feynman_service import FeynmanService
from services.autoresearch_loop import AutonomousResearchHarness
from services.fx_bridge import FXBridge
from services.fx_mcp_server import ResearchOSMCPServer
from services.evomap_autoresearch import IdeaForgeService
from services.voxcpm_service import VoiceControlParser, VoxCPMAudioService
from services.ecc_skill_loader import ECCSkillLoader
from services.academic_voice_linter import AcademicVoiceLinter
from services.conference_slides_service import ConferenceSlidesService
from services.diagram_generator import DiagramGeneratorService
from services.universal_skills import UniversalSkillsService

fx_bridge = FXBridge()
feynman_service = FeynmanService(vault_manager, fx_bridge=fx_bridge)
autoresearch_harness = AutonomousResearchHarness(vault_manager)
fx_mcp_server = ResearchOSMCPServer(vault_manager.vault_path)
evomap_service = IdeaForgeService(vault_manager)
voice_control_parser = VoiceControlParser()
voxcpm_audio_service = VoxCPMAudioService(vault_manager.vault_path)
ecc_skill_loader = ECCSkillLoader()
academic_voice_linter = AcademicVoiceLinter()
conference_slides_service = ConferenceSlidesService(vault_manager.vault_path)
diagram_generator_service = DiagramGeneratorService(vault_manager.vault_path)
universal_skills_service = UniversalSkillsService()

# SQLite is the source of truth; subscriptions never own jobs.
job_store = JobStore(os.getenv('RESEARCHINGOS_JOBS_DB', str(Path(vault_manager.vault_path).parent / 'runs/service/jobs.sqlite3')))
def launch_research_job(job_id):
    seconds = int(os.getenv('RESEARCHINGOS_RESEARCH_JOB_SECONDS', '900'))
    if not 1 <= seconds <= 1800:
        raise ValueError('Research job timeout must be 1..1800 seconds')
    command = [sys.executable, str(Path(__file__).with_name('research_job_worker.py')), job_id, str(seconds)]
    return run_isolated_job(command, seconds, env={**os.environ, 'RESEARCHINGOS_JOBS_DB': str(job_store.path.resolve())})


job_worker = DurableWorker(job_store, None, isolated_handler=launch_research_job)

class ResearchRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=4000)
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

class FeynmanAuditRequest(BaseModel):
    draft_filename: str
    code_path: Optional[str] = None

class FeynmanLitRequest(BaseModel):
    topic: Optional[str] = "Multi-Agent Systems"
    paper_names: Optional[List[str]] = None

class FeynmanReviewRequest(BaseModel):
    draft_filename: str
    venue: Optional[str] = "IEEEtran"

class FeynmanAutoresearchRequest(BaseModel):
    draft_filename: str
    venue: Optional[str] = "IEEEtran"
    max_iterations: Optional[int] = 3

class FXDispatchRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    timeout_sec: Optional[int] = 30

class FXMCPCallRequest(BaseModel):
    tool_name: str
    arguments: Optional[Dict[str, Any]] = None

class EvoMapForgeRequest(BaseModel):
    topic: str
    domain_b: Optional[str] = None
    count: Optional[int] = 2

class EvoMapPilotRequest(BaseModel):
    idea: Dict[str, Any]

class VoiceCommandRequest(BaseModel):
    text: str

class VoiceSynthesizeRequest(BaseModel):
    text: str
    persona: Optional[str] = "chairman"

class SlopAuditRequest(BaseModel):
    text: Optional[str] = None
    draft_filename: Optional[str] = None

class SlopHumanizeRequest(BaseModel):
    text: Optional[str] = None
    draft_filename: Optional[str] = None

class SlideDeckRequest(BaseModel):
    draft_filename: Optional[str] = None
    title: Optional[str] = None
    text: Optional[str] = None
    author: Optional[str] = "ResearchingOS Autonomous Academic Council"
    venue: Optional[str] = "IEEEtran / ACM Conference"

class DiagramGenerateRequest(BaseModel):
    title: Optional[str] = "ResearchingOS Multi-Agent Autonomous Council Pipeline"
    nodes: Optional[List[Dict[str, str]]] = None

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

@app.get('/api/ready')
def readiness_check():
    workers = {
        'research': bool(job_worker.thread and job_worker.thread.is_alive() and not job_worker.stopping.is_set()),
        'publisher': bool(publisher_readiness_jobs.worker.thread and publisher_readiness_jobs.worker.thread.is_alive()
                          and not publisher_readiness_jobs.worker.stopping.is_set()),
    }
    return JSONResponse(status_code=200 if all(workers.values()) else 503,
                        content={'ready': all(workers.values()), 'workers': workers})


@app.get('/api/operations')
def operations_snapshot():
    from services.operations import snapshot
    workers = json.loads(readiness_check().body)['workers']
    return snapshot(
        {'research': job_store, 'publisher': publisher_readiness_jobs.store},
        {'vault': vault_manager.vault_path, 'research': job_store.path.parent,
         'publisher': publisher_readiness_jobs.store.path.parent},
        workers,
        backup_receipt=os.getenv('RESEARCHINGOS_BACKUP_RECEIPT'),
    )


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
    enqueue = request.category == 'drafts' and request.trigger_readiness
    try:
        saved = vault_manager.save_markdown(
            request.category, request.filename, request.content, request.frontmatter, with_snapshot=enqueue,
        )
    except Exception:
        raise HTTPException(500, 'Vault file could not be saved')
    if not enqueue:
        return {'status': 'success', 'saved_path': saved}

    path, snapshot = saved
    response: Dict[str, Any] = {'status': 'success', 'saved_path': path}
    try:
        response['readiness_job'] = publisher_readiness_jobs.start(
            target_filename=Path(path).name, trigger='draft_save', draft_snapshot=snapshot)
    except QueueFull:
        response['readiness_error'] = 'Draft saved. The publisher queue is full. Start readiness again when capacity is available.'
    except Exception:
        response['readiness_error'] = 'Draft saved. Publisher queue status could not be confirmed. Check publisher status before retrying.'
    return response

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
    if wait and os.getenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated') != 'local':
        raise HTTPException(422, 'Production publisher checks must use the durable queue')
    try:
        if wait:
            return publisher_readiness_service.run(target_filename=filename, venues=venues)
        job = publisher_readiness_jobs.start(target_filename=filename, venues=venues, trigger="manual")
        return JSONResponse(status_code=202, content={"success": True, "job": job})
    except QueueFull:
        raise HTTPException(429, 'Publisher queue is full', headers={'Retry-After': '30'})
    except Exception:
        raise HTTPException(500, 'Publisher readiness could not be started')

@app.get("/api/vault/publisher/readiness/status")
def get_publisher_readiness_status(job_id: Optional[str] = Query(None)):
    """Returns the current background readiness job and completed report, if available."""
    job = publisher_readiness_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="No publisher readiness job found")
    return {"success": True, "job": job}

@app.get("/api/vault/publisher/readiness/bundle")
def download_publisher_readiness_bundle(job_id: str = Query(..., min_length=1)):
    """Download the verified artifacts recorded by a completed publisher job."""
    job = publisher_readiness_jobs.get(job_id)
    if not job:
        raise HTTPException(404, "No publisher readiness job found")
    if job["status"] != "completed":
        raise HTTPException(409, "Publisher readiness job has not completed")

    report = job["report"] or {}
    if not report.get("artifact_manifest_sha256"):
        raise HTTPException(409, "Run publisher readiness again to create a verified bundle for this job")
    if not report.get("ready_count"):
        raise HTTPException(409, "No verified publish-ready artifacts are available for this job")

    try:
        archive = publisher_readiness_jobs.service.verified_bundle(report)
    except (OSError, KeyError, ValueError, TypeError, RuntimeError):
        raise HTTPException(409, "Publisher bundle failed integrity verification. Run publisher readiness again.")
    headers = {"Content-Disposition": "attachment; filename=researchingos-publish-ready-bundle.zip"}
    return Response(content=archive, media_type="application/zip", headers=headers)

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

        # release_controller.evaluate() is a fail-closed gate; it previously
        # ran here with a hardcoded {"status": "passed", "errors": []} qa_report
        # -- passed by construction regardless of the actual PDF, before the
        # PDF even existed. pdf_qa.inspect_pdf() already implements exactly the
        # {"status", "errors"} shape this gate expects but was never called
        # anywhere. Run it on the real compiled PDF now that one exists.
        qa_report = pdf_qa.inspect_pdf(pdf_path, profile=profile.model_dump() if profile else None)
        decision = release_controller.evaluate(
            manifest=manifest,
            fact_audit=fact_audit,
            bibliography_report=bibliography_report,
            qa_report=qa_report,
            peer_review=peer_review,
            synthetic=synthetic,
        )
        print("BUILD DECISION STATUS:", decision.status)
        print("BUILD DECISION ERRORS:", decision.errors)

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

def submit_research_job(kind, payload, key, prepare=None):
    try:
        job = job_store.submit(kind, payload, key, prepare=prepare)
    except JobConflict as exc:
        raise HTTPException(409, str(exc))
    except QueueFull as exc:
        raise HTTPException(429, str(exc), headers={'Retry-After': '30'})
    except FileNotFoundError:
        raise HTTPException(404, 'Draft not found')
    except ValueError as exc:
        raise HTTPException(422, str(exc))
    return {'status': job['status'], 'project_id': job['id']}


@app.post('/api/research/start', status_code=202)
def start_research(request: ResearchRequest, idempotency_key: str = Header(...)):
    return submit_research_job('research', request.model_dump(), idempotency_key)


@app.get('/api/research/jobs/{project_id}')
def research_job_status(project_id: str):
    job = job_store.get(project_id)
    if not job:
        raise HTTPException(404, 'Job not found')
    return {key: job[key] for key in ('id', 'kind', 'status', 'created', 'updated', 'error')}


@app.post('/api/research/jobs/{project_id}/cancel')
def cancel_research_job(project_id: str):
    if not job_store.get(project_id):
        raise HTTPException(404, 'Job not found')
    try:
        job_store.cancel(project_id)
    except JobConflict as exc:
        raise HTTPException(409, str(exc))
    return research_job_status(project_id)


async def durable_stream(project_id, request, after):
    if not job_store.get(project_id):
        raise HTTPException(404, 'Job not found')
    try:
        cursor = max(after, int(request.headers.get('last-event-id', '0')))
        if cursor < 0:
            raise ValueError()
    except ValueError:
        raise HTTPException(422, 'Invalid event cursor')

    async def events():
        nonlocal cursor
        while not await request.is_disconnected():
            batch = job_store.events(project_id, cursor)
            for event in batch:
                cursor = event['seq']
                yield f"id: {cursor}\ndata: {event['data']}\n\n"
            job = job_store.get(project_id)
            if job['status'] in TERMINAL and not job_store.events(project_id, cursor):
                yield 'event: end\ndata: ' + json.dumps({'status': job['status'], 'error': job['error']}) + '\n\n'
                return
            if not batch:
                yield ': heartbeat\n\n'
                await asyncio.sleep(1)
    return StreamingResponse(events(), media_type='text/event-stream',
                             headers={'Cache-Control': 'no-store', 'X-Accel-Buffering': 'no'})


@app.get('/api/research/stream/{project_id}')
async def stream_research_logs(project_id: str, request: Request, after: int = 0):
    return await durable_stream(project_id, request, after)


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


def execute_research_job(kind, payload, emit):
    if kind == 'research':
        result = orchestrator.run_research(payload['topic'], emit, target_venue=payload.get('target_venue'),
                                           target_length=payload.get('target_length'))
        if isinstance(result, dict) and result.get('success') is False:
            raise RuntimeError('Research pipeline reported failure')
        return
    if kind != 'meta-review':
        raise ValueError('Unknown job kind')
    def log_callback(stage, agent, message, data=None):
        emit({'timestamp': int(time.time() * 1000), 'stage': stage,
              'agent': agent, 'message': message, 'data': data})
    doc = payload.get('draft_snapshot')
    if doc is None:
        raise ValueError('Legacy job has no frozen source draft; resubmit explicitly')
    result = meta_review_council.run_alignment_cycle(
        draft_content=doc.get('content', ''), target_venue=payload['target_venue'],
        target_length=payload['target_length'], log_callback=log_callback,
        is_dry_run=orchestrator.is_dry_run)
    if not result.get('success'):
        raise RuntimeError('Meta-review failed')
    if payload['save_to_vault']:
        meta = dict(doc.get('frontmatter', {}))
        meta.update(target_venue=payload['target_venue'], target_length=payload['target_length'],
                    tier_2_meta_reviewed=True, meta_review_decision=result.get('decision', 'REVIEW REQUIRED'),
                    citations_count=result.get('final_citations', 0), words_count=result.get('final_words', 0))
        stem = Path(payload['filename']).stem[:120]
        filename = f'{stem}__review_{uuid4().hex}.md'
        meta.update(source_draft=payload['filename'], source_sha256=hashlib.sha256(doc['content'].encode()).hexdigest())
        log_callback('Storage', 'Meta-Review', 'Saving a separate revision; publication review remains required')
        vault_manager.save_markdown('drafts', filename, result['revised_draft'], frontmatter=meta, create_only=True)
        log_callback('Storage', 'Meta-Review', 'Saved revised draft', {'draftFile': filename})


@app.post('/api/research/meta-review', status_code=202)
def start_meta_review(request: MetaReviewRequest, idempotency_key: str = Header(...)):
    def snapshot(payload):
        filename = vault_manager._clean_filename(payload['filename'])
        return {**payload, 'filename': filename,
                'draft_snapshot': vault_manager.read_markdown('drafts', filename, exact=True)}

    return submit_research_job('meta-review', request.model_dump(), idempotency_key, prepare=snapshot)


@app.get('/api/research/meta-review/stream/{project_id}')
async def stream_meta_review_logs(project_id: str, request: Request, after: int = 0):
    return await durable_stream(project_id, request, after)

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

# ---------------------------------------------------------------------------
# Feynman Research Assistant Endpoints (companion-inc/feynman)
# ---------------------------------------------------------------------------

@app.post("/api/feynman/audit")
def feynman_audit_endpoint(req: FeynmanAuditRequest):
    """Audits manuscript empirical claims against actual experiment code AST."""
    draft_name = req.draft_filename if req.draft_filename.endswith(".md") else f"{req.draft_filename}.md"
    try:
        doc = vault_manager.read_markdown("drafts", draft_name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Draft {draft_name} not found")
    content = doc.get("content", "")
    return feynman_service.audit_paper_against_code(content, code_dir_or_file=req.code_path)

@app.post("/api/feynman/lit")
def feynman_lit_endpoint(req: FeynmanLitRequest):
    """Synthesizes consensus, active debates, and open gaps across vault papers."""
    return feynman_service.synthesize_literature_matrix(topic=req.topic or "", paper_names=req.paper_names)

@app.post("/api/feynman/review")
def feynman_review_endpoint(req: FeynmanReviewRequest):
    """Performs simulated peer review triage with [BLOCKER], [MAJOR], [MINOR] tags."""
    draft_name = req.draft_filename if req.draft_filename.endswith(".md") else f"{req.draft_filename}.md"
    try:
        doc = vault_manager.read_markdown("drafts", draft_name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Draft {draft_name} not found")
    content = doc.get("content", "")
    return feynman_service.simulated_peer_review(content, venue=req.venue or "IEEEtran")

@app.post("/api/feynman/autoresearch")
def feynman_autoresearch_endpoint(req: FeynmanAutoresearchRequest):
    """Triggers Karpathy-style closed-loop manuscript hill-climbing optimization."""
    draft_name = req.draft_filename if req.draft_filename.endswith(".md") else f"{req.draft_filename}.md"
    return autoresearch_harness.optimize(
        draft_name, target_venue=req.venue or "IEEEtran", max_iterations=req.max_iterations or 3
    )

# ---------------------------------------------------------------------------
# Vercel Labs fx Agent Engine & MCP Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/fx/status")
def fx_status_endpoint():
    """Returns Vercel Labs fx engine installation status, execution mode, and capabilities."""
    return fx_bridge.get_status()

@app.post("/api/fx/dispatch")
def fx_dispatch_endpoint(req: FXDispatchRequest):
    """Dispatches an autonomous research query to the fx agent harness."""
    return fx_bridge.dispatch_research(
        prompt=req.prompt,
        context=req.context,
        timeout_sec=req.timeout_sec or 30,
    )

@app.get("/api/fx/mcp/tools")
def fx_mcp_tools_endpoint():
    """Lists MCP tool definitions exposed by ResearchingOS for external agents."""
    return {"tools": fx_mcp_server.get_tool_definitions()}

@app.post("/api/fx/mcp/call")
def fx_mcp_call_endpoint(req: FXMCPCallRequest):
    """Executes a ResearchingOS MCP tool call."""
    try:
        res = fx_mcp_server.call_tool(req.tool_name, req.arguments or {})
        return {"success": True, "result": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------------------------------------------------------
# EvoMap/AutoResearch Idea Forge & Pilot Gate Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/evomap/forge")
def evomap_forge_endpoint(req: EvoMapForgeRequest):
    """Generates cross-domain hypotheses with Tri-Critic review."""
    return {"ideas": evomap_service.forge_ideas(topic=req.topic, domain_b=req.domain_b, count=req.count or 2)}

@app.post("/api/evomap/pilot")
def evomap_pilot_endpoint(req: EvoMapPilotRequest):
    """Executes pilot validation gate on a candidate research hypothesis."""
    return evomap_service.run_pilot(req.idea)

@app.get("/api/evomap/negative-results")
def evomap_negative_results_endpoint(limit: int = Query(default=50, ge=1, le=500)):
    """Retrieves negative and falsified empirical outcomes ledger."""
    return {"negative_results": evomap_service.get_negative_results(limit=limit)}

# ---------------------------------------------------------------------------
# OpenBMB/VoxCPM Speech Synthesis & Voice Control Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/voice/command")
def voice_command_endpoint(req: VoiceCommandRequest):
    """Parses natural language speech-to-intent commands for hands-free control."""
    return voice_control_parser.parse_command(req.text)

@app.post("/api/voice/synthesize")
def voice_synthesize_endpoint(req: VoiceSynthesizeRequest):
    """Synthesizes speech audio using selected council persona voice."""
    return voxcpm_audio_service.synthesize_speech(req.text, persona=req.persona or "chairman")

@app.get("/api/voice/status")
def voice_status_endpoint():
    """Returns status of VoxCPM speech synthesis engine and persona voices."""
    return voxcpm_audio_service.get_engine_status()

# ---------------------------------------------------------------------------
# affaan-m/ECC Departmental Skills Catalog Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/ecc/skills")
def ecc_skills_endpoint(
    dept: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = Query(default=100, ge=1, le=300),
):
    """Lists departmental skills from affaan-m/ECC catalog."""
    return {
        "status": ecc_skill_loader.get_status(),
        "skills": ecc_skill_loader.list_skills(department=dept, query=query, limit=limit),
    }

@app.get("/api/ecc/skill/{name}")
def ecc_skill_detail_endpoint(name: str):
    """Retrieves complete content and metadata of a specific ECC skill."""
    skill = ecc_skill_loader.get_skill(name)
    if not skill:
        raise HTTPException(status_code=404, detail=f"ECC Skill '{name}' not found")
    return skill

@app.post("/api/ecc/sync")
def ecc_sync_endpoint():
    """Syncs vital core ECC skills directly to workspace .agents/skills/ecc/."""
    return ecc_skill_loader.sync_core_skills_to_workspace()

# ---------------------------------------------------------------------------
# Universal Skills, Academic Voice (Stop-Slop), Slides & Diagram Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/slop/audit")
def slop_audit_endpoint(req: SlopAuditRequest):
    """Audits text or draft manuscript for AI clichés, staging contrasts, and throat-clearing."""
    content = req.text
    if not content and req.draft_filename:
        filename = req.draft_filename if req.draft_filename.endswith(".md") else f"{req.draft_filename}.md"
        doc = vault_manager.read_markdown("drafts", filename)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Draft '{filename}' not found in vault")
        content = doc.get("content", "")
    if not content:
        raise HTTPException(status_code=400, detail="Either 'text' or 'draft_filename' must be provided")
    return academic_voice_linter.audit_prose(content)

@app.post("/api/slop/humanize")
def slop_humanize_endpoint(req: SlopHumanizeRequest):
    """Rewrites text or draft manuscript eliminating AI tells and restoring scholarly voice."""
    content = req.text
    if not content and req.draft_filename:
        filename = req.draft_filename if req.draft_filename.endswith(".md") else f"{req.draft_filename}.md"
        doc = vault_manager.read_markdown("drafts", filename)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Draft '{filename}' not found in vault")
        content = doc.get("content", "")
    if not content:
        raise HTTPException(status_code=400, detail="Either 'text' or 'draft_filename' must be provided")
    return academic_voice_linter.humanize_text(content)

@app.post("/api/slides/generate")
def slides_generate_endpoint(req: SlideDeckRequest):
    """Generates a zero-dependency 16:9 fixed-stage HTML slide deck from draft manuscript."""
    title = req.title or "Conference Slide Presentation"
    content = req.text
    if not content and req.draft_filename:
        filename = req.draft_filename if req.draft_filename.endswith(".md") else f"{req.draft_filename}.md"
        doc = vault_manager.read_markdown("drafts", filename)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Draft '{filename}' not found in vault")
        content = doc.get("content", "")
        title = doc.get("frontmatter", {}).get("title", filename)
    if not content:
        raise HTTPException(status_code=400, detail="Either 'text' or 'draft_filename' must be provided")
    return conference_slides_service.generate_deck_from_manuscript(
        draft_title=title,
        manuscript_text=content,
        author=req.author or "ResearchingOS Autonomous Academic Council",
        venue=req.venue or "IEEEtran / ACM Conference",
    )

@app.post("/api/diagram/generate")
def diagram_generate_endpoint(req: DiagramGenerateRequest):
    """Generates an editorial SVG architecture diagram for paper or dashboard."""
    return diagram_generator_service.generate_pipeline_diagram(
        title=req.title or "ResearchingOS Multi-Agent Autonomous Council Pipeline",
        nodes=req.nodes,
    )

@app.get("/api/skills/universal")
def universal_skills_endpoint(category: Optional[str] = None):
    """Lists universally installed skills across UI, design, anti-slop, slides, and diagrams."""
    return {
        "summary": universal_skills_service.get_summary(),
        "skills": universal_skills_service.list_universal_skills(category=category),
    }

@app.get("/api/skills/universal/{name}")
def universal_skill_detail_endpoint(name: str):
    """Retrieves full documentation and guidelines for a specific universally installed skill."""
    details = universal_skills_service.get_skill_details(name)
    if not details:
        raise HTTPException(status_code=404, detail=f"Skill '{name}' not found")
    return details


if __name__ == "__main__":
    import uvicorn
    # Read configuration from environment loaded via python-dotenv
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    frontend_port = int(os.getenv("FRONTEND_PORT", "3000"))
    print(f"Starting uvicorn server on http://{host}:{port}")
    print(f"Frontend (run separately): http://{host}:{frontend_port}")
    uvicorn.run("main:app", host=host, port=port, reload=False)
