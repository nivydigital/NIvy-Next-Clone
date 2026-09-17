from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A068ResponseDraftingError(RuntimeError): pass
REQUIRED = {"status","draft","tone","compliance_checks","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("inbound_triage", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A068ResponseDraftingError(f"A068 requires {name} as an object")

async def run_a068_response_draft(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"inbound_triage": request["inbound_triage"], "messaging_positioning": request["messaging_positioning"], "conversation_insights": request.get("conversation_insights") or {}, "account_context": request.get("account_context") or {}, "response_constraints": request.get("response_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A068", "Draft outbound response from triage and messaging. Return ONLY A068 JSON.", "PR004", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A068ResponseDraftingError("A068 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route draft to Communication Quality Reviewer (A071) or approval.")
    missing = REQUIRED - set(output)
    if missing: raise A068ResponseDraftingError(f"A068 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A068ResponseDraftingError("A068 confidence must be high, medium, or low")
    for f in ["compliance_checks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A068ResponseDraftingError(f"A068 {f} must be an array")
    return RunResult(llm.run_id, "A068", "response.drafting+ollama", "completed", result=output)
