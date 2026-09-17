from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A054QualificationError(RuntimeError): pass
REQUIRED = {"status","status_per_lead","criteria_met","handoff_recommendation","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("scored_leads", "qualification_scoring_strategy"):
        if not isinstance(request.get(name), dict):
            raise A054QualificationError(f"A054 requires {name} as an object")

async def run_a054_qualification(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"scored_leads": request["scored_leads"], "qualification_scoring_strategy": request["qualification_scoring_strategy"], "triage_result": request.get("triage_result") or {}, "conversation_context": request.get("conversation_context") or {}, "qualification_constraints": request.get("qualification_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A054", "Apply qualification criteria and recommend handoff. Return ONLY A054 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A054QualificationError("A054 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass qualification result to Meeting Prep (A055).")
    missing = REQUIRED - set(output)
    if missing: raise A054QualificationError(f"A054 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A054QualificationError("A054 confidence must be high, medium, or low")
    for f in ["status_per_lead", "criteria_met", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A054QualificationError(f"A054 {f} must be an array")
    if not isinstance(output.get("handoff_recommendation"), dict): raise A054QualificationError("A054 handoff_recommendation must be an object")
    return RunResult(llm.run_id, "A054", "qualification+ollama", "completed", result=output)
