from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A076RenewalRiskError(RuntimeError): pass
REQUIRED = {"status","risk_score","risk_drivers","save_plays","urgency","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("health_assessment"), dict):
        raise A076RenewalRiskError("A076 requires health_assessment as an object")

async def run_a076_renewal_risk(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"health_assessment": request["health_assessment"], "support_history": request.get("support_history") or {}, "commercial_context": request.get("commercial_context") or {}, "risk_constraints": request.get("risk_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A076", "Score renewal risk and recommend save plays. Return ONLY A076 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A076RenewalRiskError("A076 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Execute save plays via CS team or Feedback Analyst (A077).")
    missing = REQUIRED - set(output)
    if missing: raise A076RenewalRiskError(f"A076 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A076RenewalRiskError("A076 confidence must be high, medium, or low")
    for f in ["risk_drivers", "save_plays", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A076RenewalRiskError(f"A076 {f} must be an array")
    return RunResult(llm.run_id, "A076", "renewal.risk+ollama", "completed", result=output)
