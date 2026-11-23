"""Read-only writer execution and review status. No model calls from HTTP endpoints."""
from fastapi import APIRouter, HTTPException
from services import paperorchestra as writer

router = APIRouter(prefix='/api/paperorchestra', tags=['PaperOrchestra'])


@router.get('/jobs')
def jobs():
    result = []
    for p in sorted(writer.JOBS.glob('*/manifest.json')):
        try:
            m = writer.read_job(p.parent.name)
            result.append({k: m[k] for k in ('id', 'status', 'commit', 'publication_eligible', 'note')})
        except (OSError, ValueError, KeyError):
            result.append({'id': p.parent.name, 'status': 'integrity_failed', 'commit': '',
                           'publication_eligible': False, 'note': 'Job manifest or artifacts are unavailable or changed.'})
    return {'jobs': result}


@router.get('/jobs/{job_id}')
def job(job_id: str):
    try:
        return writer.read_job(job_id)
    except (OSError, ValueError, KeyError) as exc:
        raise HTTPException(status_code=409, detail='Job missing, incomplete or changed') from exc
