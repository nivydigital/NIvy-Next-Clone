from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A018OnboardingStrategyError(RuntimeError): pass

REQUIRED = {
    "status", "journey_stages", "milestones", "success_criteria", "handoff_rules",
    "risk_signals", "confidence", "assumptions", "derived_from",
    "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("offer_pricing_strategy", "gtm_strategy"):
        if not isinstance(request.get(name), dict):
            raise A018OnboardingStrategyError(f"A018 requires {name} as an object")

async def run_a018_onboarding(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "offer_pricing_strategy": request["offer_pricing_strategy"],
        "gtm_strategy": request["gtm_strategy"],
        "sales_enablement_strategy": request.get("sales_enablement_strategy") or {},
        "messaging_positioning": request.get("messaging_positioning") or {},
        "icp_definition": request.get("icp_definition") or {},
        "onboarding_constraints": request.get("onboarding_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A018",
        "Define customer onboarding journey, milestones and success criteria from the supplied offer and GTM context. Return ONLY A018 JSON.",
        "PR024",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A018OnboardingStrategyError("A018 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass onboarding strategy to onboarding execution and customer success agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A018OnboardingStrategyError(f"A018 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A018OnboardingStrategyError("A018 confidence must be high, medium, or low")
    for f in ["journey_stages", "milestones", "success_criteria", "handoff_rules", "risk_signals", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A018OnboardingStrategyError(f"A018 {f} must be an array")
    return RunResult(llm.run_id, "A018", "onboarding.strategy+ollama", "completed", result=output)
