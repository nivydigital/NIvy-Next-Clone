from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A022FeedbackInsightsError(RuntimeError): pass

REQUIRED = {"status","collection_methods","nps_csat_approach","insight_synthesis","closed_loop_actions","reporting","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("customer_health_strategy", "retention_expansion_strategy"):
        if not isinstance(request.get(name), dict):
            raise A022FeedbackInsightsError(f"A022 requires {name} as an object")

async def run_a022_feedback(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"customer_health_strategy": request["customer_health_strategy"], "retention_expansion_strategy": request["retention_expansion_strategy"], "onboarding_strategy": request.get("onboarding_strategy") or {}, "feedback_constraints": request.get("feedback_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A022", "Define feedback collection, NPS/CSAT approach and closed-loop actions from the supplied health and retention context. Return ONLY A022 JSON.", "PR028", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A022FeedbackInsightsError("A022 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass feedback strategy to survey, analytics and product agents.")
    missing = REQUIRED - set(output)
    if missing: raise A022FeedbackInsightsError(f"A022 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A022FeedbackInsightsError("A022 confidence must be high, medium, or low")
    for f in ["collection_methods", "closed_loop_actions", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A022FeedbackInsightsError(f"A022 {f} must be an array")
    for f in ["nps_csat_approach", "insight_synthesis", "reporting"]:
        if not isinstance(output.get(f), dict): raise A022FeedbackInsightsError(f"A022 {f} must be an object")
    return RunResult(llm.run_id, "A022", "feedback.insights+ollama", "completed", result=output)
