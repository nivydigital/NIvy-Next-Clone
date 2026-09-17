from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A019RetentionExpansionError(RuntimeError): pass

REQUIRED = {"status","retention_plays","expansion_triggers","risk_signals","success_metrics","playbook_outline","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("onboarding_strategy", "offer_pricing_strategy"):
        if not isinstance(request.get(name), dict):
            raise A019RetentionExpansionError(f"A019 requires {name} as an object")

async def run_a019_retention(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"onboarding_strategy": request["onboarding_strategy"], "offer_pricing_strategy": request["offer_pricing_strategy"], "icp_definition": request.get("icp_definition") or {}, "gtm_strategy": request.get("gtm_strategy") or {}, "historical_retention": request.get("historical_retention") or {}, "retention_constraints": request.get("retention_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A019", "Define retention plays, expansion triggers and risk signals from the supplied onboarding and offer context. Return ONLY A019 JSON.", "PR025", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A019RetentionExpansionError("A019 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass retention strategy to customer success and expansion agents.")
    missing = REQUIRED - set(output)
    if missing: raise A019RetentionExpansionError(f"A019 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A019RetentionExpansionError("A019 confidence must be high, medium, or low")
    for f in ["retention_plays", "expansion_triggers", "risk_signals", "success_metrics", "playbook_outline", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A019RetentionExpansionError(f"A019 {f} must be an array")
    return RunResult(llm.run_id, "A019", "retention.expansion+ollama", "completed", result=output)
