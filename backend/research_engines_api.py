"""Read-only inspection of engine runs. No remote execution or publication endpoint."""
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from services import research_engines as engines

router = APIRouter(prefix='/api/research-engines', tags=['Research engines'])


def run_path(run_id):
    try:
        path = engines.safe_run(engines.RUNS, run_id)
        if not path.is_dir(): raise ValueError('Run not found')
        return path
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


def read_record(path, name):
    file = path / name
    if file.is_symlink() or not file.resolve().is_relative_to(path.resolve()):
        raise ValueError('Unsafe record path')
    if file.stat().st_size > 8 * 1024 * 1024:
        raise ValueError('Record too large')
    return json.loads(file.read_text())


@router.get('/status')
def status():
    return engines.status()


@router.get('/workflows')
def workflows():
    from services.research_workflow import WORKFLOWS
    result = []
    for record in sorted(WORKFLOWS.glob('*/workflow.json'), reverse=True)[:100]:
        try:
            root = engines.safe_run(WORKFLOWS, record.parent.name)
            result.append(read_record(root, 'workflow.json'))
        except (OSError, ValueError):
            continue
    return {'workflows': result}


@router.get('/runs')
def list_runs():
    runs = []
    for path in sorted(engines.RUNS.glob('*/summary.json'), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            root = run_path(path.parent.name)
            if path.is_symlink(): continue
            row = read_record(root, 'summary.json')
            row['verification'] = engines.verify_run(root)
            runs.append(row)
        except (OSError, ValueError, HTTPException):
            continue
    return {'runs': runs}


@router.get('/runs/{run_id}')
def inspect_run(run_id: str):
    path = run_path(run_id)
    try:
        return {'summary': read_record(path, 'summary.json'),
                'verification': engines.verify_run(path),
                'artifacts': read_record(path, 'artifacts.json')}
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=409, detail='Run incomplete or unreadable') from exc


@router.get('/runs/{run_id}/artifact', response_class=PlainTextResponse)
def artifact(run_id: str, name: str):
    path = run_path(run_id)
    try:
        manifest = read_record(path, 'artifacts.json')
        target = path / name
        if name not in manifest or target.is_symlink() or not target.resolve().is_relative_to(path.resolve()):
            raise HTTPException(status_code=404, detail='Unknown artifact')
        if target.stat().st_size > 1024 * 1024:
            raise HTTPException(status_code=413, detail='Artifact too large for inline viewing')
        body = target.read_bytes()
        if engines.digest(body) != manifest[name]:
            raise HTTPException(status_code=409, detail='Artifact hash mismatch')
        return body.decode('utf-8')
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=409, detail='Artifact unreadable') from exc
