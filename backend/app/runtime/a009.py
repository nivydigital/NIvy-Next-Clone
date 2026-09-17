from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A009GTMStrategyError(RuntimeError): pass

REQUIRED = {
    "status", "target_segments", "channel_mix", "messaging_summary", "offer_summary",
    "launch_sequence", "success_metrics", "risks", "confidence", "assumptions",
    "derived_from", "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "channel_strategy", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A009GTMStrategyError(f"A009 requires {name} as an object")

async def run_a009_gtm(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "channel_strategy": request["channel_strategy"],
        "messaging_positioning": request["messaging_positioning"],
        "buyer_personas": request.get("buyer_personas") or {},
        "content_strategy": request.get("content_strategy") or {},
        "offer_pricing_strategy": request.get("offer_pricing_strategy") or {},
        "competitor_intelligence": request.get("competitor_intelligence") or {},
        "business_offer": request.get("business_offer") or {},
        "launch_constraints": request.get("launch_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A009",
        "Synthesize a coherent go-to-market strategy from the supplied strategy artifacts. Return ONLY A009 JSON.",
        "PR015",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A009GTMStrategyError("A009 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass GTM strategy to campaign execution, sales and operations agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A009GTMStrategyError(f"A009 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A009GTMStrategyError("A009 confidence must be high, medium, or low")
    for f in ["target_segments", "launch_sequence", "success_metrics", "risks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A009GTMStrategyError(f"A009 {f} must be an array")
    for f in ["channel_mix", "messaging_summary", "offer_summary"]:
        if not isinstance(output.get(f), dict):
            raise A009GTMStrategyError(f"A009 {f} must be an object")
    return RunResult(llm.run_id, "A009", "gtm.strategy+ollama", "completed", result=output)
