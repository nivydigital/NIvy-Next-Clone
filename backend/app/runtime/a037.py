from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A037DataQualityError(RuntimeError): pass
REQUIRED = {"status","quality_score","issues","remediation","pass_fail","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("enriched_leads"), dict):
        raise A037DataQualityError("A037 requires enriched_leads as an object")

async def run_a037_data_quality(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"enriched_leads": request["enriched_leads"], "quality_rules": request.get("quality_rules") or [], "quality_constraints": request.get("quality_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A037", "Assess data quality of enriched leads; flag issues and recommend remediation. Return ONLY A037 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A037DataQualityError("A037 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass quality report to Verification (A038).")
    missing = REQUIRED - set(output)
    if missing: raise A037DataQualityError(f"A037 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A037DataQualityError("A037 confidence must be high, medium, or low")
    for f in ["issues", "remediation", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A037DataQualityError(f"A037 {f} must be an array")
    return RunResult(llm.run_id, "A037", "data.quality+ollama", "completed", result=output)
