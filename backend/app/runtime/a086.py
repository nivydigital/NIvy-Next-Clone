from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A086SEOError(RuntimeError): pass
REQUIRED = {"status","keyword_themes","content_opportunities","technical_priorities","success_metrics","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("marketing_strategy"), dict):
        raise A086SEOError("A086 requires marketing_strategy as an object")

async def run_a086_seo(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"marketing_strategy": request["marketing_strategy"], "content_strategy": request.get("content_strategy") or {}, "keyword_seeds": request.get("keyword_seeds") or [], "seo_constraints": request.get("seo_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A086", "Define SEO keyword themes and content opportunities. Return ONLY A086 JSON.", "PR001", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A086SEOError("A086 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass to Content execution or Marketing Analytics (A089).")
    missing = REQUIRED - set(output)
    if missing: raise A086SEOError(f"A086 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A086SEOError("A086 confidence must be high, medium, or low")
    for f in ["keyword_themes", "content_opportunities", "technical_priorities", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A086SEOError(f"A086 {f} must be an array")
    return RunResult(llm.run_id, "A086", "seo.strategist+ollama", "completed", result=output)
