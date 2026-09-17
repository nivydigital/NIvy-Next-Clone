"""Phase 3 — Skill loading and Agent → Skill → Tool resolution (fail closed)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .engine import ROOT, RuntimeDenied, runtime_engine

SKILLS_DIR = ROOT / "skills"
IMPL_DIR = SKILLS_DIR / "implementations"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def list_skill_ids_from_registry() -> list[str]:
    reg = _load_yaml(SKILLS_DIR / "registry.yaml")
    skills = reg.get("skills") or []
    out: list[str] = []
    for s in skills:
        if isinstance(s, dict) and s.get("id"):
            out.append(str(s["id"]))
    return out


def load_skill_implementation(skill_id: str) -> dict[str, Any]:
    """Load skills/implementations/{skill_id}.yaml or raise RuntimeDenied."""
    path = IMPL_DIR / f"{skill_id}.yaml"
    if not path.exists():
        raise RuntimeDenied(f"skill implementation missing: {skill_id} (expected {path})")
    data = _load_yaml(path)
    if data.get("id") and str(data["id"]) != skill_id:
        raise RuntimeDenied(f"skill id mismatch in {path}: {data.get('id')} != {skill_id}")
    required = ["id", "objective", "inputs", "procedure", "outputs", "quality_checks", "failure_policy", "evidence_policy", "dependencies"]
    missing = [k for k in required if k not in data]
    if missing:
        raise RuntimeDenied(f"skill {skill_id} implementation incomplete; missing: {missing}")
    return data


def skill_implementation_exists(skill_id: str) -> bool:
    return (IMPL_DIR / f"{skill_id}.yaml").exists()


def resolve_agent_skills(agent_id: str) -> dict[str, Any]:
    """
    Resolve Agent → Skills → Tools.
    Fail closed if agent declares skills that have no implementation file.
    """
    agent = None
    for a in runtime_engine.registry.get("agents", []) or []:
        if isinstance(a, dict) and a.get("id") == agent_id:
            agent = a
            break
    if agent is None:
        raise RuntimeDenied(f"undeclared agent: {agent_id}")

    skill_ids = []
    for x in agent.get("skills") or []:
        skill_ids.append(x.get("id") if isinstance(x, dict) else str(x))

    tools = []
    for x in agent.get("tools") or []:
        tools.append(x.get("id") if isinstance(x, dict) else str(x))

    resolved: list[dict[str, Any]] = []
    missing: list[str] = []
    for sid in skill_ids:
        if not skill_implementation_exists(sid):
            missing.append(sid)
            continue
        impl = load_skill_implementation(sid)
        # Tools declared on skill (optional) must be subset of agent tools when both set
        skill_tools = impl.get("tools") or []
        skill_tool_ids = [t.get("id") if isinstance(t, dict) else str(t) for t in skill_tools]
        unauthorized = [t for t in skill_tool_ids if t and t not in tools]
        resolved.append(
            {
                "id": sid,
                "name": impl.get("name"),
                "objective": impl.get("objective"),
                "procedure_steps": len(impl.get("procedure") or []),
                "tools": skill_tool_ids,
                "unauthorized_tools": unauthorized,
                "status": impl.get("status", "implementation"),
            }
        )
        if unauthorized:
            raise RuntimeDenied(
                f"agent {agent_id} skill {sid} references tools not bound to agent: {unauthorized}"
            )

    if missing:
        raise RuntimeDenied(
            f"agent {agent_id} references skills without implementation: {missing}"
        )

    return {
        "agent_id": agent_id,
        "skills": resolved,
        "tools": tools,
        "ok": True,
    }


def skill_coverage_report() -> dict[str, Any]:
    """Inventory: registry skills vs implementation files (does not fail closed)."""
    registry_ids = list_skill_ids_from_registry()
    impl_ids = sorted(
        p.stem for p in IMPL_DIR.glob("SK*.yaml") if IMPL_DIR.exists()
    ) if IMPL_DIR.exists() else []
    missing = [s for s in registry_ids if s not in impl_ids]
    extra = [s for s in impl_ids if s not in registry_ids]
    return {
        "registry_count": len(registry_ids),
        "implementation_count": len(impl_ids),
        "missing_implementations": missing,
        "extra_implementations": extra,
        "complete": len(missing) == 0 and len(registry_ids) > 0,
    }
