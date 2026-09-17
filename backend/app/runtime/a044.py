from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A044EmailOutreachError(RuntimeError): pass
REQUIRED = {"status","drafts","personalization_notes","compliance_checks","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("outreach_plan", "account_research"):
        if not isinstance(request.get(name), dict):
            raise A044EmailOutreachError(f"A044 requires {name} as an object")

async def run_a044_email_outreach(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"outreach_plan": request["outreach_plan"], "account_research": request["account_research"], "messaging_positioning": request.get("messaging_positioning") or {}, "personalization_context": request.get("personalization_context") or {}, "email_constraints": request.get("email_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A044", "Draft personalized outreach emails. Do not send. Return ONLY A044 JSON.", "PR004", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A044EmailOutreachError("A044 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route drafts to approval or Follow-Up (A050).")
    missing = REQUIRED - set(output)
    if missing: raise A044EmailOutreachError(f"A044 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A044EmailOutreachError("A044 confidence must be high, medium, or low")
    for f in ["drafts", "personalization_notes", "compliance_checks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A044EmailOutreachError(f"A044 {f} must be an array")
    return RunResult(llm.run_id, "A044", "email.outreach+ollama", "completed", result=output)
