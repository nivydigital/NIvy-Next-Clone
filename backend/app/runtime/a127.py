from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A127Error(RuntimeError):
    pass


REQUIRED = {
    "portfolio_summary", "isolation_assessment", "shared_resource_risks", "policy_consistency", "capacity_findings", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("company_portfolio"), dict):
        raise A127Error("A127 requires company_portfolio as an object")
    if not isinstance(request.get("operations_snapshot"), dict):
        raise A127Error("A127 requires operations_snapshot as an object")


async def run_a127_multi_company_ops(request: dict[str, Any]) -> RunResult:
    """Multi-Company Operations Analyst — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "company_portfolio": request["company_portfolio"],
        "operations_snapshot": request["operations_snapshot"],
        "shared_services_map": request.get("shared_services_map") or {},
        "policy_matrix": request.get("policy_matrix") or {},
        "capacity_metrics": request.get("capacity_metrics") or {},
        "incident_summary": request.get("incident_summary") or [],
        "prior_analysis": request.get("prior_analysis") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No cross-tenant writes or data egress",
            "No secret exposure",
            "Recommendations must respect tenant isolation",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A127",
        "Analyze multi-company / multi-tenant operational posture from the supplied portfolio and operations snapshot. Assess isolation, shared-resource risks, policy consistency and capacity. Return ONLY A127 JSON.",
        "PR003",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A127Error("A127 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Review recommendations with platform governance; feed isolation gaps to Tenant Isolation Auditor (A124).")
    missing = REQUIRED - set(output)
    if missing:
        raise A127Error(f"A127 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A127Error("A127 confidence must be high, medium, or low")
    for f in ["isolation_assessment", "shared_resource_risks", "capacity_findings", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A127Error(f"A127 {f} must be an array")
    for f in ["portfolio_summary", "policy_consistency"]:
        if not isinstance(output.get(f), dict):
            raise A127Error(f"A127 {f} must be an object")
    return RunResult(llm.run_id, "A127", "a127.ollama", "completed", result=output)
