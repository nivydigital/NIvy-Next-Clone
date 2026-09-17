"""Agent discovery and structured execute dispatch (Phase 0.3 / 0.4)."""
from __future__ import annotations

import importlib
import inspect
import json
from pathlib import Path
from typing import Any, Callable, Awaitable

from .engine import ROOT, RunResult, runtime_engine, RuntimeDenied

RUNTIME_DIR = Path(__file__).resolve().parent
AGENTS_DIR = ROOT / "agents"

# Dedicated FastAPI routes already registered in main.py (not via /execute)
DEDICATED_ROUTES: dict[str, str] = {
    "A001": "POST /api/v1/runtime/agents/A001/research",
    "A002": "POST /api/v1/runtime/agents/A002/icp",
    "A003": "POST /api/v1/runtime/agents/A003/persona",
    "A004": "POST /api/v1/runtime/agents/A004/competitor",
    "A005": "POST /api/v1/runtime/agents/A005/channel",
}


def _module_path_for(agent_id: str) -> Path:
    return RUNTIME_DIR / f"{agent_id.lower()}.py"


def _folder_exists(agent_id: str) -> bool:
    return (AGENTS_DIR / agent_id).is_dir()


def _load_input_schema(agent_id: str) -> dict[str, Any] | None:
    path = AGENTS_DIR / agent_id / "input.schema.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _load_output_schema(agent_id: str) -> dict[str, Any] | None:
    path = AGENTS_DIR / agent_id / "output.schema.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _find_entrypoint(agent_id: str) -> tuple[str | None, Callable[..., Awaitable[RunResult]] | None]:
    """Import backend.app.runtime.a0xx and return (name, async callable) for run_a0xx_* if present."""
    mod_file = _module_path_for(agent_id)
    if not mod_file.exists():
        return None, None
    module_name = f"backend.app.runtime.{agent_id.lower()}"
    try:
        mod = importlib.import_module(module_name)
    except Exception:
        return None, None
    prefix = f"run_{agent_id.lower()}"
    candidates: list[tuple[str, Callable[..., Awaitable[RunResult]]]] = []
    for name, obj in inspect.getmembers(mod, inspect.iscoroutinefunction):
        if name.startswith(prefix) or name.startswith("run_a"):
            # Prefer names that include the agent number
            if agent_id.lower().replace("a", "") in name or name.startswith(prefix):
                candidates.append((name, obj))
    if not candidates:
        for name, obj in inspect.getmembers(mod, inspect.iscoroutinefunction):
            if name.startswith("run_"):
                candidates.append((name, obj))
                break
    if not candidates:
        return None, None
    # Prefer exact prefix match
    for name, obj in candidates:
        if name.startswith(prefix):
            return name, obj
    return candidates[0]


def _registry_agents() -> list[dict[str, Any]]:
    agents = runtime_engine.registry.get("agents", []) or []
    return [a for a in agents if isinstance(a, dict) and a.get("id")]


def _agent_from_registry(agent_id: str) -> dict[str, Any] | None:
    for a in _registry_agents():
        if a.get("id") == agent_id:
            return a
    return None


