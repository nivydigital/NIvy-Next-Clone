from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A067ConversationIntelError(RuntimeError): pass
REQUIRED = {"status","summary","objections","commitments","sentiment","next_best_actions","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("conversation_transcript"), dict):
        raise A067ConversationIntelError("A067 requires conversation_transcript as an object")

async def run_a067_conversation_intel(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"conversation_transcript": request["conversation_transcript"], "account_context": request.get("account_context") or {}, "analysis_focus": request.get("analysis_focus") or [], "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A067", "Extract conversation insights, objections and next actions. Return ONLY A067 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A067ConversationIntelError("A067 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass insights to Response Drafting (A068) or Qualification (A054).")
    missing = REQUIRED - set(output)
    if missing: raise A067ConversationIntelError(f"A067 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A067ConversationIntelError("A067 confidence must be high, medium, or low")
    for f in ["objections", "commitments", "next_best_actions", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A067ConversationIntelError(f"A067 {f} must be an array")
    return RunResult(llm.run_id, "A067", "conversation.intel+ollama", "completed", result=output)
