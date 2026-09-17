from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A032CompetitiveResponseError(RuntimeError): pass
REQUIRED = {"status","monitoring_triggers","response_playbooks","messaging_counters","escalation_rules","review_cadence","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("competitor_intelligence", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A032CompetitiveResponseError(f"A032 requires {name} as an object")

async def run_a032_competitive_response(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"competitor_intelligence": request["competitor_intelligence"], "messaging_positioning": request["messaging_positioning"], "brand_strategy": request.get("brand_strategy") or {}, "product_marketing_strategy": request.get("product_marketing_strategy") or {}, "response_constraints": request.get("response_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A032", "Define competitive monitoring triggers, response playbooks and messaging counters from the supplied competitor and messaging context. Return ONLY A032 JSON.", "PR038", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A032CompetitiveResponseError("A032 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass competitive response strategy to marketing and sales enablement agents.")
    missing = REQUIRED - set(output)
    if missing: raise A032CompetitiveResponseError(f"A032 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A032CompetitiveResponseError("A032 confidence must be high, medium, or low")
    for f in ["monitoring_triggers", "response_playbooks", "messaging_counters", "escalation_rules", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A032CompetitiveResponseError(f"A032 {f} must be an array")
    if not isinstance(output.get("review_cadence"), dict): raise A032CompetitiveResponseError("A032 review_cadence must be an object")
    return RunResult(llm.run_id, "A032", "competitive.response+ollama", "completed", result=output)
