from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A100Error(RuntimeError):
    pass


REQUIRED = {
    "audit_summary", "policy_findings", "tool_findings", "data_handling_findings", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("trace_bundle"), dict):
        raise A100Error("A100 requires trace_bundle as an object")
    if not isinstance(request.get("policy_baseline"), dict):
        raise A100Error("A100 requires policy_baseline as an object")


async def run_a100_trace_auditor(request: dict[str, Any]) -> RunResult:
    """Trace Auditor — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "trace_bundle": request["trace_bundle"],
        "policy_baseline": request["policy_baseline"],
        "tool_allowlist": request.get("tool_allowlist") or {},
        "known_exceptions": request.get("known_exceptions") or {},
        "prior_audit": request.get("prior_audit") or {},
        "sensitivity_tags": request.get("sensitivity_tags") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No trace mutation",
            "No secret exposure",
            "Findings must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A100",
        "Audit the trace_bundle against the policy_baseline. Produce audit_summary, policy_findings, tool_findings, data_handling_findings and recommendations. Return ONLY A100 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A100Error("A100 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Escalate critical policy findings; feed patterns to Runtime Quality Monitor (A101).")
    missing = REQUIRED - set(output)
    if missing:
        raise A100Error(f"A100 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A100Error("A100 confidence must be high, medium, or low")
    for f in ["policy_findings", "tool_findings", "data_handling_findings", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A100Error(f"A100 {f} must be an array")
    if not isinstance(output.get("audit_summary"), dict):
        raise A100Error("A100 audit_summary must be an object")
    return RunResult(llm.run_id, "A100", "a100.ollama", "completed", result=output)
