from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A120Error(RuntimeError):
    pass


REQUIRED = {
    "listing_metadata", "quality_labels", "dependency_notes", "publish_readiness", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("certified_agent_package"), dict):
        raise A120Error("A120 requires certified_agent_package as an object")


async def run_a120_marketplace_curator(request: dict[str, Any]) -> RunResult:
    """Agent Marketplace Curator — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "certified_agent_package": request["certified_agent_package"],
        "marketplace_taxonomy": request.get("marketplace_taxonomy") or {},
        "quality_labels": request.get("quality_labels") or [],
        "dependency_notes": request.get("dependency_notes") or [],
        "prior_listing": request.get("prior_listing") or {},
        "publish_constraints": request.get("publish_constraints") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No publish or install side effects",
            "No secret exposure",
            "Publish readiness must be explicit",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A120",
        "Curate a marketplace listing for the certified agent package. Produce listing_metadata, quality_labels, dependency_notes and publish_readiness. Return ONLY A120 JSON. Do not publish or install.",
        "PR001",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A120Error("A120 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Human review of publish_readiness; if ready, queue for governed marketplace publish workflow (approval-gated).")
    missing = REQUIRED - set(output)
    if missing:
        raise A120Error(f"A120 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A120Error("A120 confidence must be high, medium, or low")
    for f in ["quality_labels", "dependency_notes", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A120Error(f"A120 {f} must be an array")
    for f in ["listing_metadata", "publish_readiness"]:
        if not isinstance(output.get(f), dict):
            raise A120Error(f"A120 {f} must be an object")
    return RunResult(llm.run_id, "A120", "a120.ollama", "completed", result=output)
