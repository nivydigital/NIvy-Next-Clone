from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A035ContactDiscoveryError(RuntimeError): pass
REQUIRED = {"status","contacts","role_match","sources","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("discovered_leads", "buyer_personas"):
        if not isinstance(request.get(name), dict):
            raise A035ContactDiscoveryError(f"A035 requires {name} as an object")

async def run_a035_contact_discovery(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"discovered_leads": request["discovered_leads"], "buyer_personas": request["buyer_personas"], "icp_definition": request.get("icp_definition") or {}, "contact_constraints": request.get("contact_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A035", "Discover relevant contacts within target accounts based on personas. Return ONLY A035 JSON.", "PR003", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A035ContactDiscoveryError("A035 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass discovered contacts to Lead Enrichment (A036).")
    missing = REQUIRED - set(output)
    if missing: raise A035ContactDiscoveryError(f"A035 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A035ContactDiscoveryError("A035 confidence must be high, medium, or low")
    for f in ["contacts", "role_match", "sources", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A035ContactDiscoveryError(f"A035 {f} must be an array")
    return RunResult(llm.run_id, "A035", "contact.discovery+ollama", "completed", result=output)
