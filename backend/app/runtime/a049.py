from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A049PersonalizationError(RuntimeError): pass
REQUIRED = {"status","hooks","context_snippets","do_not_use","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("account_research", "messaging_positioning"):
        if not isinstance(request.get(name), dict):
            raise A049PersonalizationError(f"A049 requires {name} as an object")

async def run_a049_personalization(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"account_research": request["account_research"], "messaging_positioning": request["messaging_positioning"], "scored_leads": request.get("scored_leads") or {}, "personalization_constraints": request.get("personalization_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A049", "Generate personalization hooks and context from research and messaging. Return ONLY A049 JSON.", "PR004", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A049PersonalizationError("A049 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass personalization pack to Email Outreach (A044).")
    missing = REQUIRED - set(output)
    if missing: raise A049PersonalizationError(f"A049 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A049PersonalizationError("A049 confidence must be high, medium, or low")
    for f in ["hooks", "context_snippets", "do_not_use", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A049PersonalizationError(f"A049 {f} must be an array")
    return RunResult(llm.run_id, "A049", "personalization+ollama", "completed", result=output)
