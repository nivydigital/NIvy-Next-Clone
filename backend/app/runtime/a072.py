from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A072OnboardingPlannerError(RuntimeError): pass
REQUIRED = {"status","tasks","timeline","owners","checkpoints","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("onboarding_plan"), dict):
        raise A072OnboardingPlannerError("A072 requires onboarding_plan as an object")

async def run_a072_onboarding_planner(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"onboarding_plan": request["onboarding_plan"], "account_research": request.get("account_research") or {}, "customer_profile": request.get("customer_profile") or {}, "planning_constraints": request.get("planning_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A072", "Expand onboarding plan into timed tasks and checkpoints. Return ONLY A072 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A072OnboardingPlannerError("A072 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass schedule to CS team and Customer Health Analyst (A073).")
    missing = REQUIRED - set(output)
    if missing: raise A072OnboardingPlannerError(f"A072 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A072OnboardingPlannerError("A072 confidence must be high, medium, or low")
    for f in ["tasks", "owners", "checkpoints", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A072OnboardingPlannerError(f"A072 {f} must be an array")
    if not isinstance(output.get("timeline"), dict): raise A072OnboardingPlannerError("A072 timeline must be an object")
    return RunResult(llm.run_id, "A072", "onboarding.planner+ollama", "completed", result=output)
