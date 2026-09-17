from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A101Error(RuntimeError):
    pass


REQUIRED = {
    "quality_status", "signal_summary", "anomalies", "escalations", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("telemetry_snapshot"), dict):
        raise A101Error("A101 requires telemetry_snapshot as an object")
    if not isinstance(request.get("quality_targets"), dict):
        raise A101Error("A101 requires quality_targets as an object")


async def run_a101_runtime_quality(request: dict[str, Any]) -> RunResult:
    """Runtime Quality Monitor — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "telemetry_snapshot": request["telemetry_snapshot"],
        "quality_targets": request["quality_targets"],
        "error_budget": request.get("error_budget") or {},
        "incident_history": request.get("incident_history") or {},
        "prior_monitor_report": request.get("prior_monitor_report") or {},
        "service_map": request.get("service_map") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production remediation execution",
            "No secret exposure",
            "Anomalies must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A101",
        "Assess runtime quality from telemetry_snapshot against quality_targets. Produce quality_status, signal_summary, anomalies, escalations and recommendations. Return ONLY A101 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A101Error("A101 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Route escalations to platform ops; share cost-related anomalies with Cost Observability (A102).")
    missing = REQUIRED - set(output)
    if missing:
        raise A101Error(f"A101 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A101Error("A101 confidence must be high, medium, or low")
    for f in ["anomalies", "escalations", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A101Error(f"A101 {f} must be an array")
    for f in ["quality_status", "signal_summary"]:
        if not isinstance(output.get(f), dict):
            raise A101Error(f"A101 {f} must be an object")
    return RunResult(llm.run_id, "A101", "a101.ollama", "completed", result=output)
