from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A088PaidMediaError(RuntimeError): pass
REQUIRED = {"status","performance_summary","budget_recommendations","creative_recommendations","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("paid_media_performance"), dict):
        raise A088PaidMediaError("A088 requires paid_media_performance as an object")

async def run_a088_paid_media(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"paid_media_performance": request["paid_media_performance"], "marketing_strategy": request.get("marketing_strategy") or {}, "budget_constraints": request.get("budget_constraints") or [], "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A088", "Analyze paid media and recommend budget/creative changes. Return ONLY A088 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A088PaidMediaError("A088 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass to Marketing Analytics (A089) or Growth Experiment Planner (A090).")
    missing = REQUIRED - set(output)
    if missing: raise A088PaidMediaError(f"A088 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A088PaidMediaError("A088 confidence must be high, medium, or low")
    for f in ["budget_recommendations", "creative_recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A088PaidMediaError(f"A088 {f} must be an array")
    if not isinstance(output.get("performance_summary"), dict): raise A088PaidMediaError("A088 performance_summary must be an object")
    return RunResult(llm.run_id, "A088", "paid.media+ollama", "completed", result=output)
