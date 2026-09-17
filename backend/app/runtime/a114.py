from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A114Error(RuntimeError):
    pass


REQUIRED = {
    "failure_diagnosis", "impact_assessment", "recovery_options", "recommended_sequence", "escalation", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("failure_event"), dict):
        raise A114Error("A114 requires failure_event as an object")
    if not isinstance(request.get("collaboration_trace"), dict):
        raise A114Error("A114 requires collaboration_trace as an object")


async def run_a114_collaboration_failure(request: dict[str, Any]) -> RunResult:
    """Collaboration Failure Handler — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "failure_event": request["failure_event"],
        "collaboration_trace": request["collaboration_trace"],
        "agent_health": request.get("agent_health") or {},
        "prior_incidents": request.get("prior_incidents") or [],
        "sla_targets": request.get("sla_targets") or {},
        "recovery_constraints": request.get("recovery_constraints") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No autonomous recovery execution",
            "No secret exposure",
            "Recovery options must be ranked and evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A114",
        "Diagnose the collaboration failure from the failure_event and collaboration_trace. Produce failure_diagnosis, impact_assessment, recovery_options, recommended_sequence and escalation. Return ONLY A114 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A114Error("A114 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Execute recommended_sequence via orchestration with human approval where gated; log for Collaboration Auditor (A115).")
    missing = REQUIRED - set(output)
    if missing:
        raise A114Error(f"A114 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A114Error("A114 confidence must be high, medium, or low")
    for f in ["recovery_options", "recommended_sequence", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A114Error(f"A114 {f} must be an array")
    for f in ["failure_diagnosis", "impact_assessment", "escalation"]:
        if not isinstance(output.get(f), dict):
            raise A114Error(f"A114 {f} must be an object")
    return RunResult(llm.run_id, "A114", "a114.ollama", "completed", result=output)
