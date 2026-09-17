from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A050FollowUpError(RuntimeError): pass
REQUIRED = {"status","drafts","trigger_reason","timing_guidance","compliance_checks","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("email_drafts", "account_research"):
        if not isinstance(request.get(name), dict):
            raise A050FollowUpError(f"A050 requires {name} as an object")

async def run_a050_follow_up(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"email_drafts": request["email_drafts"], "account_research": request["account_research"], "outreach_plan": request.get("outreach_plan") or {}, "conversation_context": request.get("conversation_context") or {}, "follow_up_constraints": request.get("follow_up_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A050", "Draft context-aware follow-up messages. Do not send. Return ONLY A050 JSON.", "PR004", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A050FollowUpError("A050 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route follow-up drafts to approval or Reply Triage (A052).")
    missing = REQUIRED - set(output)
    if missing: raise A050FollowUpError(f"A050 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A050FollowUpError("A050 confidence must be high, medium, or low")
    for f in ["drafts", "compliance_checks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A050FollowUpError(f"A050 {f} must be an array")
    return RunResult(llm.run_id, "A050", "follow.up+ollama", "completed", result=output)
