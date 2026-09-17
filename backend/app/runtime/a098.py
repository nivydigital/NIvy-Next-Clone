from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A098Error(RuntimeError):
    pass


REQUIRED = {
    "score_summary", "dimension_scores", "failures", "gaps", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("evaluation_suite"), dict):
        raise A098Error("A098 requires evaluation_suite as an object")
    if not isinstance(request.get("run_results"), dict):
        raise A098Error("A098 requires run_results as an object")


async def run_a098_evaluation_analyst(request: dict[str, Any]) -> RunResult:
    """Evaluation Analyst — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "evaluation_suite": request["evaluation_suite"],
        "run_results": request["run_results"],
        "baselines": request.get("baselines") or {},
        "policy_rubric": request.get("policy_rubric") or {},
        "prior_evaluation": request.get("prior_evaluation") or {},
        "thresholds": request.get("thresholds") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production config mutation",
            "No secret exposure",
            "Scores must cite suite criteria",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A098",
        "Evaluate run_results against the evaluation_suite. Produce score_summary, dimension_scores, failures, gaps and recommendations. Return ONLY A098 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A098Error("A098 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Feed failures to Regression QA (A099) and Evidence Collector (A103); escalate systemic gaps.")
    missing = REQUIRED - set(output)
    if missing:
        raise A098Error(f"A098 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A098Error("A098 confidence must be high, medium, or low")
    for f in ["dimension_scores", "failures", "gaps", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A098Error(f"A098 {f} must be an array")
    if not isinstance(output.get("score_summary"), dict):
        raise A098Error("A098 score_summary must be an object")
    return RunResult(llm.run_id, "A098", "a098.ollama", "completed", result=output)
