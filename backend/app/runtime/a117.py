from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A117Error(RuntimeError):
    pass


REQUIRED = {
    "candidates", "ranked_matches", "gaps", "provenance_summary", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("discovery_scope"), dict):
        raise A117Error("A117 requires discovery_scope as an object")


async def run_a117_agent_discovery(request: dict[str, Any]) -> RunResult:
    """Agent Discovery Agent — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "discovery_scope": request["discovery_scope"],
        "source_preferences": request.get("source_preferences") or [],
        "capability_filters": request.get("capability_filters") or {},
        "existing_inventory": request.get("existing_inventory") or {},
        "license_constraints": request.get("license_constraints") or [],
        "prior_discovery": request.get("prior_discovery") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No agent registration or activation",
            "No secret exposure",
            "Every candidate must carry provenance or explicit assumption",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A117",
        (
            "Discover candidate agents and capabilities for the given discovery_scope. Rank matches, list gaps and summarize provenance. Return ONLY A117 JSON. Do not invent sources not supported by context."
        ),
        "PR001",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A117Error("A117 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass ranked candidates to Agent Compatibility Analyst (A119) and Agent Certification Agent (A118).")
    missing = REQUIRED - set(output)
    if missing:
        raise A117Error(f"A117 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A117Error("A117 confidence must be high, medium, or low")
    for f in ["candidates", "ranked_matches", "gaps", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A117Error(f"A117 {f} must be an array")
    if not isinstance(output.get("provenance_summary"), dict):
        raise A117Error("A117 provenance_summary must be an object")
    return RunResult(llm.run_id, "A117", "a117.ollama", "completed", result=output)
