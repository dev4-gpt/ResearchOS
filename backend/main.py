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

@app.get("/api/health")
def health_check():
    gemini_key = bool(os.getenv("GEMINI_API_KEY"))
    nim_key = bool(os.getenv("NVIDIA_NIM_API_KEY") or os.getenv("NVIDIA_API_KEY"))
    return {
        "status": "healthy",
        "gemini_api_configured": gemini_key,
        "nvidia_nim_configured": nim_key,
        "vault_path": vault_manager.vault_path,
        "is_dry_run": not (gemini_key or nim_key)
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
    """Performs real-time citation and grounding audit on any vault file."""
    try:
        data = vault_manager.read_markdown(category, filename)
        content = data.get("content", "")
        report = fact_checker.audit_document(content)
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

@app.get("/api/vault/export-latex")
def export_latex(filename: str = "review_systematic_review_meta_taxonomy_of_generative_ai_i.md"):
    """Generates compilable IEEEtran LaTeX and BibTeX from a vault manuscript draft."""
    try:
        from services.latex_exporter import LaTeXExporterService
        exporter = LaTeXExporterService(vault_manager)
        
        draft = vault_manager.read_markdown("drafts", filename)
        title = draft["frontmatter"].get("title", "Systematic Review Manuscript")
        authors = draft["frontmatter"].get("authors", ["Dr. Senior Principal Researcher", "ResearchingOS Council"])
        content = draft["content"]
        
        abstract_match = content.split("## Executive Abstract\n\n")
        abstract = abstract_match[1].split("\n\n## ")[0] if len(abstract_match) > 1 else "Systematic Review of Enterprise Generative AI."
        
        tex_code = exporter.markdown_to_ieeetran(title, authors, abstract, content)
        
        paper_files = vault_manager.list_files("papers")
        papers_data = [vault_manager.read_markdown("papers", p["filename"]) for p in paper_files]
        bib_code = exporter.generate_bibtex(papers_data)
        
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
        authors = frontmatter.get("authors", ["Penn State AI Collaborator", "ResearchingOS Council"])
        
        abstract_match = content.split("## Executive Abstract\n\n")
        abstract = abstract_match[1].split("\n\n## ")[0] if len(abstract_match) > 1 else "Systematic Literature Review."
        
        exporter = LaTeXExporterService(vault_manager)
        paper_files = vault_manager.list_files("papers")
        papers_data = [vault_manager.read_markdown("papers", p["filename"]) for p in paper_files]
        bib_code = exporter.generate_bibtex(papers_data)

        if venue == "ALL":
            bundle = exporter.export_multi_venue_bundle(title, authors, abstract, content)
            return {
                "success": True,
                "filename": filename,
                "venue": "ALL",
                "bundle": bundle,
                "bib_code": bib_code
            }

        tex_code = exporter.markdown_to_venue_latex(venue or "NeurIPS", title, authors, abstract, content)
        return {
            "success": True,
            "filename": filename,
            "venue": venue,
            "tex_filename": f"{filename.replace('.md', '')}_{venue}.tex",
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
        draft = vault_manager.get_file("drafts", filename)
        if not draft:
            raise HTTPException(status_code=404, detail="Manuscript draft not found")

        content = draft.get("content", "")
        meta = draft.get("metadata", {})
        title = meta.get("title", filename.replace(".md", "").replace("_", " ").title())
        authors = ["ResearchingOS Academic Council", "The Pennsylvania State University"]
        abstract = "Systematic review and empirical meta-analysis generated by ResearchingOS Multi-Agent Engine."

        papers = vault_manager.list_files("papers")
        exporter = LaTeXExporterService(vault_manager)
        bib_code = exporter.generate_bibtex(papers)
        tex_code = exporter.markdown_to_venue_latex(venue or "IEEEtran", title, authors, abstract, content)

        pdf_bytes = exporter.compile_pdflatex(tex_code, bib_code)
        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="PDF compilation failed or pdflatex encountered an error.")

        pdf_filename = f"{filename.replace('.md', '')}_{venue}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{pdf_filename}"'}
        )
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

if __name__ == "__main__":
    import uvicorn
    # Read configuration from environment loaded via python-dotenv
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"Starting uvicorn server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
