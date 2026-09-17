from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A121Error(RuntimeError):
    pass


REQUIRED = {
    "twin_scope_summary", "twin_components", "fidelity_assessment", "simulation_use_cases", "gaps", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("twin_scope"), dict):
        raise A121Error("A121 requires twin_scope as an object")
    if not isinstance(request.get("source_system_map"), dict):
        raise A121Error("A121 requires source_system_map as an object")


async def run_a121_digital_twin_analyst(request: dict[str, Any]) -> RunResult:
    """Digital Twin Analyst — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "twin_scope": request["twin_scope"],
        "source_system_map": request["source_system_map"],
        "process_models": request.get("process_models") or {},
        "agent_inventory": request.get("agent_inventory") or {},
        "simulation_goals": request.get("simulation_goals") or [],
        "prior_twin_analysis": request.get("prior_twin_analysis") or {},
        "data_availability": request.get("data_availability") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No live production simulation",
            "No secret exposure",
            "Fidelity and gaps must be explicit",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A121",
        "Analyze digital-twin scope for the given systems and processes. Map twin components, assess fidelity, define simulation use cases, gaps and recommendations. Return ONLY A121 JSON. Do not execute simulations against production.",
        "PR003",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A121Error("A121 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Prioritize high-fidelity components for sandbox twin build; feed capacity needs to Capacity Planner (A123).")
    missing = REQUIRED - set(output)
    if missing:
        raise A121Error(f"A121 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A121Error("A121 confidence must be high, medium, or low")
    for f in ["twin_components", "simulation_use_cases", "gaps", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A121Error(f"A121 {f} must be an array")
    for f in ["twin_scope_summary", "fidelity_assessment"]:
        if not isinstance(output.get(f), dict):
            raise A121Error(f"A121 {f} must be an object")
    return RunResult(llm.run_id, "A121", "a121.ollama", "completed", result=output)
