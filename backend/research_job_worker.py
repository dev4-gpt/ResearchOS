"""One research queue execution in a process owned by the durable supervisor."""
import json
import os
import sys
import threading


def watch_parent():
    os.read(0, 1)
    os._exit(75)


def run(job_id, seconds):
    threading.Thread(target=watch_parent, daemon=True).start()
    from services.paid_execution import ExecutionBudget, ProviderFailure, execution_scope
    from services.spend_ledger import SpendLedger, SpendLimit
    import main

    job = main.job_store.get(job_id)
    if not job or job['status'] != 'running':
        return 1

    def emit(data):
        budget.remaining()
        main.job_store.append(job_id, dict(data, projectId=job_id))

    with execution_scope(ExecutionBudget(seconds)) as budget:
        try:
            if not main.orchestrator.is_dry_run:
                SpendLedger.configured()
            main.execute_research_job(job['kind'], json.loads(job['payload']), emit)
            budget.remaining()
        except ProviderFailure as exc:
            return 74 if exc.code == 429 else 75
        except TimeoutError:
            return 75
        except SpendLimit:
            return 76
    return 0


if __name__ == '__main__':
    raise SystemExit(run(sys.argv[1], int(sys.argv[2])))
