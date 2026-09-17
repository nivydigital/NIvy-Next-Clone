from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A095RiskError(RuntimeError): pass
REQUIRED = {"status","risks","severity","mitigations","residual_risk","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("risk_signals"), dict):
        raise A095RiskError("A095 requires risk_signals as an object")

async def run_a095_risk(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"risk_signals": request["risk_signals"], "anomaly_report": request.get("anomaly_report") or {}, "kpi_intelligence": request.get("kpi_intelligence") or {}, "risk_constraints": request.get("risk_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A095", "Assess risks and recommend mitigations. Return ONLY A095 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A095RiskError("A095 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass to Executive Intelligence (A096) or ops owners.")
    missing = REQUIRED - set(output)
    if missing: raise A095RiskError(f"A095 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A095RiskError("A095 confidence must be high, medium, or low")
    for f in ["risks", "mitigations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A095RiskError(f"A095 {f} must be an array")
    return RunResult(llm.run_id, "A095", "risk.analyst+ollama", "completed", result=output)
