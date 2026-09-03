"""Record iCloud sync-conflict copies inside .git. Idempotent."""
import sys
sys.path.insert(0, "backend")
from services.error_ledger import ErrorLedgerService

INCIDENT = {
    "component": ".git (working tree on iCloud Drive)",
    "stage": "version_control",
    "error_type": "Sync Conflicts Inside The Git Directory",
    "summary": (
        "iCloud created conflict copies inside .git itself: eight copies of the "
        "index ('.git/index 2' through '.git/index 9'), a stale branch ref "
        "'.git/refs/heads/main 2' pointing at the initial commit from three months "
        "earlier, the matching '.git/refs/remotes/origin/main 2', and a copy under "
        "refs/codex/. Git read the duplicated refs as real branches, and `git fetch` "
        "failed outright with 'fatal: bad object refs/heads/main 2 -- did not send "
        "all necessary objects'. This surfaced immediately after merging PR #1, "
        "while confirming the merge had landed."
    ),
    "root_cause": (
        "The repository lives in ~/Library/Mobile Documents/. iCloud resolves a "
        "write conflict by duplicating the file beside the original, and it applies "
        "that to .git the same as to anything else. Git's ref namespace is a "
        "directory tree, so a duplicated file becomes a branch."
    ),
    "resolution": (
        "The eleven conflict copies were moved to the Trash; fetch, rev-parse and "
        "merge-base then worked, and the merge was confirmed on origin/main. No "
        "object loss: the duplicated refs pointed at commits already reachable, and "
        "only .git/index is ever read, so the numbered copies were inert."
    ),
    "prevention_rule": (
        "A git repository must not live inside a directory a sync client rewrites. "
        "This is the third form the same cause has taken -- credentials in duplicated "
        ".env files, duplicated modules entering an experimental corpus and flipping "
        "a result's sign, and now duplicated refs breaking fetch. The CI check for "
        "tracked '<stem> 2.<ext>' files cannot see any of these, because .git is not "
        "tracked. Move the repository off iCloud."
    ),
}

ledger = ErrorLedgerService()
if INCIDENT["summary"] in {e.get("summary") for e in ledger.data.get("history", [])}:
    print("  already recorded")
else:
    e = ledger.record_error(**INCIDENT)
    print(f"  {e['error_id']} [{e['status']}] {e['error_type']}")
