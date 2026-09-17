from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A007ContentStrategyError(RuntimeError): pass

REQUIRED = {
    "status", "content_pillars", "themes", "formats", "distribution_plan",
    "measurement", "content_calendar_outline", "confidence", "assumptions",
    "derived_from", "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A007ContentStrategyError(f"A007 requires {name} as an object")

async def run_a007_content(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "messaging_positioning": request["messaging_positioning"],
        "buyer_personas": request.get("buyer_personas") or {},
        "channel_strategy": request.get("channel_strategy") or {},
        "competitor_intelligence": request.get("competitor_intelligence") or {},
        "business_offer": request.get("business_offer") or {},
        "content_constraints": request.get("content_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A007",
        "Build an evidence-backed content strategy from the supplied ICP, messaging and channel context. Return ONLY A007 JSON.",
        "PR013",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A007ContentStrategyError("A007 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass content strategy to content production and campaign agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A007ContentStrategyError(f"A007 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A007ContentStrategyError("A007 confidence must be high, medium, or low")
    for f in ["content_pillars", "themes", "formats", "content_calendar_outline", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A007ContentStrategyError(f"A007 {f} must be an array")
    for f in ["distribution_plan", "measurement"]:
        if not isinstance(output.get(f), dict):
            raise A007ContentStrategyError(f"A007 {f} must be an object")
    return RunResult(llm.run_id, "A007", "content.strategy+ollama", "completed", result=output)
