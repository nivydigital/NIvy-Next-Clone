from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A090ExperimentError(RuntimeError): pass
REQUIRED = {"status","hypotheses","variants","success_metrics","run_plan","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("marketing_insights"), dict):
        raise A090ExperimentError("A090 requires marketing_insights as an object")

async def run_a090_experiment_planner(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"marketing_insights": request["marketing_insights"], "marketing_strategy": request.get("marketing_strategy") or {}, "experiment_constraints": request.get("experiment_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A090", "Design growth experiments with hypotheses and run plan. Return ONLY A090 JSON.", "PR001", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A090ExperimentError("A090 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route plan to Campaign QA (A091) or Experiment Manager (A107).")
    missing = REQUIRED - set(output)
    if missing: raise A090ExperimentError(f"A090 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A090ExperimentError("A090 confidence must be high, medium, or low")
    for f in ["hypotheses", "variants", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A090ExperimentError(f"A090 {f} must be an array")
    if not isinstance(output.get("run_plan"), dict): raise A090ExperimentError("A090 run_plan must be an object")
    return RunResult(llm.run_id, "A090", "experiment.planner+ollama", "completed", result=output)
