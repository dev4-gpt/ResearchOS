"""Minimal repository secret scanner for CI and local pre-commit use."""

from pathlib import Path
import re
import sys


PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"nvapi-[0-9A-Za-z_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*=\s*['\"]?(?!your_|replace_|example|<)[^\s'\"]{16,}"),
]
SKIP_PARTS = {".git", ".venv", "node_modules", "scratch", ".pytest_cache"}
SKIP_NAMES = set()


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.name in SKIP_NAMES or any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if any(pattern.search(line) for pattern in PATTERNS):
                findings.append(f"{path}:{number}")
    return findings


if __name__ == "__main__":
    results = scan(Path(__file__).resolve().parents[1])
    if results:
        print("Potential secrets found:")
        print("\n".join(results))
        sys.exit(1)
    print("No potential secrets found in scanned text files.")
