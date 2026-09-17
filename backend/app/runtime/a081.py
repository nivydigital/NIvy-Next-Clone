from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A081CashflowError(RuntimeError): pass
REQUIRED = {"status","projection","shortfall_flags","surplus_opportunities","recommendations","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("ar_analysis", "ap_analysis"):
        if not isinstance(request.get(name), dict):
            raise A081CashflowError(f"A081 requires {name} as an object")

async def run_a081_cashflow(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"ar_analysis": request["ar_analysis"], "ap_analysis": request["ap_analysis"], "operating_forecast": request.get("operating_forecast") or {}, "cashflow_constraints": request.get("cashflow_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A081", "Project cashflow and flag shortfalls/surplus. Return ONLY A081 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A081CashflowError("A081 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Share with Pricing Analyst (A082) or finance leadership.")
    missing = REQUIRED - set(output)
    if missing: raise A081CashflowError(f"A081 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A081CashflowError("A081 confidence must be high, medium, or low")
    for f in ["shortfall_flags", "surplus_opportunities", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A081CashflowError(f"A081 {f} must be an array")
    if not isinstance(output.get("projection"), dict): raise A081CashflowError("A081 projection must be an object")
    return RunResult(llm.run_id, "A081", "cashflow+ollama", "completed", result=output)
