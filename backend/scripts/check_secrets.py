"""Fail CI when tracked source contains obvious live-secret signatures.

This is intentionally narrow and deterministic. It complements provider-side
secret scanning without pretending to detect every possible credential.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATTERNS = {
    "openai": re.compile(r"\bsk-(?:proj-|live-)?[A-Za-z0-9_-]{20,}\b"),
    "stripe_live": re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "github_token": re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
}

SKIP_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".xlsx",
    ".lock",
}


def tracked_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / p.decode() for p in proc.stdout.split(b"\0") if p]


def scan_file(path: Path) -> list[tuple[str, int]]:
    if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    hits = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append((name, line))
    return hits


def main() -> int:
    findings = []
    for path in tracked_files():
        for kind, line in scan_file(path):
            findings.append((path.relative_to(ROOT), line, kind))
    if findings:
        for path, line, kind in findings:
            print(f"SECRET_SIGNATURE {kind} {path}:{line}")
        print(f"Found {len(findings)} tracked secret signature(s).")
        return 1
    print("Tracked secret signature scan: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
