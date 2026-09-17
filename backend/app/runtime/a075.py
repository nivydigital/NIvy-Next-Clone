from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A075CSPlannerError(RuntimeError): pass
REQUIRED = {"status","motions","timeline","owners","success_metrics","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("health_assessment"), dict):
        raise A075CSPlannerError("A075 requires health_assessment as an object")

async def run_a075_cs_planner(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"health_assessment": request["health_assessment"], "onboarding_schedule": request.get("onboarding_schedule") or {}, "account_context": request.get("account_context") or {}, "planning_constraints": request.get("planning_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A075", "Plan CS motions from health assessment. Return ONLY A075 JSON.", "PR003", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A075CSPlannerError("A075 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass CS plan to Renewal Risk Analyst (A076) or CS team.")
    missing = REQUIRED - set(output)
    if missing: raise A075CSPlannerError(f"A075 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A075CSPlannerError("A075 confidence must be high, medium, or low")
    for f in ["motions", "owners", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A075CSPlannerError(f"A075 {f} must be an array")
    if not isinstance(output.get("timeline"), dict): raise A075CSPlannerError("A075 timeline must be an object")
    return RunResult(llm.run_id, "A075", "cs.planner+ollama", "completed", result=output)
