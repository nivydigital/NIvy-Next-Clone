from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A096ExecIntelError(RuntimeError): pass
REQUIRED = {"status","summary","key_decisions","asks","risks_opportunities","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("signal_pack"), dict):
        raise A096ExecIntelError("A096 requires signal_pack as an object")

async def run_a096_exec_intel(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"signal_pack": request["signal_pack"], "kpi_intelligence": request.get("kpi_intelligence") or {}, "risk_assessment": request.get("risk_assessment") or {}, "briefing_constraints": request.get("briefing_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A096", "Synthesize executive brief with decisions and asks. Return ONLY A096 JSON.", "PR001", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A096ExecIntelError("A096 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Deliver brief to leadership; optional Resource Planning (A097).")
    missing = REQUIRED - set(output)
    if missing: raise A096ExecIntelError(f"A096 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A096ExecIntelError("A096 confidence must be high, medium, or low")
    for f in ["key_decisions", "asks", "risks_opportunities", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A096ExecIntelError(f"A096 {f} must be an array")
    return RunResult(llm.run_id, "A096", "exec.intelligence+ollama", "completed", result=output)
