from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A077FeedbackNPSError(RuntimeError): pass
REQUIRED = {"status","themes","nps_summary","promoter_actions","detractor_actions","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("feedback_corpus"), dict):
        raise A077FeedbackNPSError("A077 requires feedback_corpus as an object")

async def run_a077_feedback_nps(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"feedback_corpus": request["feedback_corpus"], "nps_scores": request.get("nps_scores") or {}, "account_context": request.get("account_context") or {}, "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A077", "Analyze NPS and feedback themes; recommend promoter and detractor actions. Return ONLY A077 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A077FeedbackNPSError("A077 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Feed themes into product/CS roadmap and Knowledge Extractor (A070).")
    missing = REQUIRED - set(output)
    if missing: raise A077FeedbackNPSError(f"A077 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A077FeedbackNPSError("A077 confidence must be high, medium, or low")
    for f in ["themes", "promoter_actions", "detractor_actions", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A077FeedbackNPSError(f"A077 {f} must be an array")
    if not isinstance(output.get("nps_summary"), dict): raise A077FeedbackNPSError("A077 nps_summary must be an object")
    return RunResult(llm.run_id, "A077", "feedback.nps+ollama", "completed", result=output)
