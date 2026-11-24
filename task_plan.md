# ResearchingOS production completion

Goal: execute `production-release-finish-plan.md` and report evidence without treating local fixtures as deployed production.

## Phases

1. Review architecture and acceptance contract — complete locally; operator targets pending.
2. Reproducibility and CI — local audit/tests complete; clean CI install/image/security/license receipts remain pending.
3. Security, overload and operations — local controls implemented/tested: authentication/session/body/job/storage boundaries, PDF origin/byte restrictions, skill distribution gate and monitoring. Unqualified legacy executors are local-only. Host disk quota, alert delivery, retention decision and full hostile-parser qualification remain open.
4. Live workflows, HTTPS and off-host recovery — blocked on inputs and sufficient existing allowance.
5. Final verification — final local tree: 421 backend tests passed/seven warnings; authenticated local integration repeated successfully with all four surfaces 200 and owned processes stopped. Frontend build/tests/lint previously passed and frontend unchanged since. Production acceptance remains pending clean CI/image/browser/soak receipts and deployment-level controls.

## Constraints / errors

- GitHub run 45309065824 for `afc09af`: frontend and reproducibility jobs passed, including actual frozen installation/source checks. Integrity failed during test collection because CI omitted OpenAI and PyMuPDF imports. Added explicit versions matching the local validated environment, pinned dspy implementation to avoid observed 3.5.0 transitive drift, and added an import preflight. Remote rerun requires a follow-up push.

- Preserve unrelated vault changes; do not reset the original $5 spending ledger or make unauthorized paid calls.
- Existing Git metadata writes and Docker socket access have been denied in this session. Do not bypass those boundaries.
- Initial planning files did not exist; created them without replacing other plans.
- External target decisions remain missing; independent local work continues.
- Clean isolated frozen install attempt used a new temporary cache and failed offline: missing `ormsgpack==1.12.2` wheel. Existing backend environment was untouched. CI now performs this install on a network-enabled clean runner; local install success remains unverified.
- Operator is undecided about hosting and concerned about Mac storage. Read-only inspection found 1.8 GiB free and Docker Desktop storage directory 26 GB. No deletion authorized or performed. Hosted model APIs do not require a GPU on the application host; local model hosting is a separate capacity decision.
- One tool invocation reported runtime replacement; repeated only the read-only storage/build audit. It succeeded. No mutations were replayed.
