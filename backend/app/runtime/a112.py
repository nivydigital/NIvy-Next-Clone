from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A112Error(RuntimeError):
    pass


REQUIRED = {
    "context_plan", "visibility_map", "retention_rules", "handoff_rules", "risks", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("collaboration_scope"), dict):
        raise A112Error("A112 requires collaboration_scope as an object")
    if not isinstance(request.get("participant_agents"), dict):
        raise A112Error("A112 requires participant_agents as an object")


async def run_a112_shared_context(request: dict[str, Any]) -> RunResult:
    """Shared Context Manager — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "collaboration_scope": request["collaboration_scope"],
        "participant_agents": request["participant_agents"],
        "context_payload": request.get("context_payload") or {},
        "retention_policy": request.get("retention_policy") or {},
        "visibility_rules": request.get("visibility_rules") or {},
        "prior_context": request.get("prior_context") or {},
        "constraints": request.get("constraints") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints_policy": [
            "No SoR writes",
            "No secret exposure",
            "Visibility and retention must be explicit",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A112",
        "Produce a shared collaboration context plan from the supplied scope and participant agents. Include context_plan, visibility_map, retention_rules, handoff_rules and risks. Return ONLY A112 JSON.",
        "PR003",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A112Error("A112 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Apply context_plan in orchestration layer; share visibility_map with Collaboration Policy Agent (A113).")
    missing = REQUIRED - set(output)
    if missing:
        raise A112Error(f"A112 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A112Error("A112 confidence must be high, medium, or low")
    for f in ["retention_rules", "handoff_rules", "risks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A112Error(f"A112 {f} must be an array")
    for f in ["context_plan", "visibility_map"]:
        if not isinstance(output.get(f), dict):
            raise A112Error(f"A112 {f} must be an object")
    return RunResult(llm.run_id, "A112", "a112.ollama", "completed", result=output)
