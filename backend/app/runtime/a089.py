from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A089MarketingAnalyticsError(RuntimeError): pass
REQUIRED = {"status","channel_summary","top_insights","recommended_experiments","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("marketing_performance"), dict):
        raise A089MarketingAnalyticsError("A089 requires marketing_performance as an object")

async def run_a089_marketing_analytics(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"marketing_performance": request["marketing_performance"], "marketing_strategy": request.get("marketing_strategy") or {}, "attribution_notes": request.get("attribution_notes") or {}, "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A089", "Aggregate marketing performance and recommend experiments. Return ONLY A089 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A089MarketingAnalyticsError("A089 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass experiments to Growth Experiment Planner (A090) or Campaign QA (A091).")
    missing = REQUIRED - set(output)
    if missing: raise A089MarketingAnalyticsError(f"A089 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A089MarketingAnalyticsError("A089 confidence must be high, medium, or low")
    for f in ["channel_summary", "top_insights", "recommended_experiments", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A089MarketingAnalyticsError(f"A089 {f} must be an array")
    return RunResult(llm.run_id, "A089", "marketing.analytics+ollama", "completed", result=output)
