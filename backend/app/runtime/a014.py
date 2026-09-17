from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A014OutreachStrategyError(RuntimeError): pass

REQUIRED = {
    "status", "sequences", "personalization_rules", "cadence", "channel_mix",
    "compliance_rules", "success_metrics", "confidence", "assumptions",
    "derived_from", "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("messaging_positioning", "campaign_strategy"):
        if not isinstance(request.get(name), dict):
            raise A014OutreachStrategyError(f"A014 requires {name} as an object")

async def run_a014_outreach(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "messaging_positioning": request["messaging_positioning"],
        "campaign_strategy": request["campaign_strategy"],
        "lead_generation_strategy": request.get("lead_generation_strategy") or {},
        "sales_enablement_strategy": request.get("sales_enablement_strategy") or {},
        "channel_strategy": request.get("channel_strategy") or {},
        "outreach_constraints": request.get("outreach_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A014",
        "Design a multi-channel outreach strategy with sequences, cadence and compliance from the supplied messaging and campaign context. Return ONLY A014 JSON.",
        "PR020",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A014OutreachStrategyError("A014 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass outreach strategy to email, personalization and follow-up agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A014OutreachStrategyError(f"A014 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A014OutreachStrategyError("A014 confidence must be high, medium, or low")
    for f in ["sequences", "personalization_rules", "compliance_rules", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A014OutreachStrategyError(f"A014 {f} must be an array")
    for f in ["cadence", "channel_mix"]:
        if not isinstance(output.get(f), dict):
            raise A014OutreachStrategyError(f"A014 {f} must be an object")
    return RunResult(llm.run_id, "A014", "outreach.strategy+ollama", "completed", result=output)
