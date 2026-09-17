from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A098EvalError(RuntimeError): pass
REQUIRED = {"status","scores","findings","pass_fail","recommendations","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("evaluation_target"), dict):
        raise A098EvalError("A098 requires evaluation_target as an object")

async def run_a098_evaluation(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"evaluation_target": request["evaluation_target"], "rubric": request.get("rubric") or {}, "baseline": request.get("baseline") or {}, "evaluation_constraints": request.get("evaluation_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A098", "Evaluate target against rubric; score and recommend. Return ONLY A098 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A098EvalError("A098 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route failures to Regression QA (A099) or Prompt Improvement (A105).")
    missing = REQUIRED - set(output)
    if missing: raise A098EvalError(f"A098 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A098EvalError("A098 confidence must be high, medium, or low")
    for f in ["findings", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A098EvalError(f"A098 {f} must be an array")
    if not isinstance(output.get("scores"), dict): raise A098EvalError("A098 scores must be an object")
    return RunResult(llm.run_id, "A098", "evaluation+ollama", "completed", result=output)
