from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A011SalesEnablementError(RuntimeError): pass

REQUIRED = {
    "status", "talk_tracks", "objection_handling", "qualification_rules",
    "playbooks", "battlecards_outline", "confidence", "assumptions",
    "derived_from", "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "messaging_positioning", "offer_pricing_strategy"):
        if not isinstance(request.get(name), dict):
            raise A011SalesEnablementError(f"A011 requires {name} as an object")

async def run_a011_sales_enablement(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "messaging_positioning": request["messaging_positioning"],
        "offer_pricing_strategy": request["offer_pricing_strategy"],
        "buyer_personas": request.get("buyer_personas") or {},
        "competitor_intelligence": request.get("competitor_intelligence") or {},
        "gtm_strategy": request.get("gtm_strategy") or {},
        "sales_constraints": request.get("sales_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A011",
        "Build sales enablement guidance (talk tracks, objections, playbooks) from the supplied strategy context. Return ONLY A011 JSON.",
        "PR017",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A011SalesEnablementError("A011 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass sales enablement assets to sales, onboarding and training agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A011SalesEnablementError(f"A011 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A011SalesEnablementError("A011 confidence must be high, medium, or low")
    for f in ["talk_tracks", "objection_handling", "qualification_rules", "playbooks", "battlecards_outline", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A011SalesEnablementError(f"A011 {f} must be an array")
    return RunResult(llm.run_id, "A011", "sales.enablement+ollama", "completed", result=output)
