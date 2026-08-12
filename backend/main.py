import os
import json
import asyncio
import threading
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
from services.venue_profiles import VENUE_PROFILES
from services.evidence_ledger import EvidenceLedger
from services.user_profile import UserProfileService
from agents.venue_advisor import VenueAdvisorAgent
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

# In-memory log store for streaming active research runs
# key: project_id, value: asyncio.Queue containing log dicts
log_queues: Dict[str, asyncio.Queue] = {}

class ResearchRequest(BaseModel):
    topic: str

class SaveFileRequest(BaseModel):
    category: str
    filename: str
    content: str
    frontmatter: Dict[str, Any]

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
        return {"status": "success", "saved_path": path}
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

@app.get("/api/vault/export-latex")
def export_latex(filename: str = "review_systematic_review_meta_taxonomy_of_generative_ai_i.md"):
    """Generates compilable IEEEtran LaTeX and BibTeX from a vault manuscript draft."""
    try:
        from services.latex_exporter import LaTeXExporterService
        exporter = LaTeXExporterService(vault_manager)
        
        draft = vault_manager.read_markdown("drafts", filename)
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
            "filename": filename,
            "tex_filename": filename.replace(".md", "_IEEEtran.tex"),
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
        doc_data = vault_manager.read_markdown("drafts", filename)
        content = doc_data.get("content", "")
        frontmatter = doc_data.get("frontmatter", {})
        title = frontmatter.get("title", filename.replace(".md", ""))
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
                with open(os.path.join(exports_dir, f"{filename.replace('.md', '')}_{v_key}.tex"), "w", encoding="utf-8") as f:
                    f.write(v_code)
            with open(os.path.join(exports_dir, "references.bib"), "w", encoding="utf-8") as f:
                f.write(bib_code)
            return {
                "success": True,
                "filename": filename,
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
        with open(os.path.join(exports_dir, f"{filename.replace('.md', '')}_{selected_venue}.tex"), "w", encoding="utf-8") as f:
            f.write(tex_code)
        with open(os.path.join(exports_dir, "references.bib"), "w", encoding="utf-8") as f:
            f.write(bib_code)

        return {
            "success": True,
            "filename": filename,
            "venue": selected_venue,
            "tex_filename": f"{filename.replace('.md', '')}_{selected_venue}.tex",
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
        draft = vault_manager.read_markdown("drafts", filename)
        if not draft:
            raise HTTPException(status_code=404, detail="Manuscript draft not found")

        content = draft.get("content", "")
        meta = draft.get("frontmatter", {}) or draft.get("metadata", {})
        title = meta.get("title", filename.replace(".md", "").replace("_", " ").title())
        authors = meta.get("authors", [])
        author_details = {
            "affiliation": meta.get("affiliation", ""),
            "email": meta.get("email", ""),
        }
        abstract_match = content.split("## Executive Abstract\n\n")
        abstract = abstract_match[1].split("\n\n## ")[0] if len(abstract_match) > 1 else "Systematic Literature Review."

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
        if decision.status != "ready_for_human_signoff":
            raise HTTPException(status_code=422, detail={"stage": "release_gate", "errors": decision.errors, "checks": decision.checks})

        pdf_bytes = exporter.compile_pdflatex(
            tex_code,
            bib_code,
            allow_package_fallback=True,
        )
        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="PDF compilation failed or pdflatex encountered an error.")

        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_bytes)
            temp_pdf.flush()
            qa_report = pdf_qa.inspect_pdf(temp_pdf.name, profile=profile.model_dump() if profile else None)
            print("PDF QA REPORT:", qa_report)
        if qa_report["errors"]:
            print("QA REPORT ERRORS:", qa_report["errors"])
            raise HTTPException(status_code=422, detail={"stage": "pdf_qa", "errors": qa_report["errors"]})

        build_prefix = f"builds/{selected_venue}/v1"
        artifact_hashes = {
            "manuscript.tex": evidence_ledger.record_artifact(run_id, f"{build_prefix}/manuscript.tex", tex_code.encode("utf-8")),
            "references.bib": evidence_ledger.record_artifact(run_id, f"{build_prefix}/references.bib", bib_code.encode("utf-8")),
            "final.pdf": evidence_ledger.record_artifact(run_id, f"{build_prefix}/final.pdf", pdf_bytes),
        }
        evidence_ledger.record_artifact(
            run_id,
            f"{build_prefix}/build.log",
            getattr(exporter, "last_build_log", "").encode("utf-8"),
        )
        manifest.state = "VENUE_BUILD_VERIFIED"
        manifest.build_decision = decision.model_copy(update={"status": "ready_for_human_signoff"})
        manifest_dict = manifest.model_dump(mode="json") if hasattr(manifest, "model_dump") else json.loads(manifest.json())
        evidence_ledger.write_json(run_id, "manifest.json", manifest_dict)
        evidence_ledger.write_json(
            run_id,
            f"{build_prefix}/qa-report.json",
            {"tex": tex_report, "bibliography": bibliography_report, "pdf": qa_report, "artifact_sha256": artifact_hashes},
        )

        papers_data = _paper_data()

        pdf_bytes = exporter.compile_pdf(
            venue_key=venue,
            title=title,
            authors=authors,
            abstract=abstract,
            body_markdown=content,
            papers_data=papers_data,
            author_details=author_details
        )

        exports_dir = os.path.join(vault_manager.vault_path, "04_Drafts", "exports")
        os.makedirs(exports_dir, exist_ok=True)
        pdf_path = os.path.join(exports_dir, f"{filename.replace('.md', '')}_{venue}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        # 2. Run Checkmate audit
        report = verifier.audit_pdf(pdf_path, manuscript_markdown=content, venue_key=venue)

        # 3. Save audit metrics into document frontmatter
        meta["checkmate_score"] = str(report.get("score", "0.0"))
        meta["checkmate_status"] = "PASSED" if report.get("checkmate_passed") else "NEEDS_REMEDIATION"
        meta["checkmate_matrix"] = str(report.get("checks", {}))
        vault_manager.save_markdown("drafts", filename, content, meta)

        return {
            "status": "success",
            "filename": filename,
            "venue": venue,
            "checkmate": report
        }
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

from services.o1a_tracker import O1AEvidenceTrackerService
from services.latex_exporter import VENUE_SPECS

o1a_tracker = O1AEvidenceTrackerService(vault_manager)

@app.get("/api/venues")
def get_venue_specs():
    """Returns technical specs and pinned release profiles for target venues."""
    return {"venues": VENUE_SPECS, "release_profiles": {k: v.model_dump() for k, v in VENUE_PROFILES.items()}}


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

if __name__ == "__main__":
    import uvicorn
    # Read configuration from environment loaded via python-dotenv
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"Starting uvicorn server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
