from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A078BillingAnalystError(RuntimeError): pass
REQUIRED = {"status","anomalies","dispute_candidates","process_recommendations","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("billing_records"), dict):
        raise A078BillingAnalystError("A078 requires billing_records as an object")

async def run_a078_billing_analyst(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"billing_records": request["billing_records"], "customer_context": request.get("customer_context") or {}, "billing_rules": request.get("billing_rules") or [], "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A078", "Analyze billing for anomalies and disputes. Return ONLY A078 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A078BillingAnalystError("A078 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route disputes to AR Analyst (A079) or finance ops.")
    missing = REQUIRED - set(output)
    if missing: raise A078BillingAnalystError(f"A078 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A078BillingAnalystError("A078 confidence must be high, medium, or low")
    for f in ["anomalies", "dispute_candidates", "process_recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A078BillingAnalystError(f"A078 {f} must be an array")
    return RunResult(llm.run_id, "A078", "billing.analyst+ollama", "completed", result=output)
