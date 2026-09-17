from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A115Error(RuntimeError):
    pass


REQUIRED = {
    "audit_summary", "policy_findings", "leakage_risks", "handoff_quality", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("collaboration_trace"), dict):
        raise A115Error("A115 requires collaboration_trace as an object")
    if not isinstance(request.get("policy_baseline"), dict):
        raise A115Error("A115 requires policy_baseline as an object")


async def run_a115_collaboration_auditor(request: dict[str, Any]) -> RunResult:
    """Collaboration Auditor — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "collaboration_trace": request["collaboration_trace"],
        "policy_baseline": request["policy_baseline"],
        "context_snapshots": request.get("context_snapshots") or {},
        "known_exceptions": request.get("known_exceptions") or [],
        "prior_audit": request.get("prior_audit") or {},
        "quality_targets": request.get("quality_targets") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No collaboration state mutation",
            "No secret exposure",
            "Findings must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A115",
        "Audit the collaboration_trace against the policy_baseline. Produce audit_summary, policy_findings, leakage_risks, handoff_quality and recommendations. Return ONLY A115 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A115Error("A115 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Escalate critical leakage_risks; feed systemic findings to Collaboration Policy Agent (A113).")
    missing = REQUIRED - set(output)
    if missing:
        raise A115Error(f"A115 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A115Error("A115 confidence must be high, medium, or low")
    for f in ["policy_findings", "leakage_risks", "handoff_quality", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A115Error(f"A115 {f} must be an array")
    if not isinstance(output.get("audit_summary"), dict):
        raise A115Error("A115 audit_summary must be an object")
    return RunResult(llm.run_id, "A115", "a115.ollama", "completed", result=output)
