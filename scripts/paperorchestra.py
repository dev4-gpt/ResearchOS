#!/usr/bin/env python3
"""Prepare, execute in isolation, import and review PaperOrchestra jobs; never auto-publish."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from services.paperorchestra import prepare, intake


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    bundle = commands.add_parser('prepare')
    bundle.add_argument('--materials', type=Path, required=True)
    bundle.add_argument('--template', type=Path, required=True)
    bundle.add_argument('--writer-model', required=True)
    bundle.add_argument('--reflection-model', required=True)
    bundle.add_argument('--cutoff', required=True)
    imported = commands.add_parser('import-output')
    imported.add_argument('--job', required=True)
    imported.add_argument('--output', type=Path, required=True)
    execute = commands.add_parser('run')
    execute.add_argument('--job', required=True)
    execute.add_argument('--seconds', type=int, default=1800)
    audit = commands.add_parser('review')
    audit.add_argument('--job', required=True)
    audit.add_argument('--manuscript', required=True)
    audit.add_argument('--citation-map', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            result = prepare(args.materials, args.template, args.writer_model, args.reflection_model, args.cutoff)
        elif args.command == 'import-output':
            result = intake(args.job, args.output)
        elif args.command == 'run':
            from services.paperorchestra_worker import run
            result = run(args.job, args.seconds)
        else:
            from services.paperorchestra_review import review
            result = review(args.job, args.manuscript, json.loads(args.citation_map.read_text()))
    except (ValueError, RuntimeError, OSError) as exc:
        parser.exit(1, f'{exc}\n')
    print(json.dumps(result, indent=2))
    return 1 if result.get('status') in {'failed', 'blocked', 'timed_out', 'cancelled', 'interrupted'} else 0


if __name__ == '__main__':
    raise SystemExit(main())
