#!/usr/bin/env python3
"""Validate skills/implementations against STD-01 mandatory fields."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "skills" / "implementations"
REQUIRED = ["id:", "name:", "version:", "status:", "objective:", "non_goals:", "inputs:", "outputs:", "procedure:", "quality_checks:", "failure_policy:", "evidence_policy:", "dependencies:", "acceptance_criteria:", "evaluation:", "provenance:"]

def main() -> int:
    files = sorted(IMPL.glob("SK*.yaml"))
    if len(files) < 50:
        print(f"FAIL — expected >=50 skill files, found {len(files)}")
        return 1
    errors = []
    for path in files:
        text = path.read_text()
        for req in REQUIRED:
            if req not in text:
                errors.append(f"{path.name}: missing {req}")
        if text.count("step:") < 3 and text.count("- {") < 3:
            errors.append(f"{path.name}: procedure too thin")
    if errors:
        print("FAIL — STD-01 validation errors:")
        for e in errors[:40]:
            print(" ", e)
        return 1
    print(f"OK — {len(files)} skills meet STD-01 mandatory field presence")
    return 0

if __name__ == "__main__":
    sys.exit(main())
