"""Workbench endpoints for the optional OpenResearch adapter."""
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.openresearch import OpenResearchError, OpenResearchService

router = APIRouter(prefix="/api/openresearch", tags=["OpenResearch"])
service = OpenResearchService()


class DiscoveryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    strategy: Literal["keyword", "embedding"] = "keyword"
    limit: int = Field(default=10, ge=1, le=50)


def invoke(operation, *args):
    try:
        return operation(*args)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except OpenResearchError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/status")
def status():
    return service.status()


@router.post("/discover")
def discover(request: DiscoveryRequest):
    return {"papers": invoke(service.discover, request.query, request.strategy, request.limit)}


@router.get("/projects")
def projects():
    return {"projects": invoke(service.projects)}


@router.get("/projects/{project_id}")
def project(project_id: str):
    return invoke(service.project, project_id)
