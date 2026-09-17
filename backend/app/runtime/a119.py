from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A119Error(RuntimeError):
    pass


REQUIRED = {
    "compatibility_score", "fit_dimensions", "blockers", "adaptation_requirements", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("candidate_agent_spec"), dict):
        raise A119Error("A119 requires candidate_agent_spec as an object")
    if not isinstance(request.get("platform_baseline"), dict):
        raise A119Error("A119 requires platform_baseline as an object")


async def run_a119_agent_compatibility(request: dict[str, Any]) -> RunResult:
    """Agent Compatibility Analyst — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "candidate_agent_spec": request["candidate_agent_spec"],
        "platform_baseline": request["platform_baseline"],
        "skill_contract_map": request.get("skill_contract_map") or {},
        "tool_allowlist": request.get("tool_allowlist") or [],
        "schema_versions": request.get("schema_versions") or {},
        "prior_compatibility_report": request.get("prior_compatibility_report") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No runtime or registry mutation",
            "No secret exposure",
            "Blockers must be explicit when fit is incomplete",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A119",
        "Analyze compatibility of the candidate agent with the AIOS platform baseline. Score fit dimensions, list blockers and adaptation requirements. Return ONLY A119 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A119Error("A119 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Feed adaptation_requirements to Agent Package Builder (A116); pass blockers to Certification (A118).")
    missing = REQUIRED - set(output)
    if missing:
        raise A119Error(f"A119 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A119Error("A119 confidence must be high, medium, or low")
    for f in ["fit_dimensions", "blockers", "adaptation_requirements", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A119Error(f"A119 {f} must be an array")
    if not isinstance(output.get("compatibility_score"), dict):
        raise A119Error("A119 compatibility_score must be an object")
    return RunResult(llm.run_id, "A119", "a119.ollama", "completed", result=output)
