from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A031DemandGenError(RuntimeError): pass
REQUIRED = {"status","programs","funnel_stages","content_campaign_map","measurement","volume_goals","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("campaign_strategy", "content_strategy"):
        if not isinstance(request.get(name), dict):
            raise A031DemandGenError(f"A031 requires {name} as an object")

async def run_a031_demand(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"campaign_strategy": request["campaign_strategy"], "content_strategy": request["content_strategy"], "lead_generation_strategy": request.get("lead_generation_strategy") or {}, "channel_strategy": request.get("channel_strategy") or {}, "demand_constraints": request.get("demand_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A031", "Define demand generation programs, funnel stages and measurement from the supplied campaign and content context. Return ONLY A031 JSON.", "PR037", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A031DemandGenError("A031 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass demand gen strategy to campaign execution and content production agents.")
    missing = REQUIRED - set(output)
    if missing: raise A031DemandGenError(f"A031 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A031DemandGenError("A031 confidence must be high, medium, or low")
    for f in ["programs", "funnel_stages", "content_campaign_map", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A031DemandGenError(f"A031 {f} must be an array")
    for f in ["measurement", "volume_goals"]:
        if not isinstance(output.get(f), dict): raise A031DemandGenError(f"A031 {f} must be an object")
    return RunResult(llm.run_id, "A031", "demand.generation+ollama", "completed", result=output)
