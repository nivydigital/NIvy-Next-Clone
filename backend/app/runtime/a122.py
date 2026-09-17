from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A122Error(RuntimeError):
    pass


REQUIRED = {
    "slo_status", "error_budget", "anomalies", "risk_escalations", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("telemetry_snapshot"), dict):
        raise A122Error("A122 requires telemetry_snapshot as an object")
    if not isinstance(request.get("service_inventory"), dict):
        raise A122Error("A122 requires service_inventory as an object")


async def run_a122_reliability_monitor(request: dict[str, Any]) -> RunResult:
    """Reliability Monitor — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "telemetry_snapshot": request["telemetry_snapshot"],
        "service_inventory": request["service_inventory"],
        "slo_targets": request.get("slo_targets") or {},
        "error_budget_state": request.get("error_budget_state") or {},
        "incident_history": request.get("incident_history") or [],
        "dependency_health": request.get("dependency_health") or {},
        "prior_reliability_report": request.get("prior_reliability_report") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production mutation or remediation execution",
            "No secret exposure",
            "Anomalies and escalations must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A122",
        "Assess reliability of AIOS runtimes and dependencies from the supplied telemetry and service inventory. Report SLO status, error budget, anomalies, risk escalations and non-mutating recommendations. Return ONLY A122 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A122Error("A122 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Route escalations to platform ops; feed capacity signals to Capacity Planner (A123).")
    missing = REQUIRED - set(output)
    if missing:
        raise A122Error(f"A122 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A122Error("A122 confidence must be high, medium, or low")
    for f in ["anomalies", "risk_escalations", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A122Error(f"A122 {f} must be an array")
    for f in ["slo_status", "error_budget"]:
        if not isinstance(output.get(f), dict):
            raise A122Error(f"A122 {f} must be an object")
    return RunResult(llm.run_id, "A122", "a122.ollama", "completed", result=output)
