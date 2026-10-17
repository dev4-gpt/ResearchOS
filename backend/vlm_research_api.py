from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.vlm_research import VLMResearchService

router = APIRouter(prefix='/api/research/projects/vlm-safety', tags=['VLM research task'])
service = VLMResearchService()


class PrepareRequest(BaseModel):
    sample_per_group: int = Field(default=30, ge=1, le=100)


@router.get('')
def status():
    return service.status()


@router.post('/prepare')
def prepare(request: PrepareRequest):
    try:
        return service.prepare(request.sample_per_group)
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(422, str(exc)) from exc
