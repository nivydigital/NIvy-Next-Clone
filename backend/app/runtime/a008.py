from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A008OfferPricingError(RuntimeError): pass

REQUIRED = {
    "status", "offers", "packaging", "pricing_guidance", "differentiation",
    "objections", "confidence", "assumptions", "derived_from",
    "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "business_offer"):
        if not isinstance(request.get(name), dict):
            raise A008OfferPricingError(f"A008 requires {name} as an object")

async def run_a008_offer(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "business_offer": request["business_offer"],
        "buyer_personas": request.get("buyer_personas") or {},
        "competitor_intelligence": request.get("competitor_intelligence") or {},
        "messaging_positioning": request.get("messaging_positioning") or {},
        "market_research": request.get("market_research") or {},
        "pricing_constraints": request.get("pricing_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A008",
        "Build an evidence-backed offer and pricing strategy from the supplied ICP, business offer and competitor context. Return ONLY A008 JSON.",
        "PR014",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A008OfferPricingError("A008 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass offer and pricing strategy to GTM and sales enablement agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A008OfferPricingError(f"A008 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A008OfferPricingError("A008 confidence must be high, medium, or low")
    for f in ["offers", "packaging", "differentiation", "objections", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A008OfferPricingError(f"A008 {f} must be an array")
    if not isinstance(output.get("pricing_guidance"), dict):
        raise A008OfferPricingError("A008 pricing_guidance must be an object")
    return RunResult(llm.run_id, "A008", "offer.pricing+ollama", "completed", result=output)
