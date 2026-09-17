from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A017ProposalStrategyError(RuntimeError): pass

REQUIRED = {
    "status", "structure", "value_framing", "pricing_presentation", "proof_sections",
    "approval_boundaries", "confidence", "assumptions", "derived_from",
    "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("offer_pricing_strategy", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A017ProposalStrategyError(f"A017 requires {name} as an object")

async def run_a017_proposal(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "offer_pricing_strategy": request["offer_pricing_strategy"],
        "messaging_positioning": request["messaging_positioning"],
        "sales_enablement_strategy": request.get("sales_enablement_strategy") or {},
        "pipeline_deal_strategy": request.get("pipeline_deal_strategy") or {},
        "competitor_intelligence": request.get("competitor_intelligence") or {},
        "proposal_constraints": request.get("proposal_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A017",
        "Design proposal structure, value framing and approval boundaries from the supplied offer and messaging context. Return ONLY A017 JSON.",
        "PR023",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A017ProposalStrategyError("A017 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass proposal strategy to proposal generation and approval agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A017ProposalStrategyError(f"A017 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A017ProposalStrategyError("A017 confidence must be high, medium, or low")
    for f in ["structure", "proof_sections", "approval_boundaries", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A017ProposalStrategyError(f"A017 {f} must be an array")
    for f in ["value_framing", "pricing_presentation"]:
        if not isinstance(output.get(f), dict):
            raise A017ProposalStrategyError(f"A017 {f} must be an object")
    return RunResult(llm.run_id, "A017", "proposal.strategy+ollama", "completed", result=output)
