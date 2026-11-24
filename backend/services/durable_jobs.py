"""Single-host durable work queue. Interrupted effects require operator reconciliation."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import logging
import os
from pathlib import Path
import sqlite3
import signal
import subprocess
import threading
import time
import uuid

TERMINAL = {'completed', 'failed', 'interrupted', 'cancelled'}


class JobConflict(ValueError):
    pass


class QueueFull(RuntimeError):
    pass


class JobExecutionFailure(RuntimeError):
    """An execution failure with a fixed, public diagnostic."""


def run_isolated_job(command, seconds, env=None):
    # The child watches stdin for supervisor death. Keep the pipe open until it exits.
    with subprocess.Popen(command, env=env, stdin=subprocess.PIPE, start_new_session=True,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as child:
        try:
            code = child.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
            raise JobExecutionFailure('Execution deadline exhausted; reconcile any provider calls before retrying')
    if code:
        message = {74: 'Provider quota exhausted; no automatic retry',
                   75: 'Provider call timed out or its outcome is uncertain; no automatic retry',
                   76: 'Spending configuration or budget blocked execution'}
        raise JobExecutionFailure(message.get(code, 'Execution failed; review diagnostics before retrying'))


class JobStore:
    def __init__(self, path, capacity=100):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.capacity = capacity
        with self.connect() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS jobs (
              id TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL,
              idem TEXT UNIQUE, digest TEXT NOT NULL, status TEXT NOT NULL,
              created REAL NOT NULL, updated REAL NOT NULL, error TEXT);
            CREATE TABLE IF NOT EXISTS events (
              seq INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL,
              data TEXT NOT NULL, FOREIGN KEY(job_id) REFERENCES jobs(id));
            CREATE INDEX IF NOT EXISTS events_job ON events(job_id,seq);
            ''')
            columns = {r[1] for r in db.execute('PRAGMA table_info(jobs)')}
            if 'result' not in columns:
                db.execute('ALTER TABLE jobs ADD COLUMN result TEXT')
        os.chmod(self.path, 0o600)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA synchronous=FULL')
        try:
            with db:
                yield db
        finally:
            db.close()

    def submit(self, kind, payload, key=None, prepare=None):
        encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        if len(encoded.encode()) > 1_000_000:
            raise QueueFull('Job input exceeds the 1 MB admission limit')
        digest = hashlib.sha256((kind + encoded).encode()).hexdigest()
        if key is not None and (not key or len(key) > 200):
            raise ValueError('Idempotency-Key must contain 1..200 characters')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if key:
                old = db.execute('SELECT * FROM jobs WHERE idem=?', (key,)).fetchone()
                if old:
                    if old['digest'] != digest:
                        raise JobConflict('Idempotency key already used with different inputs')
                    return dict(old)
            # Reject new work before mutating inputs or accepting responsibility
            # when persistent storage is nearly full. Idempotent reads still work.
            import shutil
            if shutil.disk_usage(self.path.parent).free < 256 * 1024 * 1024:
                raise QueueFull('Job storage is low; free disk space before submitting work')
            count = db.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]
            if count >= self.capacity:
                raise QueueFull('Research queue is full')
            if prepare:
                encoded = json.dumps(prepare(payload), sort_keys=True, separators=(',', ':'))
                if len(encoded.encode()) > 1_000_000:
                    raise QueueFull('Prepared job input exceeds the 1 MB admission limit')
            job_id = 'job_' + uuid.uuid4().hex
            now = time.time()
            db.execute('INSERT INTO jobs(id,kind,payload,idem,digest,status,created,updated,error) VALUES (?,?,?,?,?,?,?,?,?)',
                       (job_id, kind, encoded, key, digest, 'queued', now, now, None))
        return self.get(job_id)

    def get(self, job_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
            return dict(row) if row else None

    def metrics(self):
        """Aggregate state only: no prompts, payloads, paths or artifact contents."""
        with self.connect() as db:
            counts = dict(db.execute('SELECT status,count(*) FROM jobs GROUP BY status'))
            oldest = db.execute("SELECT min(created) FROM jobs WHERE status='queued'").fetchone()[0]
            recent_failures = db.execute("SELECT count(*) FROM jobs WHERE status='failed' AND updated>?",
                                         (time.time() - 3600,)).fetchone()[0]
        return {'states': counts, 'capacity': self.capacity,
                'failed_last_hour': recent_failures,
                'oldest_queued_seconds': max(0, time.time() - oldest) if oldest is not None else 0}

    def append(self, job_id, data):
        encoded = json.dumps(data)
        if len(encoded.encode()) > 256_000:
            encoded = json.dumps({'stage': 'Warning', 'message': 'Oversized event omitted'})
        with self.connect() as db:
            count = db.execute('SELECT count(*) FROM events WHERE job_id=?', (job_id,)).fetchone()[0]
            if count >= 10000:
                raise RuntimeError('Job event budget exhausted')
            db.execute('INSERT INTO events(job_id,data) VALUES (?,?)', (job_id, encoded))

    def events(self, job_id, after=0):
        with self.connect() as db:
            return [dict(r) for r in db.execute('SELECT seq,data FROM events WHERE job_id=? AND seq>? ORDER BY seq LIMIT 100', (job_id, after))]

    def recover(self):
        # Call only while holding the exclusive worker lock. Never reissue ambiguous paid work.
        with self.connect() as db:
            db.execute("UPDATE jobs SET status='interrupted',error='Worker stopped; reconcile external effects before creating another job',updated=? WHERE status='running'", (time.time(),))

    def claim(self):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY created,id LIMIT 1").fetchone()
            if not row:
                return None
            db.execute("UPDATE jobs SET status='running',updated=? WHERE id=?", (time.time(), row['id']))
            return dict(row)

    def finish(self, job_id, error=None, result=None):
        with self.connect() as db:
            db.execute("UPDATE jobs SET status=?,error=?,updated=?,result=? WHERE id=? AND status='running'",
                       ('failed' if error else 'completed', error, time.time(), json.dumps(result), job_id))

    def cancel(self, job_id):
        with self.connect() as db:
            result = db.execute("UPDATE jobs SET status='cancelled',updated=? WHERE id=? AND status='queued'", (time.time(), job_id))
            if not result.rowcount:
                raise JobConflict('Only queued jobs can be cancelled; running work requires operator reconciliation')
        return self.get(job_id)


class DurableWorker:
    def __init__(self, store, handler, *, isolated_handler=None):
        self.store, self.handler = store, handler
        self.isolated_handler = isolated_handler
        self.stopping = threading.Event()
        self.thread = None
        self.lock = None

    def start(self):
        if self.thread and self.thread.is_alive():
            if self.stopping.is_set():
                raise RuntimeError('Previous worker is still stopping')
            return
        self.stopping.clear()
        lock = self.store.path.with_suffix('.worker.lock').open('a')
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            lock.close()
            raise RuntimeError('Another worker owns this job database; deploy exactly one API worker')
        self.lock = lock
        try:
            self.store.recover()
        except Exception:
            lock.close()
            raise
        self.thread = threading.Thread(target=self.run, daemon=True, name='durable-research-worker')
        self.thread.start()

    def run(self):
        try:
            while not self.stopping.is_set():
                job = self.store.claim()
                if not job:
                    self.stopping.wait(0.25)
                    continue
                try:
                    logging.getLogger(__name__).info('Job %s started (%s)', job['id'], job['kind'])
                    if self.isolated_handler:
                        result = self.isolated_handler(job['id'])
                    else:
                        result = self.handler(job['kind'], json.loads(job['payload']),
                                     lambda data: self.store.append(job['id'], dict(data, projectId=job['id'])))
                    self.store.finish(job['id'], result=result)
                    logging.getLogger(__name__).info('Job %s completed', job['id'])
                except JobExecutionFailure as exc:
                    self.store.finish(job['id'], str(exc))
                except Exception as exc:
                    logging.getLogger(__name__).error('Job %s failed (%s)', job['id'], type(exc).__name__)
                    # Provider exceptions can contain request/credential data. Keep public errors generic.
                    self.store.finish(job['id'], 'Execution failed; review server diagnostics before retrying')
        finally:
            self.lock.close()

    def stop(self):
        self.stopping.set()
        if self.thread:
            self.thread.join(timeout=2)
        # A busy worker retains its lock until it exits; a process death releases it.
