from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A055MeetingPrepError(RuntimeError): pass
REQUIRED = {"status","agenda","talking_points","risks","questions","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("account_research", "qualification_result"):
        if not isinstance(request.get(name), dict):
            raise A055MeetingPrepError(f"A055 requires {name} as an object")

async def run_a055_meeting_prep(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"account_research": request["account_research"], "qualification_result": request["qualification_result"], "conversation_context": request.get("conversation_context") or {}, "messaging_positioning": request.get("messaging_positioning") or {}, "meeting_constraints": request.get("meeting_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A055", "Prepare meeting brief with agenda, talking points and questions. Return ONLY A055 JSON.", "PR003", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A055MeetingPrepError("A055 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass meeting brief to Proposal Agent (A060) or sales user.")
    missing = REQUIRED - set(output)
    if missing: raise A055MeetingPrepError(f"A055 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A055MeetingPrepError("A055 confidence must be high, medium, or low")
    for f in ["agenda", "talking_points", "risks", "questions", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A055MeetingPrepError(f"A055 {f} must be an array")
    return RunResult(llm.run_id, "A055", "meeting.prep+ollama", "completed", result=output)
