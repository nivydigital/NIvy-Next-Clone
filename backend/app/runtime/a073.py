from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A073HealthAnalystError(RuntimeError): pass
REQUIRED = {"status","health_score","risk_flags","expansion_signals","recommended_actions","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("customer_signals"), dict):
        raise A073HealthAnalystError("A073 requires customer_signals as an object")

async def run_a073_health_analyst(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"customer_signals": request["customer_signals"], "health_strategy": request.get("health_strategy") or {}, "account_context": request.get("account_context") or {}, "health_constraints": request.get("health_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A073", "Assess customer health, risks and expansion signals. Return ONLY A073 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A073HealthAnalystError("A073 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route risks to Renewal Risk Analyst (A076) or Support Triage (A074).")
    missing = REQUIRED - set(output)
    if missing: raise A073HealthAnalystError(f"A073 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A073HealthAnalystError("A073 confidence must be high, medium, or low")
    for f in ["risk_flags", "expansion_signals", "recommended_actions", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A073HealthAnalystError(f"A073 {f} must be an array")
    return RunResult(llm.run_id, "A073", "health.analyst+ollama", "completed", result=output)
