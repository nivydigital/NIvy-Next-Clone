from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A108Error(RuntimeError):
    pass


REQUIRED = {
    "regression_status", "affected_areas", "severity", "evidence", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("change_summary"), dict):
        raise A108Error("A108 requires change_summary as an object")
    if not isinstance(request.get("evaluation_snapshot"), dict):
        raise A108Error("A108 requires evaluation_snapshot as an object")


async def run_a108_regression_guard(request: dict[str, Any]) -> RunResult:
    """Regression Guard — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "change_summary": request["change_summary"],
        "evaluation_snapshot": request["evaluation_snapshot"],
        "baseline_metrics": request.get("baseline_metrics") or {},
        "regression_thresholds": request.get("regression_thresholds") or {},
        "prior_guard_report": request.get("prior_guard_report") or {},
        "affected_agents": request.get("affected_agents") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No automatic rollback execution",
            "No secret exposure",
            "Severity must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A108",
        "Assess regression risk from the change_summary and evaluation_snapshot. Produce regression_status, affected_areas, severity, evidence and recommendations. Return ONLY A108 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A108Error("A108 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "If severity is high, block promotion and route to Regression QA (A099); else allow review by A109.")
    missing = REQUIRED - set(output)
    if missing:
        raise A108Error(f"A108 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A108Error("A108 confidence must be high, medium, or low")
    for f in ["affected_areas", "evidence", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A108Error(f"A108 {f} must be an array")
    for f in ["regression_status", "severity"]:
        if not isinstance(output.get(f), dict):
            raise A108Error(f"A108 {f} must be an object")
    return RunResult(llm.run_id, "A108", "a108.ollama", "completed", result=output)
