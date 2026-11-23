"""Durable, bounded publisher queue; every accepted request has its own record."""
import inspect
import json
import os
from pathlib import Path
import threading
from services.durable_jobs import JobStore, DurableWorker


class PublisherReadinessJobManager:
    def __init__(self, service, path=None):
        self.service = service
        default = Path(__file__).resolve().parents[2] / 'runs/service/publisher.sqlite3'
        self.store = JobStore(path or os.getenv('RESEARCHINGOS_PUBLISHER_DB', str(default)))
        self.worker = DurableWorker(self.store, self._execute)
        self._lock = threading.Lock()

    def boot(self):
        with self._lock:
            self.worker.start()

    def start(self, target_filename=None, venues=None, trigger='manual', draft_snapshot=None):
        self.boot()
        payload = {'target_filename': target_filename, 'venues': venues, 'trigger': trigger}
        if draft_snapshot is not None:
            payload['draft_snapshot'] = draft_snapshot
        job = self.store.submit('publisher', payload)
        return self.get(job['id'])

    def _execute(self, kind, payload, emit):
        args = {k: payload[k] for k in ('target_filename', 'venues')}
        if 'progress_callback' in inspect.signature(self.service.run).parameters:
            args['progress_callback'] = emit
        if 'draft_snapshot' in payload:
            args['draft_snapshot'] = payload['draft_snapshot']
        return self.service.run(**args)

    def get(self, job_id=None):
        if not job_id:
            with self.store.connect() as db:
                row = db.execute('SELECT id FROM jobs ORDER BY created DESC LIMIT 1').fetchone()
                job_id = row['id'] if row else None
        job = self.store.get(job_id) if job_id else None
        if not job:
            return None
        payload = json.loads(job['payload'])
        payload.pop('draft_snapshot', None)
        report = json.loads(job['result']) if job['result'] else None
        # Read the most recent progress directly, independent of a browser subscription.
        with self.store.connect() as db:
            rows = list(db.execute('SELECT data FROM events WHERE job_id=? ORDER BY seq DESC LIMIT 250', (job_id,)))
        events = [json.loads(r['data']) for r in reversed(rows)]
        return {'job_id': job_id, 'status': job['status'], **payload,
                'started_at': job['created'], 'finished_at': job['updated'] if report else None,
                'error': job['error'], 'report': report, 'stage_events': events,
                'current_stage': events[-1].get('stage', 'prepare') if events else 'prepare',
                'progress': (report or {}).get('progress', {}),
                'run_id': (report or {}).get('run_id'), 'next_job_id': None}
