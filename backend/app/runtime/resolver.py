from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml


ROOT = Path(__file__).resolve().parents[3]


class CapabilityResolutionError(RuntimeError):
    pass


def _load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _records(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [x for x in value if isinstance(x, dict)]
    if isinstance(value, dict):
        for key in ("agents", "skills", "tools", "items", "registry"):
            if isinstance(value.get(key), list):
                return [x for x in value[key] if isinstance(x, dict)]
    return []


def resolve_agent(agent_id: str) -> dict[str, Any]:
    path = ROOT / "agents" / "registry.yaml"
    records = _records(_load_yaml(path))
    for agent in records:
        if agent.get("id") == agent_id:
            status = str(agent.get("status", "")).lower()
            if status in {"disabled", "deprecated", "archived"}:
                raise CapabilityResolutionError(f"agent {agent_id} is not activatable")
            return agent
    raise CapabilityResolutionError(f"undeclared agent: {agent_id}")


def resolve_capabilities(agent: dict[str, Any]) -> dict[str, list[str]]:
    tools = agent.get("tools", []) or []
    skills = agent.get("skills", []) or []
    prompts = agent.get("prompts", []) or []
    def ids(values: Any) -> list[str]:
        return [v.get("id") if isinstance(v, dict) else str(v) for v in values]
    return {"skills": ids(skills), "prompts": ids(prompts), "tools": ids(tools)}
