"""PaperOrchestra handoff/intake adapter. Generated manuscripts remain unverified.

Preparing a bundle does not call a model, compile TeX or publish a document.
"""
from __future__ import annotations
import json
from pathlib import Path
import re
import uuid

from services.research_engines import ROOT, digest, pinned_source, safe_run, write_json

JOBS = ROOT / 'runs/paperorchestra'
LIMIT = 50 * 1024 * 1024
REQUIRED_MATERIALS = ('idea_sparse.md', 'experimental_log.md')
ASSETS = {'.png', '.jpg', '.jpeg', '.pdf', '.json'}
TEMPLATE_EXTENSIONS = {'.tex', '.sty', '.cls', '.bst', '.bib', '.md', '.json'}
OUTPUT_EXTENSIONS = TEMPLATE_EXTENSIONS | ASSETS


def collect(directory, extensions):
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('Expected an ordinary directory')
    root = directory.resolve()
    files, total = {}, 0
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise ValueError('Symlinks are not accepted in manuscript bundles')
        if not p.is_file() or p.suffix.lower() not in extensions:
            continue
        total += p.stat().st_size
        if total > LIMIT:
            raise ValueError('Bundle exceeds the 50 MiB limit')
        files[p.relative_to(root).as_posix()] = p.read_bytes()
    return files


def persist(root, files):
    hashes = {}
    for name, body in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(body)
        hashes[name] = digest(body)
    return hashes


def job_path(job_id):
    path = safe_run(JOBS, job_id)
    if not path.is_dir():
        raise ValueError('PaperOrchestra job not found')
    return path


def read_job(job_id):
    root = job_path(job_id)
    p = root / 'manifest.json'
    if p.is_symlink() or p.stat().st_size > 1024 * 1024:
        raise ValueError('Unsafe job manifest')
    manifest = json.loads(p.read_text())
    for relative, expected in manifest['artifacts'].items():
        artifact = root / relative
        if artifact.is_symlink() or not artifact.resolve().is_relative_to(root.resolve()):
            raise ValueError('Unsafe artifact path')
        if digest(artifact.read_bytes()) != expected:
            raise ValueError('Artifact integrity failure: ' + relative)
    # An input hash or imported PDF does not establish scientific validity.
    manifest['publication_eligible'] = False
    return manifest


def prepare(materials, template, writer_model, reflection_model, cutoff):
    if not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', cutoff):
        raise ValueError('Cutoff must be YYYY-MM')
    if not writer_model.strip() or not reflection_model.strip():
        raise ValueError('Explicit writer and reflection model IDs are required')
    source, pin = pinned_source('paperorchestra')
    raw = collect(materials, {'.md', '.txt', '.json'} | ASSETS)
    for name in REQUIRED_MATERIALS:
        if not raw.get(name, b'').strip():
            raise ValueError('Missing nonempty material: ' + name)
    # Only expected materials and figure assets are passed to upstream, not a whole vault.
    raw = {name: body for name, body in raw.items() if name in REQUIRED_MATERIALS or name.startswith('figures/')}
    raw.setdefault('figures/info.json', b'[]\n')
    tex = collect(template, TEMPLATE_EXTENSIONS)
    for name in ('template.tex', 'guidelines.md'):
        if not tex.get(name, b'').strip():
            raise ValueError('Missing template file: ' + name)
    job_id = 'paperorchestra-' + uuid.uuid4().hex[:12]
    root = safe_run(JOBS, job_id)
    root.mkdir(parents=True)
    artifacts = persist(root, {'raw_materials/' + k: v for k, v in raw.items()})
    artifacts.update(persist(root, {'template/' + k: v for k, v in tex.items()}))
    argv = ['python', str(source / 'paper_writing_cli.py'),
            '--raw_materials_dir', str(root / 'raw_materials'),
            '--latex_template_dir', str(root / 'template'), '--output_dir', str(root / 'upstream_output'),
            '--writer_model_name', writer_model, '--reflection_model_name', reflection_model,
            '--research_cutoff', cutoff, '--use_plotting', 'false']
    manifest = {'id': job_id, 'status': 'prepared', 'upstream': pin['repository'], 'commit': pin['commit'],
                'writer_model': writer_model, 'reflection_model': reflection_model,
                'research_cutoff': cutoff, 'use_plotting': False, 'generation_executed': False,
                'publication_eligible': False, 'artifacts': artifacts, 'argv': argv,
                'note': 'Prepared handoff only. Run upstream in an isolated worker; import output for review.'}
    write_json(root / 'manifest.json', manifest)
    return manifest


def intake(job_id, output):
    manifest = read_job(job_id)
    files = collect(output, OUTPUT_EXTENSIONS)
    if not any(name.endswith('.tex') for name in files):
        raise ValueError('Expected LaTeX output; PDF alone is not sufficient')
    # Keep each import independently; never overwrite input evidence or prior drafts.
    prefix = 'intake-' + uuid.uuid4().hex[:12] + '/'
    manifest['artifacts'].update(persist(job_path(job_id), {prefix + k: v for k, v in files.items()}))
    manifest.update(status='awaiting_review', latest_intake=prefix, publication_eligible=False,
        note='Imported output is unverified. Citations, numerical claims, venue compliance and compilation require review.')
    # Import does not prove which software/model generated these files.
    manifest['generation_executed'] = False
    write_json(job_path(job_id) / 'manifest.json', manifest)
    return manifest
