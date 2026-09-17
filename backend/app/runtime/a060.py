from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A060ProposalError(RuntimeError): pass
REQUIRED = {"status","sections","value_summary","pricing_block","next_steps","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("proposal_strategy", "offer_pricing_strategy"):
        if not isinstance(request.get(name), dict):
            raise A060ProposalError(f"A060 requires {name} as an object")

async def run_a060_proposal(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"proposal_strategy": request["proposal_strategy"], "offer_pricing_strategy": request["offer_pricing_strategy"], "account_research": request.get("account_research") or {}, "qualification_result": request.get("qualification_result") or {}, "meeting_brief": request.get("meeting_brief") or {}, "proposal_constraints": request.get("proposal_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A060", "Draft proposal sections, value summary and pricing block. Do not send. Return ONLY A060 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A060ProposalError("A060 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route proposal draft to approval or Onboarding Agent (A065).")
    missing = REQUIRED - set(output)
    if missing: raise A060ProposalError(f"A060 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A060ProposalError("A060 confidence must be high, medium, or low")
    for f in ["sections", "next_steps", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A060ProposalError(f"A060 {f} must be an array")
    if not isinstance(output.get("pricing_block"), dict): raise A060ProposalError("A060 pricing_block must be an object")
    return RunResult(llm.run_id, "A060", "proposal+ollama", "completed", result=output)
