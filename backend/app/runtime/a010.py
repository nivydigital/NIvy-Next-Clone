from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A010CampaignStrategyError(RuntimeError): pass

REQUIRED = {
    "status", "campaigns", "goals", "audiences", "channel_plan", "sequences",
    "success_metrics", "budget_guidance", "confidence", "assumptions",
    "derived_from", "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("gtm_strategy", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A010CampaignStrategyError(f"A010 requires {name} as an object")

async def run_a010_campaign(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "gtm_strategy": request["gtm_strategy"],
        "messaging_positioning": request["messaging_positioning"],
        "content_strategy": request.get("content_strategy") or {},
        "offer_pricing_strategy": request.get("offer_pricing_strategy") or {},
        "channel_strategy": request.get("channel_strategy") or {},
        "icp_definition": request.get("icp_definition") or {},
        "campaign_constraints": request.get("campaign_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A010",
        "Build concrete campaign plans from the supplied GTM and messaging strategy. Return ONLY A010 JSON.",
        "PR016",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A010CampaignStrategyError("A010 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass campaign strategy to execution, content and outreach agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A010CampaignStrategyError(f"A010 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A010CampaignStrategyError("A010 confidence must be high, medium, or low")
    for f in ["campaigns", "goals", "audiences", "sequences", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A010CampaignStrategyError(f"A010 {f} must be an array")
    for f in ["channel_plan", "budget_guidance"]:
        if not isinstance(output.get(f), dict):
            raise A010CampaignStrategyError(f"A010 {f} must be an object")
    return RunResult(llm.run_id, "A010", "campaign.strategy+ollama", "completed", result=output)
