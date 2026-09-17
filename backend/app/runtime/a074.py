from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A074SupportTriageError(RuntimeError): pass
REQUIRED = {"status","severity","category","route_to","playbook","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("support_ticket"), dict):
        raise A074SupportTriageError("A074 requires support_ticket as an object")

async def run_a074_support_triage(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"support_ticket": request["support_ticket"], "customer_health": request.get("customer_health") or {}, "triage_rules": request.get("triage_rules") or [], "triage_constraints": request.get("triage_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A074", "Triage support ticket by severity, category and playbook. Return ONLY A074 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A074SupportTriageError("A074 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route ticket to assigned queue or Customer Success Planner (A075).")
    missing = REQUIRED - set(output)
    if missing: raise A074SupportTriageError(f"A074 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A074SupportTriageError("A074 confidence must be high, medium, or low")
    for f in ["assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A074SupportTriageError(f"A074 {f} must be an array")
    if not isinstance(output.get("playbook"), dict): raise A074SupportTriageError("A074 playbook must be an object")
    return RunResult(llm.run_id, "A074", "support.triage+ollama", "completed", result=output)
