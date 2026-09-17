from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A026PricingGovernanceError(RuntimeError): pass
REQUIRED = {"status","approval_paths","discount_guardrails","exception_handling","review_cadence","escalation_rules","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("offer_pricing_strategy", "revenue_operations_strategy"):
        if not isinstance(request.get(name), dict):
            raise A026PricingGovernanceError(f"A026 requires {name} as an object")

async def run_a026_pricing_gov(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"offer_pricing_strategy": request["offer_pricing_strategy"], "revenue_operations_strategy": request["revenue_operations_strategy"], "pipeline_deal_strategy": request.get("pipeline_deal_strategy") or {}, "pricing_constraints": request.get("pricing_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A026", "Define pricing approval paths, discount guardrails and exception handling from the supplied offer and RevOps context. Return ONLY A026 JSON.", "PR032", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A026PricingGovernanceError("A026 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass pricing governance to deal desk and finance agents.")
    missing = REQUIRED - set(output)
    if missing: raise A026PricingGovernanceError(f"A026 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A026PricingGovernanceError("A026 confidence must be high, medium, or low")
    for f in ["approval_paths", "discount_guardrails", "escalation_rules", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A026PricingGovernanceError(f"A026 {f} must be an array")
    for f in ["exception_handling", "review_cadence"]:
        if not isinstance(output.get(f), dict): raise A026PricingGovernanceError(f"A026 {f} must be an object")
    return RunResult(llm.run_id, "A026", "pricing.governance+ollama", "completed", result=output)
