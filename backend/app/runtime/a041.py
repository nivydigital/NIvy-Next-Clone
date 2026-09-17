from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A041AccountResearchError(RuntimeError): pass
REQUIRED = {"status","accounts","signals","talking_points","sources","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("scored_leads"), dict):
        raise A041AccountResearchError("A041 requires scored_leads as an object")

async def run_a041_account_research(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"scored_leads": request["scored_leads"], "icp_definition": request.get("icp_definition") or {}, "competitor_intelligence": request.get("competitor_intelligence") or {}, "research_constraints": request.get("research_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A041", "Research target accounts for signals and talking points. Return ONLY A041 JSON.", "PR003", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A041AccountResearchError("A041 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass account research to Outreach Strategy (A043) and Personalization (A049).")
    missing = REQUIRED - set(output)
    if missing: raise A041AccountResearchError(f"A041 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A041AccountResearchError("A041 confidence must be high, medium, or low")
    for f in ["accounts", "signals", "talking_points", "sources", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A041AccountResearchError(f"A041 {f} must be an array")
    return RunResult(llm.run_id, "A041", "account.research+ollama", "completed", result=output)
