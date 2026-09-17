from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A093PlanningError(RuntimeError): pass
REQUIRED = {"status","priorities","workstreams","owners","checkpoints","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("goals"), dict):
        raise A093PlanningError("A093 requires goals as an object")

async def run_a093_planning(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"goals": request["goals"], "kpi_intelligence": request.get("kpi_intelligence") or {}, "resource_constraints": request.get("resource_constraints") or [], "planning_constraints": request.get("planning_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A093", "Turn goals into prioritized plan with owners and checkpoints. Return ONLY A093 JSON.", "PR001", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A093PlanningError("A093 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass plan to Resource Planning (A097) or executive review.")
    missing = REQUIRED - set(output)
    if missing: raise A093PlanningError(f"A093 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A093PlanningError("A093 confidence must be high, medium, or low")
    for f in ["priorities", "workstreams", "owners", "checkpoints", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A093PlanningError(f"A093 {f} must be an array")
    return RunResult(llm.run_id, "A093", "planning+ollama", "completed", result=output)
