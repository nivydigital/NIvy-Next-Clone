from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A028ContinuousImprovementError(RuntimeError): pass
REQUIRED = {"status","learning_loops","experiment_to_scale","retrospective_cadence","improvement_ownership","prioritization_rules","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("experiment_growth_plan", "revenue_operations_strategy"):
        if not isinstance(request.get(name), dict):
            raise A028ContinuousImprovementError(f"A028 requires {name} as an object")

async def run_a028_improvement(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"experiment_growth_plan": request["experiment_growth_plan"], "revenue_operations_strategy": request["revenue_operations_strategy"], "analytics_reporting_strategy": request.get("analytics_reporting_strategy") or {}, "feedback_insights_strategy": request.get("feedback_insights_strategy") or {}, "improvement_constraints": request.get("improvement_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A028", "Define learning loops, experiment-to-scale process and improvement ownership from the supplied experiment and RevOps context. Return ONLY A028 JSON.", "PR034", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A028ContinuousImprovementError("A028 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass continuous improvement strategy to growth and operations agents.")
    missing = REQUIRED - set(output)
    if missing: raise A028ContinuousImprovementError(f"A028 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A028ContinuousImprovementError("A028 confidence must be high, medium, or low")
    for f in ["learning_loops", "improvement_ownership", "prioritization_rules", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A028ContinuousImprovementError(f"A028 {f} must be an array")
    for f in ["experiment_to_scale", "retrospective_cadence"]:
        if not isinstance(output.get(f), dict): raise A028ContinuousImprovementError(f"A028 {f} must be an object")
    return RunResult(llm.run_id, "A028", "continuous.improvement+ollama", "completed", result=output)
