from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A085ContentError(RuntimeError): pass
REQUIRED = {"status","pillars","formats","calendar_outline","success_metrics","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("marketing_strategy"), dict):
        raise A085ContentError("A085 requires marketing_strategy as an object")

async def run_a085_content(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"marketing_strategy": request["marketing_strategy"], "messaging_positioning": request.get("messaging_positioning") or {}, "audience_insights": request.get("audience_insights") or {}, "content_constraints": request.get("content_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A085", "Plan content pillars, formats and calendar. Return ONLY A085 JSON.", "PR004", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A085ContentError("A085 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass to SEO Strategist (A086) or Social Media Strategist (A087).")
    missing = REQUIRED - set(output)
    if missing: raise A085ContentError(f"A085 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A085ContentError("A085 confidence must be high, medium, or low")
    for f in ["pillars", "formats", "calendar_outline", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A085ContentError(f"A085 {f} must be an array")
    return RunResult(llm.run_id, "A085", "content.strategist+ollama", "completed", result=output)
