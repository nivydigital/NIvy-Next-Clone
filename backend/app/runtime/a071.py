from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A071QualityReviewError(RuntimeError): pass
REQUIRED = {"status","pass_fail","issues","suggested_edits","score","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("response_draft"), dict):
        raise A071QualityReviewError("A071 requires response_draft as an object")

async def run_a071_quality_review(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"response_draft": request["response_draft"], "messaging_positioning": request.get("messaging_positioning") or {}, "quality_rules": request.get("quality_rules") or [], "review_constraints": request.get("review_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A071", "Review communication draft for quality and compliance. Return ONLY A071 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A071QualityReviewError("A071 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "If pass, approve send; if fail, return to Response Drafting (A068).")
    missing = REQUIRED - set(output)
    if missing: raise A071QualityReviewError(f"A071 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A071QualityReviewError("A071 confidence must be high, medium, or low")
    for f in ["issues", "suggested_edits", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A071QualityReviewError(f"A071 {f} must be an array")
    return RunResult(llm.run_id, "A071", "quality.review+ollama", "completed", result=output)
