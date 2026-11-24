#!/bin/bash
# Run from the operator's Terminal when this workspace cannot write .git.
# Explicit paths preserve unrelated vault edits and private runtime data.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "$(git branch --show-current)" != 'wip/backup-local-2026-10-19' ]; then
  echo 'Unexpected branch; review the target before committing.' >&2
  exit 1
fi
if ! git diff --cached --quiet; then
  echo 'The index already contains changes. Review those before this checkpoint.' >&2
  exit 1
fi
files=(
  .env.example .github/workflows/integrity.yml requirements-ci.txt
  backend/main.py backend/services/access_control.py backend/services/durable_jobs.py
  backend/services/pdf_extractor.py backend/services/research_skills.py
  backend/services/operations.py backend/services/request_limits.py
  backend/tests/test_universal_skills_and_slop.py backend/tests/test_build_inputs.py
  backend/tests/test_operations.py backend/tests/test_operations_monitor.py
  backend/tests/test_operator_limits.py backend/tests/test_pdf_download_limits.py
  backend/tests/test_skill_distribution.py
  frontend/src/components/OperatorGate.tsx
  scripts/check_build_inputs.py scripts/monitor_operations.py scripts/commit-production-checkpoint.sh
  deploy/operations-monitor.service.example deploy/operations-monitor.timer.example
  docs/production-deployment.md docs/release-completion-checklist.md
  docs/production-acceptance-contract.md docs/production-design-review-2026-11-23.md
  docs/local-authenticated-validation-2026-11-23.json
  production-release-finish-plan.md task_plan.md findings.md progress.md
)
command -v gitleaks >/dev/null
scan_dir=$(mktemp -d)
trap 'rm -rf "$scan_dir"' EXIT
for path in "${files[@]}"; do
  mkdir -p "$scan_dir/$(dirname "$path")"
  cp "$path" "$scan_dir/$path"
done
gitleaks dir "$scan_dir" --redact --no-banner
git add -- "${files[@]}"
gitleaks git --staged --redact --no-banner
git diff --cached --check
git diff --cached --stat
git commit -m 'feat: Harden operator access and production diagnostics'
git push origin HEAD
git log -1 --oneline
git status -sb
