#!/usr/bin/env python3
"""Generate skills/implementations/SK*.yaml from skills/definitions.yaml if missing."""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = ROOT / "skills" / "definitions.yaml"
OUT = ROOT / "skills" / "implementations"


def main() -> None:
    data = yaml.safe_load(DEFINITIONS.read_text(encoding="utf-8")) or {}
    skills = data.get("skills") or {}
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for sid, meta in skills.items():
        path = OUT / f"{sid}.yaml"
        if path.exists():
            continue
        name = meta.get("name", sid)
        objective = meta.get("objective", "")
        inputs = meta.get("inputs") or []
        outputs = meta.get("outputs") or []
        doc = {
            "id": sid,
            "name": name,
            "version": "1.0",
            "status": "implementation",
            "objective": objective,
            "inputs": inputs,
            "outputs": outputs,
            "procedure": [
                {"step": 1, "action": "validate_inputs", "detail": f"Validate required inputs: {inputs}"},
                {"step": 2, "action": "prepare_context", "detail": "Normalize inputs and constraints"},
                {"step": 3, "action": "execute", "detail": objective},
                {"step": 4, "action": "quality_check", "detail": "Check outputs against acceptance"},
                {"step": 5, "action": "return", "detail": "Return structured result with evidence"},
            ],
            "quality_checks": ["schema_complete", "no_fabricated_claims", "unknowns_explicit"],
            "failure_policy": "fail_closed_on_invalid_input; never fabricate success",
            "evidence_policy": "preserve sources for material claims",
            "dependencies": [],
            "tools": ["tool.ollama.generate"],
            "acceptance": [f"{o} present" for o in outputs] or ["status present"],
        }
        path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
        written += 1
    print(f"wrote {written} skill implementations under {OUT}")


if __name__ == "__main__":
    main()
