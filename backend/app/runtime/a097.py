from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A097Error(RuntimeError):
    pass


REQUIRED = {
    "allocation_plan", "headroom", "bottlenecks", "risks", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("demand_forecast"), dict):
        raise A097Error("A097 requires demand_forecast as an object")
    if not isinstance(request.get("resource_inventory"), dict):
        raise A097Error("A097 requires resource_inventory as an object")


async def run_a097_resource_planning(request: dict[str, Any]) -> RunResult:
    """Resource Planning Analyst — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "demand_forecast": request["demand_forecast"],
        "resource_inventory": request["resource_inventory"],
        "constraints": request.get("constraints") or {},
        "priority_policy": request.get("priority_policy") or {},
        "historical_utilization": request.get("historical_utilization") or {},
        "prior_plan": request.get("prior_plan") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints_policy": [
            "No live schedule or infra mutation",
            "No secret exposure",
            "Bottlenecks must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A097",
        "Produce a resource allocation plan from demand_forecast and resource_inventory. Include allocation_plan, headroom, bottlenecks, risks and recommendations. Return ONLY A097 JSON.",
        "PR001",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A097Error("A097 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Review bottlenecks with ops; align with Capacity Planner (A123) for infra headroom.")
    missing = REQUIRED - set(output)
    if missing:
        raise A097Error(f"A097 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A097Error("A097 confidence must be high, medium, or low")
    for f in ["bottlenecks", "risks", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A097Error(f"A097 {f} must be an array")
    for f in ["allocation_plan", "headroom"]:
        if not isinstance(output.get(f), dict):
            raise A097Error(f"A097 {f} must be an object")
    return RunResult(llm.run_id, "A097", "a097.ollama", "completed", result=output)
