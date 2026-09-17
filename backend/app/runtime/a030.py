from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A030ProductMarketingError(RuntimeError): pass
REQUIRED = {"status","product_narrative","launch_messaging","differentiation","enablement_needs","proof_points","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("offer_pricing_strategy", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A030ProductMarketingError(f"A030 requires {name} as an object")

async def run_a030_product_marketing(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"offer_pricing_strategy": request["offer_pricing_strategy"], "messaging_positioning": request["messaging_positioning"], "competitor_intelligence": request.get("competitor_intelligence") or {}, "brand_strategy": request.get("brand_strategy") or {}, "product_constraints": request.get("product_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A030", "Define product narrative, launch messaging and differentiation from the supplied offer and messaging context. Return ONLY A030 JSON.", "PR036", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A030ProductMarketingError("A030 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass product marketing strategy to launch, sales enablement and content agents.")
    missing = REQUIRED - set(output)
    if missing: raise A030ProductMarketingError(f"A030 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A030ProductMarketingError("A030 confidence must be high, medium, or low")
    if not isinstance(output.get("product_narrative"), str) or not output["product_narrative"].strip(): raise A030ProductMarketingError("A030 product_narrative must be a non-empty string")
    for f in ["differentiation", "enablement_needs", "proof_points", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A030ProductMarketingError(f"A030 {f} must be an array")
    if not isinstance(output.get("launch_messaging"), dict): raise A030ProductMarketingError("A030 launch_messaging must be an object")
    return RunResult(llm.run_id, "A030", "product.marketing+ollama", "completed", result=output)
