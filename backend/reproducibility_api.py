"""Read-only evidence access. Running repository code is restricted to the CLI."""
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from services.reproducibility import RUNS, status
from services.fact_checker import FactCheckerService

router = APIRouter(prefix="/api/reproducibility", tags=["Reproducibility"])


def run_path(run_id: str) -> Path:
    path = (RUNS / run_id).resolve()
    if path.parent != RUNS.resolve() or not path.is_dir():
        raise HTTPException(status_code=404, detail="Run not found")
    return path


@router.get("/status")
def get_status():
    return status()


@router.get("/runs")
def list_runs():
    runs = []
    for path in sorted(RUNS.glob("*/summary.json"), reverse=True):
        try:
            summary = json.loads(path.read_text())
            runs.append({"id": path.parent.name, "synthetic": summary["synthetic"],
                         "model": summary["model"], "arms": summary["arms"]})
        except (OSError, ValueError, KeyError):
            continue
    return {"runs": runs}


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    path = run_path(run_id)
    try:
        return {"id": run_id, "summary": json.loads((path / "summary.json").read_text()),
                "report": (path / "report.md").read_text(),
                "artifacts": json.loads((path / "artifacts.json").read_text())}
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=409, detail="Run is incomplete or unreadable") from exc


@router.get("/runs/{run_id}/artifact", response_class=PlainTextResponse)
def get_artifact(run_id: str, path: str):
    root = run_path(run_id)
    try:
        manifest = json.loads((root / "artifacts.json").read_text())
        target = (root / path).resolve()
        if path not in manifest or not target.is_relative_to(root) or target.suffix not in {".json", ".diff"}:
            raise HTTPException(status_code=404, detail="Text artifact not found")
        return target.read_text()[:200000]
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=409, detail="Artifact unreadable") from exc


class MeasurementClaim(BaseModel):
    arm: str
    metric: str
    value: float


@router.post("/runs/{run_id}/verify")
def verify(run_id: str, claim: MeasurementClaim):
    return FactCheckerService().verify_reproducibility_claim(run_path(run_id), claim.arm, claim.metric, claim.value)
