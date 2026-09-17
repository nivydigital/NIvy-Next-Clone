from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A103Error(RuntimeError):
    pass


REQUIRED = {
    "evidence_pack", "coverage", "gaps", "integrity_notes", "recommendations", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("run_refs"), dict):
        raise A103Error("A103 requires run_refs as an object")
    if not isinstance(request.get("evidence_scope"), dict):
        raise A103Error("A103 requires evidence_scope as an object")


async def run_a103_evidence_collector(request: dict[str, Any]) -> RunResult:
    """Evidence Collector — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "run_refs": request["run_refs"],
        "evidence_scope": request["evidence_scope"],
        "trace_snippets": request.get("trace_snippets") or {},
        "score_cards": request.get("score_cards") or {},
        "artifact_index": request.get("artifact_index") or {},
        "prior_evidence_pack": request.get("prior_evidence_pack") or {},
        "retention_policy": request.get("retention_policy") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No production evidence-store writes",
            "No secret exposure",
            "Gaps must be explicit",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A103",
        "Assemble an evidence pack from run_refs and evidence_scope. Produce evidence_pack, coverage, gaps, integrity_notes and recommendations. Return ONLY A103 JSON.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A103Error("A103 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Attach evidence_pack to Evaluation Analyst (A098) or Improvement Promotion Reviewer (A109).")
    missing = REQUIRED - set(output)
    if missing:
        raise A103Error(f"A103 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A103Error("A103 confidence must be high, medium, or low")
    for f in ["gaps", "integrity_notes", "recommendations", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A103Error(f"A103 {f} must be an array")
    for f in ["evidence_pack", "coverage"]:
        if not isinstance(output.get(f), dict):
            raise A103Error(f"A103 {f} must be an object")
    return RunResult(llm.run_id, "A103", "a103.ollama", "completed", result=output)
