#!/usr/bin/env python3
"""P9.1 — Generate minimal golden input fixtures from agents/*/input.schema.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
OUT = ROOT / "evaluation" / "fixtures" / "golden"


def sample_for_schema(schema: dict) -> dict:
    """Build a minimal valid-ish object from JSON Schema (object-focused)."""
    if not isinstance(schema, dict):
        return {}
    t = schema.get("type")
    if t == "string":
        return schema.get("default", "sample")
    if t == "integer":
        return schema.get("default", 1)
    if t == "number":
        return schema.get("default", 1.0)
    if t == "boolean":
        return schema.get("default", False)
    if t == "array":
        items = schema.get("items") or {}
        return [sample_for_schema(items)] if items else []
    if t == "object" or "properties" in schema or "required" in schema:
        props = schema.get("properties") or {}
        required = schema.get("required") or []
        out = {}
        for key in required:
            if key in props:
                out[key] = sample_for_schema(props[key])
            else:
                out[key] = {}
        # include a few optional with defaults
        for key, sub in props.items():
            if key not in out and isinstance(sub, dict) and "default" in sub:
                out[key] = sub["default"]
        return out
    return {}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for folder in sorted(AGENTS.iterdir()):
        if not folder.is_dir() or not folder.name.startswith("A"):
            continue
        schema_path = folder / "input.schema.json"
        if not schema_path.exists():
            continue
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        fixture = {
            "agent_id": folder.name,
            "schema_title": schema.get("title"),
            "payload": sample_for_schema(schema),
        }
        out_path = OUT / f"{folder.name}.input.json"
        out_path.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
        written += 1
    index = {
        "count": written,
        "path": str(OUT.relative_to(ROOT)),
        "note": "Minimal fixtures for schema/contract tests; not production goldens",
    }
    (OUT / "INDEX.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {written} fixtures under {OUT}")


if __name__ == "__main__":
    main()
