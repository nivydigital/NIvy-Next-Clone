from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A079ARAnalystError(RuntimeError): pass
REQUIRED = {"status","priority_accounts","aging_summary","collection_actions","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("ar_aging"), dict):
        raise A079ARAnalystError("A079 requires ar_aging as an object")

async def run_a079_ar_analyst(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"ar_aging": request["ar_aging"], "customer_health": request.get("customer_health") or {}, "collection_policy": request.get("collection_policy") or {}, "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A079", "Analyze AR aging and recommend collection priorities. Return ONLY A079 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A079ARAnalystError("A079 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Execute collection actions via finance ops or AP Analyst (A080).")
    missing = REQUIRED - set(output)
    if missing: raise A079ARAnalystError(f"A079 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A079ARAnalystError("A079 confidence must be high, medium, or low")
    for f in ["priority_accounts", "collection_actions", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A079ARAnalystError(f"A079 {f} must be an array")
    if not isinstance(output.get("aging_summary"), dict): raise A079ARAnalystError("A079 aging_summary must be an object")
    return RunResult(llm.run_id, "A079", "ar.analyst+ollama", "completed", result=output)
