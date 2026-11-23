#!/usr/bin/env python3
"""Run discovery, selected research experiments and isolated manuscript generation."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from services.research_workflow import WorkflowSpec, create, resume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--spec', type=Path)
    group.add_argument('--resume')
    args = parser.parse_args()
    try:
        workflow_id = args.resume or create(WorkflowSpec.model_validate_json(args.spec.read_text()))['id']
        result = resume(workflow_id)
        print(json.dumps(result, indent=2))
        return 1 if result['status'] == 'blocked' else 0
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
