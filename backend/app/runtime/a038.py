from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A038VerificationError(RuntimeError): pass
REQUIRED = {"status","verified_records","failed_checks","evidence","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("enriched_leads"), dict):
        raise A038VerificationError("A038 requires enriched_leads as an object")

async def run_a038_verification(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"enriched_leads": request["enriched_leads"], "data_quality_report": request.get("data_quality_report") or {}, "verification_fields": request.get("verification_fields") or [], "verification_constraints": request.get("verification_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A038", "Verify critical lead and contact attributes against public evidence. Return ONLY A038 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A038VerificationError("A038 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass verified records to Lead Scoring (A039).")
    missing = REQUIRED - set(output)
    if missing: raise A038VerificationError(f"A038 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A038VerificationError("A038 confidence must be high, medium, or low")
    for f in ["verified_records", "failed_checks", "evidence", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A038VerificationError(f"A038 {f} must be an array")
    return RunResult(llm.run_id, "A038", "verification+ollama", "completed", result=output)
