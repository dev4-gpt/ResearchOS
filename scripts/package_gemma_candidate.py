#!/usr/bin/env python3
"""Package the candidate config; this does not validate Kaggle compatibility."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "competition" / "gemma4"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "x", zipfile.ZIP_DEFLATED) as archive:
        for name in ("agent.yaml", "prompts/system.md"):
            archive.write(SOURCE / name, name)
    print(f"Candidate only — official harness validation pending: {args.output.resolve()}")


if __name__ == "__main__":
    main()
