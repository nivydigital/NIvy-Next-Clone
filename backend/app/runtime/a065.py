from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A065OnboardingError(RuntimeError): pass
REQUIRED = {"status","steps","milestones","owners","success_criteria","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("onboarding_strategy", "qualification_result"):
        if not isinstance(request.get(name), dict):
            raise A065OnboardingError(f"A065 requires {name} as an object")

async def run_a065_onboarding(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"onboarding_strategy": request["onboarding_strategy"], "qualification_result": request["qualification_result"], "proposal_draft": request.get("proposal_draft") or {}, "account_research": request.get("account_research") or {}, "onboarding_constraints": request.get("onboarding_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A065", "Plan customer onboarding steps and milestones. Return ONLY A065 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A065OnboardingError("A065 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass onboarding plan to Customer Onboarding Planner (A072) or CS team.")
    missing = REQUIRED - set(output)
    if missing: raise A065OnboardingError(f"A065 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A065OnboardingError("A065 confidence must be high, medium, or low")
    for f in ["steps", "milestones", "owners", "success_criteria", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A065OnboardingError(f"A065 {f} must be an array")
    return RunResult(llm.run_id, "A065", "onboarding+ollama", "completed", result=output)
