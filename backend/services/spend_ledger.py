"""Conservative cumulative reservations; ambiguous calls remain charged to the cap."""
import sqlite3
import time
from contextlib import closing
from pathlib import Path
from decimal import Decimal, InvalidOperation, ROUND_CEILING


class SpendLimit(RuntimeError):
    pass


class SpendLedger:
    def __init__(self, path, cap_usd):
        self.path = Path(path)
        cap = Decimal(str(cap_usd))
        if not cap.is_finite() or cap <= 0:
            raise ValueError('Spending cap must be finite and positive')
        if cap * 1_000_000 != int(cap * 1_000_000):
            raise ValueError('Spending cap must use whole microdollars')
        self.cap = int(cap * 1_000_000)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY CHECK(id=1), cap INTEGER NOT NULL, reserved INTEGER NOT NULL)')
            db.execute('INSERT OR IGNORE INTO budget VALUES (1,?,0)', (self.cap,))
            if db.execute('SELECT cap FROM budget WHERE id=1').fetchone()[0] != self.cap:
                raise SpendLimit('Existing ledger cap cannot be changed implicitly')
        self.path.chmod(0o600)

    @classmethod
    def configured(cls):
        import os

        path = os.getenv('RESEARCHINGOS_SPEND_LEDGER')
        cap = os.getenv('RESEARCHINGOS_SPEND_CAP_USD')
        if not path or not cap or not Path(path).is_absolute():
            raise SpendLimit('Paid calls require an absolute path to the shared spending ledger and its cap')
        ledger = cls.__new__(cls)
        ledger.path = Path(path).resolve()
        try:
            expected = Decimal(cap) * 1_000_000
            with closing(ledger.connect()) as db:
                row = db.execute('SELECT cap,reserved FROM budget WHERE id=1').fetchone()
        except (sqlite3.Error, InvalidOperation) as exc:
            raise SpendLimit('Configured spending ledger is missing or unreadable') from exc
        if row is None or not 0 <= row[1] <= row[0] or expected != row[0]:
            raise SpendLimit('Configured cap differs from the existing spending ledger')
        ledger.cap = row[0]
        return ledger

    def connect(self, timeout=10):
        # Opening a missing or moved ledger must never grant a fresh allowance.
        return sqlite3.connect(self.path.resolve().as_uri() + '?mode=rw', uri=True, timeout=timeout)

    def reserve(self, usd, *, provider=None, interval=0, deadline=None):
        value = Decimal(str(usd))
        if not value.is_finite() or value < 0:
            raise ValueError('Reservation must be finite and nonnegative')
        amount = int((value * 1_000_000).to_integral_value(rounding=ROUND_CEILING))
        while True:
            remaining = 10 if deadline is None else deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('Spending reservation deadline exhausted')
            with closing(self.connect(timeout=min(remaining, 10))) as db, db:
                db.execute('BEGIN IMMEDIATE')
                cap, used = db.execute('SELECT cap,reserved FROM budget WHERE id=1').fetchone()
                if cap != self.cap or not 0 <= used <= cap or used + amount > cap:
                    raise SpendLimit('Cumulative spending cap exhausted or changed')
                now = time.time()
                wait = 0
                if provider:
                    db.execute('CREATE TABLE IF NOT EXISTS pacing (provider TEXT PRIMARY KEY, next_call REAL NOT NULL)')
                    slot = db.execute('SELECT next_call FROM pacing WHERE provider=?', (provider,)).fetchone()
                    wait = max(0, slot[0] - now) if slot else 0
                if not wait:
                    if deadline is not None and time.monotonic() >= deadline:
                        raise TimeoutError('Spending reservation deadline exhausted')
                    db.execute('UPDATE budget SET reserved=reserved+? WHERE id=1', (amount,))
                    if provider:
                        db.execute('INSERT OR REPLACE INTO pacing VALUES (?,?)', (provider, now + interval))
                    return
            if deadline is not None and wait >= deadline - time.monotonic():
                raise TimeoutError('No provider rate slot before deadline')
            time.sleep(wait)

    def status(self):
        with closing(self.connect()) as db:
            cap, used = db.execute('SELECT cap,reserved FROM budget WHERE id=1').fetchone()
        return {'cap_usd': cap / 1_000_000, 'reserved_usd': used / 1_000_000}
