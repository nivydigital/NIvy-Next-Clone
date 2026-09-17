from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A082PricingError(RuntimeError): pass
REQUIRED = {"status","performance_summary","recommended_changes","experiments","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("offer_pricing_strategy"), dict):
        raise A082PricingError("A082 requires offer_pricing_strategy as an object")

async def run_a082_pricing(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"offer_pricing_strategy": request["offer_pricing_strategy"], "revenue_signals": request.get("revenue_signals") or {}, "competitor_pricing": request.get("competitor_pricing") or {}, "pricing_constraints": request.get("pricing_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A082", "Analyze pricing performance and recommend changes. Return ONLY A082 JSON.", "PR002", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A082PricingError("A082 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Feed into Revenue Analytics (A083) or offer strategy updates.")
    missing = REQUIRED - set(output)
    if missing: raise A082PricingError(f"A082 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A082PricingError("A082 confidence must be high, medium, or low")
    for f in ["recommended_changes", "experiments", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A082PricingError(f"A082 {f} must be an array")
    if not isinstance(output.get("performance_summary"), dict): raise A082PricingError("A082 performance_summary must be an object")
    return RunResult(llm.run_id, "A082", "pricing+ollama", "completed", result=output)
