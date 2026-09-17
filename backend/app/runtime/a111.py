from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A111Error(RuntimeError):
    pass


REQUIRED = {
    "handoff_package", "acceptance_checklist", "residual_risks", "audit_notes", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("handoff_from"), dict):
        raise A111Error("A111 requires handoff_from as an object")
    if not isinstance(request.get("handoff_to"), dict):
        raise A111Error("A111 requires handoff_to as an object")
    if not isinstance(request.get("work_payload"), dict):
        raise A111Error("A111 requires work_payload as an object")


async def run_a111_agent_handoff(request: dict[str, Any]) -> RunResult:
    """Agent Handoff Manager — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "handoff_from": request["handoff_from"],
        "handoff_to": request["handoff_to"],
        "work_payload": request["work_payload"],
        "acceptance_criteria": request.get("acceptance_criteria") or {},
        "prior_handoffs": request.get("prior_handoffs") or {},
        "risk_notes": request.get("risk_notes") or {},
        "context_refs": request.get("context_refs") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No SoR writes",
            "No secret exposure",
            "Acceptance criteria must be explicit",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A111",
        "Structure an agent handoff from handoff_from to handoff_to with the work_payload. Produce handoff_package, acceptance_checklist, residual_risks, audit_notes and recommendations. Return ONLY A111 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A111Error("A111 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Deliver handoff_package to receiving agent; log audit_notes for Collaboration Auditor (A115).")
    missing = REQUIRED - set(output)
    if missing:
        raise A111Error(f"A111 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A111Error("A111 confidence must be high, medium, or low")
    for f in ["acceptance_checklist", "residual_risks", "audit_notes", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A111Error(f"A111 {f} must be an array")
    if not isinstance(output.get("handoff_package"), dict):
        raise A111Error("A111 handoff_package must be an object")
    return RunResult(llm.run_id, "A111", "a111.ollama", "completed", result=output)
