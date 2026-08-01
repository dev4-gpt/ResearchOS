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
    return {
        "status": "healthy",
        "gemini_api_configured": bool(os.getenv("GEMINI_API_KEY")),
        "vault_path": vault_manager.vault_path,
        "is_dry_run": not bool(os.getenv("GEMINI_API_KEY"))
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
