from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A102Error(RuntimeError):
    pass


REQUIRED = {
    "cost_summary", "unit_costs", "anomalies", "optimization_opportunities", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("cost_snapshot"), dict):
        raise A102Error("A102 requires cost_snapshot as an object")
    if not isinstance(request.get("workload_context"), dict):
        raise A102Error("A102 requires workload_context as an object")


async def run_a102_cost_observability(request: dict[str, Any]) -> RunResult:
    """Cost Observability Analyst — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "cost_snapshot": request["cost_snapshot"],
        "workload_context": request["workload_context"],
        "budget_targets": request.get("budget_targets") or {},
        "historical_spend": request.get("historical_spend") or {},
        "pricing_model": request.get("pricing_model") or {},
        "prior_cost_report": request.get("prior_cost_report") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No billing or infra mutation",
            "No secret exposure",
            "Recommendations must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A102",
        "Analyze cost observability from the cost_snapshot and workload_context. Produce cost_summary, unit_costs, anomalies, optimization_opportunities and recommendations. Return ONLY A102 JSON.",
        "PR002",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A102Error("A102 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Share anomalies with Runtime Quality Monitor (A101); queue high-value optimizations for human review.")
    missing = REQUIRED - set(output)
    if missing:
        raise A102Error(f"A102 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A102Error("A102 confidence must be high, medium, or low")
    for f in ["unit_costs", "anomalies", "optimization_opportunities", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A102Error(f"A102 {f} must be an array")
    if not isinstance(output.get("cost_summary"), dict):
        raise A102Error("A102 cost_summary must be an object")
    return RunResult(llm.run_id, "A102", "a102.ollama", "completed", result=output)
