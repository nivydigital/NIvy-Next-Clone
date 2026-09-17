from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A066InboundTriageError(RuntimeError): pass
REQUIRED = {"status","intent","urgency","route_to","summary","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("inbound_message"), dict):
        raise A066InboundTriageError("A066 requires inbound_message as an object")

async def run_a066_inbound_triage(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"inbound_message": request["inbound_message"], "channel_metadata": request.get("channel_metadata") or {}, "triage_rules": request.get("triage_rules") or [], "triage_constraints": request.get("triage_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A066", "Triage inbound communication by intent, urgency and route. Return ONLY A066 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A066InboundTriageError("A066 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route to Response Drafting (A068) or Support Triage (A074).")
    missing = REQUIRED - set(output)
    if missing: raise A066InboundTriageError(f"A066 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A066InboundTriageError("A066 confidence must be high, medium, or low")
    for f in ["assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A066InboundTriageError(f"A066 {f} must be an array")
    return RunResult(llm.run_id, "A066", "inbound.triage+ollama", "completed", result=output)
