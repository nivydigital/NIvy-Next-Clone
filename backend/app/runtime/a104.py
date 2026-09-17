from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A104Error(RuntimeError):
    pass


REQUIRED = {
    "theme_summary", "severity_distribution", "actionable_signals", "risks", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("feedback_corpus"), dict):
        raise A104Error("A104 requires feedback_corpus as an object")
    if not isinstance(request.get("analysis_scope"), dict):
        raise A104Error("A104 requires analysis_scope as an object")


async def run_a104_feedback_analyst(request: dict[str, Any]) -> RunResult:
    """Feedback Analyst — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "feedback_corpus": request["feedback_corpus"],
        "analysis_scope": request["analysis_scope"],
        "agent_filter": request.get("agent_filter") or {},
        "prior_themes": request.get("prior_themes") or {},
        "severity_rubric": request.get("severity_rubric") or {},
        "product_context": request.get("product_context") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production config mutation",
            "No secret exposure",
            "Signals must be evidence-backed",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A104",
        "Analyze the feedback_corpus for the given analysis_scope. Produce theme_summary, severity_distribution, actionable_signals, risks and recommendations. Return ONLY A104 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A104Error("A104 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Route high-severity signals to Prompt/Skill Improvement (A105/A106); feed themes to Experiment Manager (A107).")
    missing = REQUIRED - set(output)
    if missing:
        raise A104Error(f"A104 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A104Error("A104 confidence must be high, medium, or low")
    for f in ["actionable_signals", "risks", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A104Error(f"A104 {f} must be an array")
    for f in ["theme_summary", "severity_distribution"]:
        if not isinstance(output.get(f), dict):
            raise A104Error(f"A104 {f} must be an object")
    return RunResult(llm.run_id, "A104", "a104.ollama", "completed", result=output)
