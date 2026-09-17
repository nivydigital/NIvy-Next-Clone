from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A107Error(RuntimeError):
    pass


REQUIRED = {
    "experiment_design", "metrics", "stop_rules", "risks", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("experiment_goal"), dict):
        raise A107Error("A107 requires experiment_goal as an object")
    if not isinstance(request.get("candidate_change"), dict):
        raise A107Error("A107 requires candidate_change as an object")


async def run_a107_experiment_manager(request: dict[str, Any]) -> RunResult:
    """Experiment Manager — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "experiment_goal": request["experiment_goal"],
        "candidate_change": request["candidate_change"],
        "baseline_config": request.get("baseline_config") or {},
        "success_metrics": request.get("success_metrics") or {},
        "risk_constraints": request.get("risk_constraints") or {},
        "prior_experiments": request.get("prior_experiments") or {},
        "sample_plan": request.get("sample_plan") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No live production config mutation",
            "No secret exposure",
            "Stop rules must be measurable",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A107",
        "Design a controlled experiment for the given goal and candidate change. Produce experiment_design, metrics, stop_rules, risks and recommendations. Return ONLY A107 JSON. Do not apply live changes.",
        "PR001",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A107Error("A107 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Run experiment in sandbox; feed outcomes to Improvement Promotion Reviewer (A109).")
    missing = REQUIRED - set(output)
    if missing:
        raise A107Error(f"A107 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A107Error("A107 confidence must be high, medium, or low")
    for f in ["metrics", "stop_rules", "risks", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A107Error(f"A107 {f} must be an array")
    if not isinstance(output.get("experiment_design"), dict):
        raise A107Error("A107 experiment_design must be an object")
    return RunResult(llm.run_id, "A107", "a107.ollama", "completed", result=output)
