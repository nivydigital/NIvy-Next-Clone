from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A021SupportStrategyError(RuntimeError): pass

REQUIRED = {"status","support_model","triage_rules","sla_guidance","escalation_paths","knowledge_requirements","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("onboarding_strategy", "customer_health_strategy"):
        if not isinstance(request.get(name), dict):
            raise A021SupportStrategyError(f"A021 requires {name} as an object")

async def run_a021_support(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"onboarding_strategy": request["onboarding_strategy"], "customer_health_strategy": request["customer_health_strategy"], "offer_pricing_strategy": request.get("offer_pricing_strategy") or {}, "support_constraints": request.get("support_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A021", "Define support model, triage rules and escalation paths from the supplied onboarding and health context. Return ONLY A021 JSON.", "PR027", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A021SupportStrategyError("A021 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass support strategy to support triage and knowledge agents.")
    missing = REQUIRED - set(output)
    if missing: raise A021SupportStrategyError(f"A021 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A021SupportStrategyError("A021 confidence must be high, medium, or low")
    for f in ["triage_rules", "escalation_paths", "knowledge_requirements", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A021SupportStrategyError(f"A021 {f} must be an array")
    for f in ["support_model", "sla_guidance"]:
        if not isinstance(output.get(f), dict): raise A021SupportStrategyError(f"A021 {f} must be an object")
    return RunResult(llm.run_id, "A021", "support.strategy+ollama", "completed", result=output)
