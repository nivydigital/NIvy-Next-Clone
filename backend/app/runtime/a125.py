from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A125Error(RuntimeError):
    pass


REQUIRED = {
    "recovery_objectives", "failover_sequences", "backup_verification", "communication_runbook", "validation_checklist", "risks", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("system_inventory"), dict):
        raise A125Error("A125 requires system_inventory as an object")
    if not isinstance(request.get("recovery_objectives"), dict):
        raise A125Error("A125 requires recovery_objectives as an object")


async def run_a125_disaster_recovery(request: dict[str, Any]) -> RunResult:
    """Disaster Recovery Planner — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "system_inventory": request["system_inventory"],
        "recovery_objectives": request["recovery_objectives"],
        "current_backup_state": request.get("current_backup_state") or {},
        "dependency_map": request.get("dependency_map") or {},
        "compliance_constraints": request.get("compliance_constraints") or [],
        "prior_dr_plan": request.get("prior_dr_plan") or {},
        "incident_history": request.get("incident_history") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No live infrastructure mutation",
            "No secret exposure",
            "All claims must be evidence-backed or explicitly assumed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A125",
        "Produce a disaster recovery plan for the supplied AIOS system inventory and recovery objectives. Cover RTO/RPO, failover sequences, backup verification, communication runbook and validation checklist. Return ONLY A125 JSON.",
        "PR002",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A125Error("A125 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Review DR plan with platform ops; schedule tabletop exercise; hand off to Deployment Rollout Agent (A126).")
    missing = REQUIRED - set(output)
    if missing:
        raise A125Error(f"A125 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A125Error("A125 confidence must be high, medium, or low")
    for f in ["failover_sequences", "backup_verification", "communication_runbook", "validation_checklist", "risks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A125Error(f"A125 {f} must be an array")
    if not isinstance(output.get("recovery_objectives"), dict):
        raise A125Error("A125 recovery_objectives must be an object")
    return RunResult(llm.run_id, "A125", "a125.ollama", "completed", result=output)
