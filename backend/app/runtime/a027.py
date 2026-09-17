from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A027PartnerStrategyError(RuntimeError): pass
REQUIRED = {"status","partner_types","value_exchange","enablement_needs","joint_gtm_rules","success_metrics","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("gtm_strategy", "channel_strategy"):
        if not isinstance(request.get(name), dict):
            raise A027PartnerStrategyError(f"A027 requires {name} as an object")

async def run_a027_partner(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"gtm_strategy": request["gtm_strategy"], "channel_strategy": request["channel_strategy"], "offer_pricing_strategy": request.get("offer_pricing_strategy") or {}, "messaging_positioning": request.get("messaging_positioning") or {}, "partner_constraints": request.get("partner_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A027", "Define partner types, value exchange and joint GTM rules from the supplied GTM and channel context. Return ONLY A027 JSON.", "PR033", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A027PartnerStrategyError("A027 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass partner strategy to partner management and enablement agents.")
    missing = REQUIRED - set(output)
    if missing: raise A027PartnerStrategyError(f"A027 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A027PartnerStrategyError("A027 confidence must be high, medium, or low")
    for f in ["partner_types", "enablement_needs", "joint_gtm_rules", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A027PartnerStrategyError(f"A027 {f} must be an array")
    if not isinstance(output.get("value_exchange"), dict): raise A027PartnerStrategyError("A027 value_exchange must be an object")
    return RunResult(llm.run_id, "A027", "partner.strategy+ollama", "completed", result=output)
