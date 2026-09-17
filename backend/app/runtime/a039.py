from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A039LeadScoringError(RuntimeError): pass
REQUIRED = {"status","scores","score_breakdown","priority_order","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("verified_records", "qualification_scoring_strategy"):
        if not isinstance(request.get(name), dict):
            raise A039LeadScoringError(f"A039 requires {name} as an object")

async def run_a039_lead_scoring(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"verified_records": request["verified_records"], "qualification_scoring_strategy": request["qualification_scoring_strategy"], "icp_definition": request.get("icp_definition") or {}, "data_quality_report": request.get("data_quality_report") or {}, "scoring_constraints": request.get("scoring_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A039", "Score leads on ICP fit, intent and data quality. Return ONLY A039 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A039LeadScoringError("A039 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass scored leads to Account Research (A041).")
    missing = REQUIRED - set(output)
    if missing: raise A039LeadScoringError(f"A039 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A039LeadScoringError("A039 confidence must be high, medium, or low")
    for f in ["scores", "score_breakdown", "priority_order", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A039LeadScoringError(f"A039 {f} must be an array")
    return RunResult(llm.run_id, "A039", "lead.scoring+ollama", "completed", result=output)
