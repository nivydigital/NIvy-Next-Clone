from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A106Error(RuntimeError):
    pass


REQUIRED = {
    "proposed_skill_changes", "gap_analysis", "rationale", "risks", "validation_plan", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("skill_spec"), dict):
        raise A106Error("A106 requires skill_spec as an object")
    if not isinstance(request.get("improvement_signals"), dict):
        raise A106Error("A106 requires improvement_signals as an object")


async def run_a106_skill_improvement(request: dict[str, Any]) -> RunResult:
    """Skill Improvement Agent — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "skill_spec": request["skill_spec"],
        "improvement_signals": request["improvement_signals"],
        "evaluation_evidence": request.get("evaluation_evidence") or {},
        "dependency_map": request.get("dependency_map") or {},
        "prior_skill_versions": request.get("prior_skill_versions") or {},
        "policy_constraints": request.get("policy_constraints") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No skill deployment",
            "No secret exposure",
            "Changes must be explicit and testable",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A106",
        "Propose skill improvements from skill_spec and improvement_signals. Produce proposed_skill_changes, gap_analysis, rationale, risks and validation_plan. Return ONLY A106 JSON. Do not deploy.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A106Error("A106 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Validate via Experiment Manager (A107); submit to Improvement Promotion Reviewer (A109).")
    missing = REQUIRED - set(output)
    if missing:
        raise A106Error(f"A106 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A106Error("A106 confidence must be high, medium, or low")
    for f in ["proposed_skill_changes", "gap_analysis", "risks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A106Error(f"A106 {f} must be an array")
    for f in ["rationale", "validation_plan"]:
        if not isinstance(output.get(f), dict):
            raise A106Error(f"A106 {f} must be an object")
    return RunResult(llm.run_id, "A106", "a106.ollama", "completed", result=output)