def list_agents() -> dict[str, Any]:
    """P0.3 discovery: registry + filesystem + entrypoint presence."""
    by_id: dict[str, dict[str, Any]] = {}

    for agent in _registry_agents():
        aid = str(agent["id"])
        mod = _module_path_for(aid)
        entry_name, _ = _find_entrypoint(aid)
        by_id[aid] = {
            "id": aid,
            "name": agent.get("name"),
            "registry_status": agent.get("status", "declared"),
            "registry_runtime": agent.get("runtime", "planned"),
            "in_registry": True,
            "agent_folder_exists": _folder_exists(aid),
            "runtime_module": str(mod.relative_to(ROOT)) if mod.exists() else None,
            "runtime_module_exists": mod.exists(),
            "structured_entrypoint": entry_name,
            "dedicated_route": DEDICATED_ROUTES.get(aid),
            "tools": agent.get("tools") or [],
            "prompts": agent.get("prompts") or [],
            "skills": agent.get("skills") or [],
            "input_schema": _folder_exists(aid) and (AGENTS_DIR / aid / "input.schema.json").exists(),
            "output_schema": _folder_exists(aid) and (AGENTS_DIR / aid / "output.schema.json").exists(),
        }

    # Include disk-only strategy agents (e.g. A003–A033) not in registry
    if AGENTS_DIR.exists():
        for path in sorted(AGENTS_DIR.iterdir()):
            if not path.is_dir() or not path.name.startswith("A"):
                continue
            aid = path.name
            if aid in by_id:
                continue
            mod = _module_path_for(aid)
            entry_name, _ = _find_entrypoint(aid)
            by_id[aid] = {
                "id": aid,
                "name": None,
                "registry_status": "extension_not_in_registry",
                "registry_runtime": None,
                "in_registry": False,
                "agent_folder_exists": True,
                "runtime_module": str(mod.relative_to(ROOT)) if mod.exists() else None,
                "runtime_module_exists": mod.exists(),
                "structured_entrypoint": entry_name,
                "dedicated_route": DEDICATED_ROUTES.get(aid),
                "tools": [],
                "prompts": [],
                "skills": [],
                "input_schema": (path / "input.schema.json").exists(),
                "output_schema": (path / "output.schema.json").exists(),
            }

    items = [by_id[k] for k in sorted(by_id.keys(), key=lambda x: (len(x), x))]
    structured = sum(1 for i in items if i.get("structured_entrypoint"))
    return {
        "count": len(items),
        "structured_entrypoint_count": structured,
        "dedicated_route_count": len(DEDICATED_ROUTES),
        "items": items,
    }


def get_agent(agent_id: str) -> dict[str, Any]:
    listing = list_agents()
    for item in listing["items"]:
        if item["id"] == agent_id:
            detail = dict(item)
            detail["input_schema_body"] = _load_input_schema(agent_id)
            detail["output_schema_body"] = _load_output_schema(agent_id)
            reg = _agent_from_registry(agent_id)
            if reg:
                detail["registry_record"] = reg
            return detail
    raise RuntimeDenied(f"unknown agent: {agent_id}")


def _validate_required_fields(payload: dict[str, Any], schema: dict[str, Any] | None) -> None:
    if not schema:
        return
    required = schema.get("required") or []
    missing = [f for f in required if f not in payload or payload.get(f) is None]
    if missing:
        raise RuntimeDenied(f"input missing required fields: {missing}")


async def execute_agent(
    agent_id: str,
    payload: dict[str, Any],
    prompt_id: str | None = None,
    allow_llm_fallback: bool = True,
) -> RunResult:
    """
    P0.4 unified path:
    validate input schema → resolve structured entrypoint → execute → audit via engine.
    Falls back to run_llm if no structured entrypoint and allow_llm_fallback.
    """
    # Prefer registry presence; extension agents allowed if module exists
    reg = _agent_from_registry(agent_id)
    mod = _module_path_for(agent_id)
    if reg is None and not mod.exists():
        raise RuntimeDenied(f"undeclared agent and no runtime module: {agent_id}")

    schema = _load_input_schema(agent_id)
    _validate_required_fields(payload, schema)

    entry_name, entry_fn = _find_entrypoint(agent_id)
    if entry_fn is not None:
        runtime_engine._record(
            event_type="agent.execute",
            actor="runtime",
            action=agent_id,
            status="started",
            request_id=payload.get("request_id"),
            data={"entrypoint": entry_name, "mode": "structured"},
        )
        try:
            result = await entry_fn(payload)
            runtime_engine._record(
                event_type="agent.execute",
                actor="runtime",
                action=agent_id,
                status=result.status if isinstance(result, RunResult) else "completed",
                request_id=getattr(result, "run_id", None),
                data={"entrypoint": entry_name, "mode": "structured"},
            )
            return result
        except Exception as exc:
            runtime_engine._record(
                event_type="agent.execute",
                actor="runtime",
                action=agent_id,
                status="failed",
                request_id=payload.get("request_id"),
                data={"entrypoint": entry_name, "error": str(exc)},
            )
            raise

    if not allow_llm_fallback:
        raise RuntimeDenied(f"no structured entrypoint for {agent_id}")

    # Fallback: generic LLM with registry prompt binding
    return await runtime_engine.run_llm(
        agent_id,
        prompt=str(payload.get("prompt") or ""),
        prompt_id=prompt_id or (reg.get("prompts", [None])[0] if reg else None),
        context=payload,
    )
