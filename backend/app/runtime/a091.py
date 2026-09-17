from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A091CampaignQAError(RuntimeError): pass
REQUIRED = {"status","pass_fail","issues","suggested_fixes","score","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("campaign_package"), dict):
        raise A091CampaignQAError("A091 requires campaign_package as an object")

async def run_a091_campaign_qa(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"campaign_package": request["campaign_package"], "marketing_strategy": request.get("marketing_strategy") or {}, "qa_rules": request.get("qa_rules") or [], "review_constraints": request.get("review_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A091", "QA campaign package for brand and compliance. Return ONLY A091 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A091CampaignQAError("A091 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "If pass, approve launch; if fail, return to campaign owners.")
    missing = REQUIRED - set(output)
    if missing: raise A091CampaignQAError(f"A091 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A091CampaignQAError("A091 confidence must be high, medium, or low")
    for f in ["issues", "suggested_fixes", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A091CampaignQAError(f"A091 {f} must be an array")
    return RunResult(llm.run_id, "A091", "campaign.qa+ollama", "completed", result=output)
