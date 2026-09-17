from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A029BrandStrategyError(RuntimeError): pass
REQUIRED = {"status","brand_positioning","personality","narrative_pillars","visual_verbal_guardrails","proof_themes","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("messaging_positioning", "icp_definition"):
        if not isinstance(request.get(name), dict):
            raise A029BrandStrategyError(f"A029 requires {name} as an object")

async def run_a029_brand(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"messaging_positioning": request["messaging_positioning"], "icp_definition": request["icp_definition"], "competitor_intelligence": request.get("competitor_intelligence") or {}, "content_strategy": request.get("content_strategy") or {}, "brand_constraints": request.get("brand_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A029", "Define brand positioning, personality and narrative pillars from the supplied messaging and ICP context. Return ONLY A029 JSON.", "PR035", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A029BrandStrategyError("A029 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass brand strategy to content, design and marketing agents.")
    missing = REQUIRED - set(output)
    if missing: raise A029BrandStrategyError(f"A029 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A029BrandStrategyError("A029 confidence must be high, medium, or low")
    if not isinstance(output.get("brand_positioning"), str) or not output["brand_positioning"].strip(): raise A029BrandStrategyError("A029 brand_positioning must be a non-empty string")
    for f in ["narrative_pillars", "visual_verbal_guardrails", "proof_themes", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A029BrandStrategyError(f"A029 {f} must be an array")
    if not isinstance(output.get("personality"), dict): raise A029BrandStrategyError("A029 personality must be an object")
    return RunResult(llm.run_id, "A029", "brand.strategy+ollama", "completed", result=output)
