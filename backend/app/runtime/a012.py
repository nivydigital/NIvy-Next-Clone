from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A012ExperimentGrowthError(RuntimeError): pass

REQUIRED = {
    "status", "experiments", "hypotheses", "metrics", "prioritization",
    "decision_rules", "learning_agenda", "confidence", "assumptions",
    "derived_from", "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("gtm_strategy", "campaign_strategy"):
        if not isinstance(request.get(name), dict):
            raise A012ExperimentGrowthError(f"A012 requires {name} as an object")

async def run_a012_experiment(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "gtm_strategy": request["gtm_strategy"],
        "campaign_strategy": request["campaign_strategy"],
        "channel_strategy": request.get("channel_strategy") or {},
        "content_strategy": request.get("content_strategy") or {},
        "offer_pricing_strategy": request.get("offer_pricing_strategy") or {},
        "historical_performance": request.get("historical_performance") or {},
        "experiment_constraints": request.get("experiment_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A012",
        "Design prioritized growth experiments and a learning agenda from the supplied GTM and campaign strategy. Return ONLY A012 JSON.",
        "PR018",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A012ExperimentGrowthError("A012 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass experiment plan to growth execution and analytics agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A012ExperimentGrowthError(f"A012 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A012ExperimentGrowthError("A012 confidence must be high, medium, or low")
    for f in ["experiments", "hypotheses", "metrics", "prioritization", "decision_rules", "learning_agenda", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A012ExperimentGrowthError(f"A012 {f} must be an array")
    return RunResult(llm.run_id, "A012", "experiment.growth+ollama", "completed", result=output)
