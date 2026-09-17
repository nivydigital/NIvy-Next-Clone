from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .engine import RunResult, runtime_engine


class A002ICPError(RuntimeError):
    pass


REQUIRED_FIELDS = {
    "status",
    "icp_definition",
    "evidence",
    "warnings",
    "errors",
    "next_action",
}


def _has_provenance(item: dict[str, Any]) -> bool:
    if item.get("url") or item.get("source_url") or item.get("provenance"):
        return True
    return False


def _collect_evidence(market_research: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = market_research.get("evidence") or market_research.get("sources") or []
    if not isinstance(candidates, list):
        return []
    return [x for x in candidates if isinstance(x, dict)]


def _validate_market_research(market_research: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = _collect_evidence(market_research)
    if not evidence:
        raise A002ICPError("A002 requires approved market research evidence with provenance")
    invalid = [i for i, item in enumerate(evidence) if not _has_provenance(item)]
    if invalid:
        raise A002ICPError(f"A002 evidence items missing provenance at indexes: {invalid}")
    return evidence


def _validate_output(output: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS - set(output)
    if missing:
        raise A002ICPError(f"A002 output missing required fields: {sorted(missing)}")
    if output.get("status") not in {"success", "partial", "failed", "escalated"}:
        raise A002ICPError("A002 output has invalid status")
    definition = output.get("icp_definition")
    if not isinstance(definition, dict):
        raise A002ICPError("A002 icp_definition must be an object")
    required_definition = {
        "target_segments", "firmographics", "buyer_roles", "pain_points",
        "buying_signals", "exclusions", "confidence", "assumptions",
        "derived_from", "discovery_rules",
    }
    missing_definition = required_definition - set(definition)
    if missing_definition:
        raise A002ICPError(f"A002 icp_definition missing fields: {sorted(missing_definition)}")
    if definition.get("confidence") not in {"high", "medium", "low"}:
        raise A002ICPError("A002 confidence must be high, medium, or low")
    for field in ["target_segments", "buyer_roles", "pain_points", "buying_signals", "exclusions", "assumptions", "derived_from", "discovery_rules"]:
        if not isinstance(definition.get(field), list):
            raise A002ICPError(f"A002 {field} must be an array")
    if not isinstance(definition.get("firmographics"), dict):
        raise A002ICPError("A002 firmographics must be an object")


async def run_a002_icp(request: dict[str, Any]) -> RunResult:
    market_research = request.get("market_research")
    if not isinstance(market_research, dict):
        raise A002ICPError("A002 requires market_research as an object")

    evidence = _validate_market_research(market_research)
    context = {
        "market_research": market_research,
        "business_offer": request.get("business_offer") or {},
        "existing_customers": request.get("existing_customers") or [],
        "exclusions": request.get("exclusions") or [],
        "geography": request.get("geography"),
        "revenue_targets": request.get("revenue_targets") or {},
        "approved_evidence": evidence,
        "current_time": datetime.now(timezone.utc).isoformat(),
        "output_schema": {
            "required": sorted(REQUIRED_FIELDS),
            "icp_definition_required": [
                "target_segments", "firmographics", "buyer_roles", "pain_points",
                "buying_signals", "exclusions", "confidence", "assumptions",
                "derived_from", "discovery_rules",
            ],
            "confidence_values": ["high", "medium", "low"],
        },
    }

    llm = await runtime_engine.run_llm(
        "A002",
        "Build an operational ICP only from the supplied approved market evidence and business context. Return ONLY the A002 output JSON object.",
        "PR002",
        context,
    )
    if llm.status != "completed":
        return llm

    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A002ICPError("A002 model did not return valid JSON") from exc

    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("actions", [])
    output.setdefault("records_changed", [])
    output.setdefault("next_action", "Pass validated ICP to the downstream discovery/scoring agent.")
    _validate_output(output)
    return RunResult(llm.run_id, "A002", "icp.strategy+ollama", "completed", result=output)
