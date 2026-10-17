from fastapi import APIRouter, HTTPException

from services.research_skills import ResearchSkillsService

router = APIRouter(prefix='/api/skills/research', tags=['Research skills'])
service = ResearchSkillsService()


@router.get('')
def research_skills(source: str | None = None, role: str | None = None, query: str | None = None):
    return {'summary': service.summary(), 'skills': service.list_skills(source, role, query)}


@router.get('/{skill_id}')
def research_skill(skill_id: str):
    skill = service.get_skill(skill_id)
    if not skill:
        raise HTTPException(404, 'Research skill not found')
    return skill
