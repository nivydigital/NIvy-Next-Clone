from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A006MessagingPositioningError(RuntimeError): pass

REQUIRED = {
    "status",
    "positioning_statement",
    "value_propositions",
    "messaging_pillars",
    "proof_points",
    "objections_and_responses",
    "tone_and_voice",
    "confidence",
    "assumptions",
    "derived_from",
    "warnings",
    "errors",
    "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "buyer_personas"):
        if not isinstance(request.get(name), dict):
            raise A006MessagingPositioningError(f"A006 requires {name} as an object")

async def run_a006_messaging(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "buyer_personas": request["buyer_personas"],
        "market_research": request.get("market_research") or {},
        "competitor_intelligence": request.get("competitor_intelligence") or {},
        "channel_strategy": request.get("channel_strategy") or {},
        "business_offer": request.get("business_offer") or {},
        "brand_constraints": request.get("brand_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A006",
        "Build evidence-backed messaging pillars, value propositions and positioning from the supplied ICP, personas and strategy context. Return ONLY A006 JSON.",
        "PR012",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A006MessagingPositioningError("A006 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass messaging and positioning to content, outreach and campaign agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A006MessagingPositioningError(f"A006 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A006MessagingPositioningError("A006 confidence must be high, medium, or low")
    for f in ["value_propositions", "messaging_pillars", "proof_points", "objections_and_responses", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A006MessagingPositioningError(f"A006 {f} must be an array")
    if not isinstance(output.get("positioning_statement"), str) or not output["positioning_statement"].strip():
        raise A006MessagingPositioningError("A006 positioning_statement must be a non-empty string")
    if not isinstance(output.get("tone_and_voice"), dict):
        raise A006MessagingPositioningError("A006 tone_and_voice must be an object")
    return RunResult(llm.run_id, "A006", "messaging.positioning+ollama", "completed", result=output)
