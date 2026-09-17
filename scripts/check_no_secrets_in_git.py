#!/usr/bin/env python3
"""P10.1 — Fail if high-risk secret patterns appear in tracked files."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", ".local-data", "__pycache__", ".venv", "venv", "dist", "build"}
PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[=:]\s*['\"]?(?!change-me|replace_me|your_|xxx|empty|none|\s*$)[A-Za-z0-9_\-]{20,}"), "assigned secret-like value"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key block"),
    (re.compile(r"(?i)sk-[A-Za-z0-9]{20,}"), "openai-like key"),
]
ALLOW_PATH_FRAGMENTS = [".env.example", "SECRETS-POLICY", "check_no_secrets", "test_", "PHASE-10"]


def should_skip(path: Path) -> bool:
    if set(path.parts) & SKIP_DIRS:
        return True
    s = str(path)
    if any(a in s for a in ALLOW_PATH_FRAGMENTS):
        return True
    if path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".pyc"}:
        return True
    return False


def main() -> int:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            if "change-me" in low or "replace_me" in low or "your_" in low:
                continue
            if "${" in line and ":-" in line:
                continue
            for rx, label in PATTERNS:
                if rx.search(line):
                    findings.append(f"{path.relative_to(ROOT)}:{i}: {label}")
                    break
    if findings:
        print("FAIL — possible secrets in tracked files:")
        for f in findings[:50]:
            print(f"  {f}")
        return 1
    print("OK — no high-confidence secret patterns in tracked files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
