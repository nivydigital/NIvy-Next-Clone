from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A020CustomerHealthError(RuntimeError): pass

REQUIRED = {"status","health_dimensions","leading_indicators","scoring_rules","intervention_triggers","reporting_cadence","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("retention_expansion_strategy", "onboarding_strategy"):
        if not isinstance(request.get(name), dict):
            raise A020CustomerHealthError(f"A020 requires {name} as an object")

async def run_a020_health(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"retention_expansion_strategy": request["retention_expansion_strategy"], "onboarding_strategy": request["onboarding_strategy"], "icp_definition": request.get("icp_definition") or {}, "historical_health": request.get("historical_health") or {}, "health_constraints": request.get("health_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A020", "Define customer health model, indicators and intervention triggers from the supplied retention and onboarding context. Return ONLY A020 JSON.", "PR026", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A020CustomerHealthError("A020 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass health strategy to monitoring and success agents.")
    missing = REQUIRED - set(output)
    if missing: raise A020CustomerHealthError(f"A020 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A020CustomerHealthError("A020 confidence must be high, medium, or low")
    for f in ["health_dimensions", "leading_indicators", "intervention_triggers", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A020CustomerHealthError(f"A020 {f} must be an array")
    for f in ["scoring_rules", "reporting_cadence"]:
        if not isinstance(output.get(f), dict): raise A020CustomerHealthError(f"A020 {f} must be an object")
    return RunResult(llm.run_id, "A020", "customer.health+ollama", "completed", result=output)
