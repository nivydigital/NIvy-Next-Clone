from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A080APAnalystError(RuntimeError): pass
REQUIRED = {"status","due_summary","payment_priorities","risk_flags","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("ap_records"), dict):
        raise A080APAnalystError("A080 requires ap_records as an object")

async def run_a080_ap_analyst(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"ap_records": request["ap_records"], "cash_position": request.get("cash_position") or {}, "payment_policy": request.get("payment_policy") or {}, "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A080", "Analyze AP and prioritize payments. Return ONLY A080 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A080APAnalystError("A080 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass AP analysis to Cashflow Analyst (A081).")
    missing = REQUIRED - set(output)
    if missing: raise A080APAnalystError(f"A080 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A080APAnalystError("A080 confidence must be high, medium, or low")
    for f in ["payment_priorities", "risk_flags", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A080APAnalystError(f"A080 {f} must be an array")
    if not isinstance(output.get("due_summary"), dict): raise A080APAnalystError("A080 due_summary must be an object")
    return RunResult(llm.run_id, "A080", "ap.analyst+ollama", "completed", result=output)
