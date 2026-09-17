from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A043OutreachStrategyError(RuntimeError): pass
REQUIRED = {"status","channel_mix","sequence_outline","messaging_angles","success_metrics","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("account_research", "outreach_strategy"):
        if not isinstance(request.get(name), dict):
            raise A043OutreachStrategyError(f"A043 requires {name} as an object")

async def run_a043_outreach_plan(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"account_research": request["account_research"], "outreach_strategy": request["outreach_strategy"], "messaging_positioning": request.get("messaging_positioning") or {}, "scored_leads": request.get("scored_leads") or {}, "outreach_constraints": request.get("outreach_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A043", "Design operational outreach plan (channels, sequence, angles) from research and strategy. Return ONLY A043 JSON.", "PR004", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A043OutreachStrategyError("A043 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass outreach plan to Email Outreach (A044).")
    missing = REQUIRED - set(output)
    if missing: raise A043OutreachStrategyError(f"A043 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A043OutreachStrategyError("A043 confidence must be high, medium, or low")
    for f in ["sequence_outline", "messaging_angles", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A043OutreachStrategyError(f"A043 {f} must be an array")
    if not isinstance(output.get("channel_mix"), dict): raise A043OutreachStrategyError("A043 channel_mix must be an object")
    return RunResult(llm.run_id, "A043", "outreach.plan+ollama", "completed", result=output)
