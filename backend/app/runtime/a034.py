from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A034LeadDiscoveryError(RuntimeError): pass
REQUIRED = {"status","leads","sources","match_rationale","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "lead_generation_strategy"):
        if not isinstance(request.get(name), dict):
            raise A034LeadDiscoveryError(f"A034 requires {name} as an object")

async def run_a034_lead_discovery(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"icp_definition": request["icp_definition"], "lead_generation_strategy": request["lead_generation_strategy"], "targeting_rules": request.get("targeting_rules") or [], "channel_strategy": request.get("channel_strategy") or {}, "discovery_constraints": request.get("discovery_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A034", "Discover target leads matching ICP and lead-generation strategy. Return ONLY A034 JSON with public-source-backed candidates.", "PR003", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A034LeadDiscoveryError("A034 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass discovered leads to Contact Discovery (A035).")
    missing = REQUIRED - set(output)
    if missing: raise A034LeadDiscoveryError(f"A034 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A034LeadDiscoveryError("A034 confidence must be high, medium, or low")
    for f in ["leads", "sources", "match_rationale", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A034LeadDiscoveryError(f"A034 {f} must be an array")
    return RunResult(llm.run_id, "A034", "lead.discovery+ollama", "completed", result=output)
