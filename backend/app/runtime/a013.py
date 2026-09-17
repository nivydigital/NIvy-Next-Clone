from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A013LeadGenStrategyError(RuntimeError): pass

REQUIRED = {
    "status", "sources", "targeting_rules", "volume_goals", "qualification_handoff",
    "prioritization", "confidence", "assumptions", "derived_from",
    "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "gtm_strategy"):
        if not isinstance(request.get(name), dict):
            raise A013LeadGenStrategyError(f"A013 requires {name} as an object")

async def run_a013_lead_gen(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "gtm_strategy": request["gtm_strategy"],
        "campaign_strategy": request.get("campaign_strategy") or {},
        "channel_strategy": request.get("channel_strategy") or {},
        "buyer_personas": request.get("buyer_personas") or {},
        "historical_performance": request.get("historical_performance") or {},
        "lead_constraints": request.get("lead_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A013",
        "Design an evidence-backed lead generation strategy from the supplied ICP and GTM context. Return ONLY A013 JSON.",
        "PR019",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A013LeadGenStrategyError("A013 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass lead generation strategy to discovery and enrichment agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A013LeadGenStrategyError(f"A013 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A013LeadGenStrategyError("A013 confidence must be high, medium, or low")
    for f in ["sources", "targeting_rules", "prioritization", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A013LeadGenStrategyError(f"A013 {f} must be an array")
    for f in ["volume_goals", "qualification_handoff"]:
        if not isinstance(output.get(f), dict):
            raise A013LeadGenStrategyError(f"A013 {f} must be an object")
    return RunResult(llm.run_id, "A013", "leadgen.strategy+ollama", "completed", result=output)
