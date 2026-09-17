from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A099Error(RuntimeError):
    pass


REQUIRED = {
    "regression_verdict", "delta_summary", "severity", "evidence", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("baseline_results"), dict):
        raise A099Error("A099 requires baseline_results as an object")
    if not isinstance(request.get("candidate_results"), dict):
        raise A099Error("A099 requires candidate_results as an object")


async def run_a099_regression_qa(request: dict[str, Any]) -> RunResult:
    """Regression QA Agent — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "baseline_results": request["baseline_results"],
        "candidate_results": request["candidate_results"],
        "thresholds": request.get("thresholds") or {},
        "affected_agents": request.get("affected_agents") or {},
        "prior_regression_report": request.get("prior_regression_report") or {},
        "change_context": request.get("change_context") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No automatic rollback",
            "No secret exposure",
            "Severity must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A099",
        "Compare candidate_results to baseline_results for regressions. Produce regression_verdict, delta_summary, severity, evidence and recommendations. Return ONLY A099 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A099Error("A099 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "If severity high, block promotion and notify Regression Guard (A108); else pass to human review.")
    missing = REQUIRED - set(output)
    if missing:
        raise A099Error(f"A099 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A099Error("A099 confidence must be high, medium, or low")
    for f in ["evidence", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A099Error(f"A099 {f} must be an array")
    for f in ["regression_verdict", "delta_summary", "severity"]:
        if not isinstance(output.get(f), dict):
            raise A099Error(f"A099 {f} must be an object")
    return RunResult(llm.run_id, "A099", "a099.ollama", "completed", result=output)
