from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A113Error(RuntimeError):
    pass


REQUIRED = {
    "policy_set", "escalation_paths", "approval_gates", "exceptions", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("policy_scope"), dict):
        raise A113Error("A113 requires policy_scope as an object")
    if not isinstance(request.get("participant_roles"), dict):
        raise A113Error("A113 requires participant_roles as an object")


async def run_a113_collaboration_policy(request: dict[str, Any]) -> RunResult:
    """Collaboration Policy Agent — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "policy_scope": request["policy_scope"],
        "participant_roles": request["participant_roles"],
        "existing_policies": request.get("existing_policies") or {},
        "risk_appetite": request.get("risk_appetite") or {},
        "regulatory_constraints": request.get("regulatory_constraints") or [],
        "prior_policy_report": request.get("prior_policy_report") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production policy enforcement writes",
            "No secret exposure",
            "Approval gates must be explicit",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A113",
        "Define collaboration policies for the given scope and roles. Produce policy_set, escalation_paths, approval_gates, exceptions and recommendations. Return ONLY A113 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A113Error("A113 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Review approval_gates with governance; feed exceptions to Collaboration Auditor (A115).")
    missing = REQUIRED - set(output)
    if missing:
        raise A113Error(f"A113 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A113Error("A113 confidence must be high, medium, or low")
    for f in ["policy_set", "escalation_paths", "approval_gates", "exceptions", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A113Error(f"A113 {f} must be an array")
    return RunResult(llm.run_id, "A113", "a113.ollama", "completed", result=output)
