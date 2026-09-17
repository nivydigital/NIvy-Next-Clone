from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A024AnalyticsReportingError(RuntimeError): pass
REQUIRED = {"status","report_hierarchy","kpi_definitions","data_ownership","decision_cadence","dashboard_outline","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("revenue_operations_strategy", "gtm_strategy"):
        if not isinstance(request.get(name), dict):
            raise A024AnalyticsReportingError(f"A024 requires {name} as an object")

async def run_a024_analytics(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"revenue_operations_strategy": request["revenue_operations_strategy"], "gtm_strategy": request["gtm_strategy"], "pipeline_deal_strategy": request.get("pipeline_deal_strategy") or {}, "campaign_strategy": request.get("campaign_strategy") or {}, "analytics_constraints": request.get("analytics_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A024", "Define analytics model, report hierarchy and decision cadence from the supplied RevOps and GTM context. Return ONLY A024 JSON.", "PR030", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A024AnalyticsReportingError("A024 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass analytics strategy to BI and operations agents.")
    missing = REQUIRED - set(output)
    if missing: raise A024AnalyticsReportingError(f"A024 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A024AnalyticsReportingError("A024 confidence must be high, medium, or low")
    for f in ["report_hierarchy", "kpi_definitions", "data_ownership", "dashboard_outline", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A024AnalyticsReportingError(f"A024 {f} must be an array")
    if not isinstance(output.get("decision_cadence"), dict): raise A024AnalyticsReportingError("A024 decision_cadence must be an object")
    return RunResult(llm.run_id, "A024", "analytics.reporting+ollama", "completed", result=output)
