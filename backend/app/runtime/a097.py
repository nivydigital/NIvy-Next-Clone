from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A097ResourceError(RuntimeError): pass
REQUIRED = {"status","allocations","gaps","reallocation_options","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("operational_plan"), dict):
        raise A097ResourceError("A097 requires operational_plan as an object")

async def run_a097_resource_planning(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"operational_plan": request["operational_plan"], "resource_inventory": request.get("resource_inventory") or {}, "capacity_constraints": request.get("capacity_constraints") or [], "planning_constraints": request.get("planning_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A097", "Map plan to resources; flag gaps and reallocation options. Return ONLY A097 JSON.", "PR001", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A097ResourceError("A097 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Present resource plan to leadership or Evaluation Analyst (A098).")
    missing = REQUIRED - set(output)
    if missing: raise A097ResourceError(f"A097 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A097ResourceError("A097 confidence must be high, medium, or low")
    for f in ["allocations", "gaps", "reallocation_options", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A097ResourceError(f"A097 {f} must be an array")
    return RunResult(llm.run_id, "A097", "resource.planning+ollama", "completed", result=output)
