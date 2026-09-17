from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A087SocialError(RuntimeError): pass
REQUIRED = {"status","channel_mix","content_types","engagement_plays","success_metrics","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("marketing_strategy"), dict):
        raise A087SocialError("A087 requires marketing_strategy as an object")

async def run_a087_social(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"marketing_strategy": request["marketing_strategy"], "content_strategy": request.get("content_strategy") or {}, "audience_insights": request.get("audience_insights") or {}, "social_constraints": request.get("social_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A087", "Plan social channel mix and engagement plays. Return ONLY A087 JSON.", "PR004", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A087SocialError("A087 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass to Paid Media Analyst (A088) or Marketing Analytics (A089).")
    missing = REQUIRED - set(output)
    if missing: raise A087SocialError(f"A087 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A087SocialError("A087 confidence must be high, medium, or low")
    for f in ["channel_mix", "content_types", "engagement_plays", "success_metrics", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A087SocialError(f"A087 {f} must be an array")
    return RunResult(llm.run_id, "A087", "social.strategist+ollama", "completed", result=output)
