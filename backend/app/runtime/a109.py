from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A109Error(RuntimeError):
    pass


REQUIRED = {
    "verdict", "evidence_assessment", "risks", "conditions", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("improvement_proposal"), dict):
        raise A109Error("A109 requires improvement_proposal as an object")
    if not isinstance(request.get("evidence_pack"), dict):
        raise A109Error("A109 requires evidence_pack as an object")


async def run_a109_improvement_promotion(request: dict[str, Any]) -> RunResult:
    """Improvement Promotion Reviewer — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "improvement_proposal": request["improvement_proposal"],
        "evidence_pack": request["evidence_pack"],
        "regression_guard_report": request.get("regression_guard_report") or {},
        "policy_baseline": request.get("policy_baseline") or {},
        "prior_promotions": request.get("prior_promotions") or {},
        "risk_appetite": request.get("risk_appetite") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production promotion writes",
            "No secret exposure",
            "Verdict must be promote|hold|reject",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A109",
        "Review the improvement_proposal against the evidence_pack. Return verdict (promote|hold|reject), evidence_assessment, risks, conditions and recommendations. Return ONLY A109 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A109Error("A109 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "If promote, queue governed change with conditions; if hold/reject, return feedback to proposer.")
    missing = REQUIRED - set(output)
    if missing:
        raise A109Error(f"A109 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A109Error("A109 confidence must be high, medium, or low")
    if output.get("verdict") not in {"promote", "hold", "reject"}:
        raise A109Error("A109 verdict must be promote, hold, or reject")
    for f in ["risks", "conditions", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A109Error(f"A109 {f} must be an array")
    if not isinstance(output.get("evidence_assessment"), dict):
        raise A109Error("A109 evidence_assessment must be an object")
    return RunResult(llm.run_id, "A109", "a109.ollama", "completed", result=output)
