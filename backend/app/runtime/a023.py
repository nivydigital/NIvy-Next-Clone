from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A023RevOpsStrategyError(RuntimeError): pass

REQUIRED = {"status","operating_model","process_ownership","systems_guidance","kpi_hierarchy","handoff_map","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("gtm_strategy", "pipeline_deal_strategy"):
        if not isinstance(request.get(name), dict):
            raise A023RevOpsStrategyError(f"A023 requires {name} as an object")

async def run_a023_revops(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"gtm_strategy": request["gtm_strategy"], "pipeline_deal_strategy": request["pipeline_deal_strategy"], "lead_generation_strategy": request.get("lead_generation_strategy") or {}, "retention_expansion_strategy": request.get("retention_expansion_strategy") or {}, "campaign_strategy": request.get("campaign_strategy") or {}, "revops_constraints": request.get("revops_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A023", "Define RevOps operating model, process ownership and KPI hierarchy from the supplied GTM and pipeline context. Return ONLY A023 JSON.", "PR029", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A023RevOpsStrategyError("A023 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass RevOps strategy to operations, analytics and systems agents.")
    missing = REQUIRED - set(output)
    if missing: raise A023RevOpsStrategyError(f"A023 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A023RevOpsStrategyError("A023 confidence must be high, medium, or low")
    for f in ["process_ownership", "kpi_hierarchy", "handoff_map", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A023RevOpsStrategyError(f"A023 {f} must be an array")
    for f in ["operating_model", "systems_guidance"]:
        if not isinstance(output.get(f), dict): raise A023RevOpsStrategyError(f"A023 {f} must be an object")
    return RunResult(llm.run_id, "A023", "revops.strategy+ollama", "completed", result=output)
