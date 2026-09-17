from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A092KPIError(RuntimeError): pass
REQUIRED = {"status","variance_summary","drivers","recommended_actions","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("kpi_pack"), dict):
        raise A092KPIError("A092 requires kpi_pack as an object")

async def run_a092_kpi_intelligence(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"kpi_pack": request["kpi_pack"], "targets": request.get("targets") or {}, "prior_period": request.get("prior_period") or {}, "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A092", "Interpret KPIs vs targets and recommend actions. Return ONLY A092 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A092KPIError("A092 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass to Planning Analyst (A093) or Anomaly Detection (A094).")
    missing = REQUIRED - set(output)
    if missing: raise A092KPIError(f"A092 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A092KPIError("A092 confidence must be high, medium, or low")
    for f in ["drivers", "recommended_actions", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A092KPIError(f"A092 {f} must be an array")
    if not isinstance(output.get("variance_summary"), dict): raise A092KPIError("A092 variance_summary must be an object")
    return RunResult(llm.run_id, "A092", "kpi.intelligence+ollama", "completed", result=output)
