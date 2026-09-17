from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A052ReplyTriageError(RuntimeError): pass
REQUIRED = {"status","classification","recommended_action","urgency","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("inbound_message"), dict):
        raise A052ReplyTriageError("A052 requires inbound_message as an object")

async def run_a052_reply_triage(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"inbound_message": request["inbound_message"], "conversation_context": request.get("conversation_context") or {}, "triage_rules": request.get("triage_rules") or [], "triage_constraints": request.get("triage_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A052", "Classify inbound reply and recommend next action. Return ONLY A052 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A052ReplyTriageError("A052 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route triage result to Qualification (A054) or Response Drafting.")
    missing = REQUIRED - set(output)
    if missing: raise A052ReplyTriageError(f"A052 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A052ReplyTriageError("A052 confidence must be high, medium, or low")
    for f in ["assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A052ReplyTriageError(f"A052 {f} must be an array")
    return RunResult(llm.run_id, "A052", "reply.triage+ollama", "completed", result=output)
