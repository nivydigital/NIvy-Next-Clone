from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A118Error(RuntimeError):
    pass


REQUIRED = {
    "verdict", "gate_results", "evidence_gaps", "remediation", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("candidate_agent_spec"), dict):
        raise A118Error("A118 requires candidate_agent_spec as an object")


async def run_a118_agent_certification(request: dict[str, Any]) -> RunResult:
    """Agent Certification Agent — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "candidate_agent_spec": request["candidate_agent_spec"],
        "completeness_checklist": request.get("completeness_checklist") or {},
        "policy_baseline": request.get("policy_baseline") or {},
        "security_baseline": request.get("security_baseline") or {},
        "evaluation_evidence": request.get("evaluation_evidence") or {},
        "prior_certification": request.get("prior_certification") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No agent activation or registry write",
            "No secret exposure",
            "Verdict must be pass|conditional|fail",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A118",
        "Certify the candidate agent against AIOS completeness, policy, security and quality gates. Return verdict (pass|conditional|fail), gate_results, evidence_gaps and remediation. Return ONLY A118 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A118Error("A118 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "If pass/conditional, route to Agent Package Builder (A116) or Marketplace Curator (A120); if fail, return remediation to owner.")
    missing = REQUIRED - set(output)
    if missing:
        raise A118Error(f"A118 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A118Error("A118 confidence must be high, medium, or low")
    if output.get("verdict") not in {"pass", "conditional", "fail"}:
        raise A118Error("A118 verdict must be pass, conditional, or fail")
    for f in ["gate_results", "evidence_gaps", "remediation", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A118Error(f"A118 {f} must be an array")
    return RunResult(llm.run_id, "A118", "a118.ollama", "completed", result=output)
