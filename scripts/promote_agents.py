#!/usr/bin/env python3
"""Promote agent registry status when scaffold gates are met (Phase 6).

Promotion rules (declared -> implementation):
  1. agents/{id}/agent.yaml exists
  2. input.schema.json + output.schema.json exist
  3. backend/app/runtime/{id_lower}.py exists with run_{id_lower}_* entrypoint
  4. agent.yaml lists runtime.adapter + runtime.entrypoint

Does NOT promote to production without evaluation evidence (deferred testing).
"""
from __future__ import annotations

import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
RUNTIME = ROOT / "backend" / "app" / "runtime"
REGISTRY = AGENTS / "registry.yaml"
IMPL_REG = AGENTS / "implementation-registry.yaml"


def has_entrypoint(agent_id: str) -> tuple[bool, str | None]:
    mod = RUNTIME / f"{agent_id.lower()}.py"
    if not mod.exists():
        return False, None
    text = mod.read_text(encoding="utf-8")
    m = re.search(rf"async def (run_{agent_id.lower()}_\w+)", text)
    if m:
        return True, m.group(1)
    m2 = re.search(r"async def (run_\w+)", text)
    return (bool(m2), m2.group(1) if m2 else None)


def gates(agent_id: str) -> dict:
    folder = AGENTS / agent_id
    ok_folder = folder.is_dir()
    ok_agent_yaml = (folder / "agent.yaml").exists()
    ok_in = (folder / "input.schema.json").exists()
    ok_out = (folder / "output.schema.json").exists()
    ok_rt, entry = has_entrypoint(agent_id)
    return {
        "agent_id": agent_id,
        "folder": ok_folder,
        "agent_yaml": ok_agent_yaml,
        "input_schema": ok_in,
        "output_schema": ok_out,
        "runtime_module": ok_rt,
        "entrypoint": entry,
        "promotable": all([ok_folder, ok_agent_yaml, ok_in, ok_out, ok_rt]),
    }


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main() -> None:
    targets = [f"A{i:03d}" for i in range(100, 109)]
    report = [gates(a) for a in targets]
    promotable = [r for r in report if r["promotable"]]

    reg = load_yaml(REGISTRY)
    agents = reg.get("agents") or []
    by_id = {a["id"]: a for a in agents if isinstance(a, dict) and a.get("id")}

    for r in promotable:
        aid = r["agent_id"]
        if aid not in by_id:
            continue
        a = by_id[aid]
        a["status"] = "implementation"
        a["runtime"] = f"backend.app.runtime.{aid.lower()}:{r['entrypoint']}"
        # ensure agent.yaml status aligned
        ay = AGENTS / aid / "agent.yaml"
        if ay.exists():
            data = yaml.safe_load(ay.read_text(encoding="utf-8")) or {}
            if data.get("status") != "implementation":
                data["status"] = "implementation"
                ay.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    REGISTRY.write_text(yaml.safe_dump(reg, sort_keys=False), encoding="utf-8")

    # implementation-registry: upsert A100-A108
    impl = load_yaml(IMPL_REG)
    impl.setdefault("version", "1.0")
    impl.setdefault("status", "implementation-extension")
    impl.setdefault("agents", [])
    impl_by = {a["id"]: a for a in impl["agents"] if isinstance(a, dict) and a.get("id")}
    for r in promotable:
        aid = r["agent_id"]
        base = by_id.get(aid) or {}
        record = {
            "id": aid,
            "name": base.get("name") or aid,
            "version": "1.0",
            "status": "implementation",
            "owner": "unassigned",
            "runtime": f"backend.app.runtime.{aid.lower()}:{r['entrypoint']}",
            "skills": base.get("skills") or [],
            "prompts": base.get("prompts") or [],
            "knowledge": base.get("knowledge") or [],
            "tools": base.get("tools") or ["tool.ollama.generate"],
            "permissions": base.get("permissions") or {"side_effects": False},
        }
        impl_by[aid] = record
    impl["agents"] = list(impl_by.values())
    IMPL_REG.write_text(yaml.safe_dump(impl, sort_keys=False), encoding="utf-8")

    print("Phase 6 promotion report")
    for r in report:
        flag = "PROMOTE" if r["promotable"] else "BLOCK"
        print(f"  {r['agent_id']}: {flag} entry={r['entrypoint']}")
    print(f"promotable: {len(promotable)}/{len(targets)}")


if __name__ == "__main__":
    main()
