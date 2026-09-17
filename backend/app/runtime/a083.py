from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A083RevenueError(RuntimeError): pass
REQUIRED = {"status","trend_summary","cohort_insights","drivers","recommendations","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("revenue_records"), dict):
        raise A083RevenueError("A083 requires revenue_records as an object")

async def run_a083_revenue(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"revenue_records": request["revenue_records"], "cohort_definitions": request.get("cohort_definitions") or {}, "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A083", "Analyze revenue trends, cohorts and drivers. Return ONLY A083 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A083RevenueError("A083 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Share with Marketing Strategist (A084) or executive planning.")
    missing = REQUIRED - set(output)
    if missing: raise A083RevenueError(f"A083 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A083RevenueError("A083 confidence must be high, medium, or low")
    for f in ["cohort_insights", "drivers", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A083RevenueError(f"A083 {f} must be an array")
    if not isinstance(output.get("trend_summary"), dict): raise A083RevenueError("A083 trend_summary must be an object")
    return RunResult(llm.run_id, "A083", "revenue.analytics+ollama", "completed", result=output)
