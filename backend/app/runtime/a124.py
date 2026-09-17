from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A124Error(RuntimeError):
    pass


REQUIRED = {
    "isolation_posture", "leakage_risks", "control_gaps", "policy_findings", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("tenant_map"), dict):
        raise A124Error("A124 requires tenant_map as an object")
    if not isinstance(request.get("isolation_controls"), dict):
        raise A124Error("A124 requires isolation_controls as an object")


async def run_a124_tenant_isolation_auditor(request: dict[str, Any]) -> RunResult:
    """Tenant Isolation Auditor — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "tenant_map": request["tenant_map"],
        "isolation_controls": request["isolation_controls"],
        "access_logs_summary": request.get("access_logs_summary") or {},
        "shared_resource_map": request.get("shared_resource_map") or {},
        "policy_matrix": request.get("policy_matrix") or {},
        "prior_isolation_audit": request.get("prior_isolation_audit") or {},
        "known_incidents": request.get("known_incidents") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No cross-tenant writes or data egress",
            "No secret exposure",
            "Leakage risks must be evidence-backed or explicitly assumed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A124",
        "Audit tenant isolation from the supplied tenant map and isolation controls. Report isolation posture, leakage risks, control gaps, policy findings and non-mutating recommendations. Return ONLY A124 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A124Error("A124 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Escalate critical leakage risks to governance; feed shared-resource findings to Multi-Company Operations Analyst (A127).")
    missing = REQUIRED - set(output)
    if missing:
        raise A124Error(f"A124 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A124Error("A124 confidence must be high, medium, or low")
    for f in ["leakage_risks", "control_gaps", "policy_findings", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A124Error(f"A124 {f} must be an array")
    if not isinstance(output.get("isolation_posture"), dict):
        raise A124Error("A124 isolation_posture must be an object")
    return RunResult(llm.run_id, "A124", "a124.ollama", "completed", result=output)
