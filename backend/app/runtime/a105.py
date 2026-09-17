from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A105Error(RuntimeError):
    pass


REQUIRED = {
    "proposed_prompt", "change_summary", "rationale", "risks", "validation_plan", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("current_prompt"), dict):
        raise A105Error("A105 requires current_prompt as an object")
    if not isinstance(request.get("improvement_signals"), dict):
        raise A105Error("A105 requires improvement_signals as an object")


async def run_a105_prompt_improvement(request: dict[str, Any]) -> RunResult:
    """Prompt Improvement Agent — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "current_prompt": request["current_prompt"],
        "improvement_signals": request["improvement_signals"],
        "evaluation_evidence": request.get("evaluation_evidence") or {},
        "style_constraints": request.get("style_constraints") or {},
        "prior_prompt_versions": request.get("prior_prompt_versions") or {},
        "risk_appetite": request.get("risk_appetite") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production prompt promotion",
            "No secret exposure",
            "Proposed changes must be explicit diffs",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A105",
        "Propose prompt improvements from current_prompt and improvement_signals. Produce proposed_prompt, change_summary, rationale, risks and validation_plan. Return ONLY A105 JSON. Do not promote.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A105Error("A105 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Validate via Experiment Manager (A107); submit to Improvement Promotion Reviewer (A109).")
    missing = REQUIRED - set(output)
    if missing:
        raise A105Error(f"A105 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A105Error("A105 confidence must be high, medium, or low")
    for f in ["change_summary", "risks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A105Error(f"A105 {f} must be an array")
    for f in ["proposed_prompt", "rationale", "validation_plan"]:
        if not isinstance(output.get(f), dict):
            raise A105Error(f"A105 {f} must be an object")
    return RunResult(llm.run_id, "A105", "a105.ollama", "completed", result=output)
