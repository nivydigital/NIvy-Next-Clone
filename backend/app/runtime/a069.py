from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A069MeetingIntelError(RuntimeError): pass
REQUIRED = {"status","decisions","action_items","risks","follow_ups","summary","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("meeting_notes"), dict):
        raise A069MeetingIntelError("A069 requires meeting_notes as an object")

async def run_a069_meeting_intel(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"meeting_notes": request["meeting_notes"], "meeting_brief": request.get("meeting_brief") or {}, "account_context": request.get("account_context") or {}, "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A069", "Extract decisions, action items and follow-ups from meeting notes. Return ONLY A069 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A069MeetingIntelError("A069 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass meeting intelligence to Follow-Up (A050) or Communication Knowledge Extractor (A070).")
    missing = REQUIRED - set(output)
    if missing: raise A069MeetingIntelError(f"A069 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A069MeetingIntelError("A069 confidence must be high, medium, or low")
    for f in ["decisions", "action_items", "risks", "follow_ups", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A069MeetingIntelError(f"A069 {f} must be an array")
    return RunResult(llm.run_id, "A069", "meeting.intel+ollama", "completed", result=output)
