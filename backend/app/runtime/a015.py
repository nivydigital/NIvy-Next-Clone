from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A015QualificationScoringError(RuntimeError): pass

REQUIRED = {
    "status", "qualification_criteria", "scoring_model", "routing_rules",
    "disqualification_rules", "handoff_triggers", "confidence", "assumptions",
    "derived_from", "warnings", "errors", "next_action",
}

def _check(request: dict[str, Any]) -> None:
    for name in ("icp_definition", "sales_enablement_strategy"):
        if not isinstance(request.get(name), dict):
            raise A015QualificationScoringError(f"A015 requires {name} as an object")

async def run_a015_qualification(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {
        "icp_definition": request["icp_definition"],
        "sales_enablement_strategy": request["sales_enablement_strategy"],
        "buyer_personas": request.get("buyer_personas") or {},
        "lead_generation_strategy": request.get("lead_generation_strategy") or {},
        "gtm_strategy": request.get("gtm_strategy") or {},
        "scoring_constraints": request.get("scoring_constraints") or [],
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
    }
    llm = await runtime_engine.run_llm(
        "A015",
        "Define lead qualification criteria, scoring model and routing rules from the supplied ICP and sales enablement context. Return ONLY A015 JSON.",
        "PR021",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A015QualificationScoringError("A015 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Pass qualification and scoring strategy to scoring, routing and CRM agents.")
    missing = REQUIRED - set(output)
    if missing:
        raise A015QualificationScoringError(f"A015 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A015QualificationScoringError("A015 confidence must be high, medium, or low")
    for f in ["qualification_criteria", "routing_rules", "disqualification_rules", "handoff_triggers", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A015QualificationScoringError(f"A015 {f} must be an array")
    if not isinstance(output.get("scoring_model"), dict):
        raise A015QualificationScoringError("A015 scoring_model must be an object")
    return RunResult(llm.run_id, "A015", "qualification.scoring+ollama", "completed", result=output)
