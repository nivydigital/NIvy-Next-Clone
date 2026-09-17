from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A110Error(RuntimeError):
    pass


REQUIRED = {
    "delegation_plan", "assignments", "dependencies", "escalation_paths", "risks", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("work_request"), dict):
        raise A110Error("A110 requires work_request as an object")
    if not isinstance(request.get("available_agents"), dict):
        raise A110Error("A110 requires available_agents as an object")


async def run_a110_delegation_coordinator(request: dict[str, Any]) -> RunResult:
    """Delegation Coordinator — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "work_request": request["work_request"],
        "available_agents": request["available_agents"],
        "capability_map": request.get("capability_map") or {},
        "priority": request.get("priority") or {},
        "constraints": request.get("constraints") or {},
        "prior_delegation": request.get("prior_delegation") or {},
        "sla_targets": request.get("sla_targets") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints_policy": [
            "No autonomous work execution",
            "No secret exposure",
            "Assignments must name concrete agents",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A110",
        "Produce a delegation plan for the work_request given available_agents. Include delegation_plan, assignments, dependencies, escalation_paths and risks. Return ONLY A110 JSON.",
        "PR003",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A110Error("A110 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Execute assignments via orchestration; hand off context via Agent Handoff Manager (A111).")
    missing = REQUIRED - set(output)
    if missing:
        raise A110Error(f"A110 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A110Error("A110 confidence must be high, medium, or low")
    for f in ["assignments", "dependencies", "escalation_paths", "risks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A110Error(f"A110 {f} must be an array")
    if not isinstance(output.get("delegation_plan"), dict):
        raise A110Error("A110 delegation_plan must be an object")
    return RunResult(llm.run_id, "A110", "a110.ollama", "completed", result=output)
