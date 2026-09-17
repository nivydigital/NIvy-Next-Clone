from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A016PipelineDealError(RuntimeError): pass

REQUIRED = {
    "status", "stages", "progression_rules", "deal_qualification", "forecast_guidance",
    "exit_criteria", "confidence", "assumptions", "derived_from",
    "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "qualification_scoring_strategy"):
        if not isinstance(request.get(name), dict):
            raise A016PipelineDealError(f"A016 requires {name} as an object")

async def run_a016_pipeline(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "qualification_scoring_strategy": request["qualification_scoring_strategy"],
        "sales_enablement_strategy": request.get("sales_enablement_strategy") or {},
        "gtm_strategy": request.get("gtm_strategy") or {},
        "historical_pipeline": request.get("historical_pipeline") or {},
        "pipeline_constraints": request.get("pipeline_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A016",
        "Define pipeline stages, progression rules and forecast guidance from the supplied ICP and qualification context. Return ONLY A016 JSON.",
        "PR022",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A016PipelineDealError("A016 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass pipeline strategy to CRM, forecasting and sales operations agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A016PipelineDealError(f"A016 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A016PipelineDealError("A016 confidence must be high, medium, or low")
    for f in ["stages", "progression_rules", "exit_criteria", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A016PipelineDealError(f"A016 {f} must be an array")
    for f in ["deal_qualification", "forecast_guidance"]:
        if not isinstance(output.get(f), dict):
            raise A016PipelineDealError(f"A016 {f} must be an object")
    return RunResult(llm.run_id, "A016", "pipeline.deal+ollama", "completed", result=output)
