from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A123Error(RuntimeError):
    pass


REQUIRED = {
    "forecast_summary", "headroom", "scale_triggers", "recommendations", "cost_notes", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("workload_forecast"), dict):
        raise A123Error("A123 requires workload_forecast as an object")
    if not isinstance(request.get("current_capacity"), dict):
        raise A123Error("A123 requires current_capacity as an object")


async def run_a123_capacity_planner(request: dict[str, Any]) -> RunResult:
    """Capacity Planner — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "workload_forecast": request["workload_forecast"],
        "current_capacity": request["current_capacity"],
        "growth_assumptions": request.get("growth_assumptions") or {},
        "cost_constraints": request.get("cost_constraints") or {},
        "reliability_signals": request.get("reliability_signals") or {},
        "historical_utilization": request.get("historical_utilization") or {},
        "prior_capacity_plan": request.get("prior_capacity_plan") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No live scale-up/scale-down execution",
            "No secret exposure",
            "Scale triggers must be measurable",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A123",
        "Produce a capacity plan from the supplied workload forecast and current capacity. Include forecast summary, headroom, measurable scale triggers, cost-aware recommendations. Return ONLY A123 JSON.",
        "PR002",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A123Error("A123 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Review headroom with platform ops; align scale triggers with Reliability Monitor (A122).")
    missing = REQUIRED - set(output)
    if missing:
        raise A123Error(f"A123 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A123Error("A123 confidence must be high, medium, or low")
    for f in ["scale_triggers", "recommendations", "cost_notes", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A123Error(f"A123 {f} must be an array")
    for f in ["forecast_summary", "headroom"]:
        if not isinstance(output.get(f), dict):
            raise A123Error(f"A123 {f} must be an object")
    return RunResult(llm.run_id, "A123", "a123.ollama", "completed", result=output)
