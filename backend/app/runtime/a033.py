from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A033StrategicPlanningError(RuntimeError): pass
REQUIRED = {"status","priorities","initiatives","resource_guidance","success_metrics","risk_register","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("gtm_strategy", "revenue_operations_strategy"):
        if not isinstance(request.get(name), dict):
            raise A033StrategicPlanningError(f"A033 requires {name} as an object")

async def run_a033_strategic_plan(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"gtm_strategy": request["gtm_strategy"], "revenue_operations_strategy": request["revenue_operations_strategy"], "experiment_growth_plan": request.get("experiment_growth_plan") or {}, "continuous_improvement_strategy": request.get("continuous_improvement_strategy") or {}, "brand_strategy": request.get("brand_strategy") or {}, "planning_constraints": request.get("planning_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A033", "Synthesize strategic priorities, initiatives and success metrics from the supplied GTM and RevOps context. Return ONLY A033 JSON.", "PR039", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A033StrategicPlanningError("A033 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass strategic plan to leadership, operations and execution agents.")
    missing = REQUIRED - set(output)
    if missing: raise A033StrategicPlanningError(f"A033 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A033StrategicPlanningError("A033 confidence must be high, medium, or low")
    for f in ["priorities", "initiatives", "success_metrics", "risk_register", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A033StrategicPlanningError(f"A033 {f} must be an array")
    if not isinstance(output.get("resource_guidance"), dict): raise A033StrategicPlanningError("A033 resource_guidance must be an object")
    return RunResult(llm.run_id, "A033", "strategic.planning+ollama", "completed", result=output)
