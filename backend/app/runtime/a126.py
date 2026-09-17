from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A126Error(RuntimeError):
    pass


REQUIRED = {
    "rollout_strategy", "stages", "health_gates", "rollback_criteria", "change_window", "communication_plan", "risks", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("release_manifest"), dict):
        raise A126Error("A126 requires release_manifest as an object")
    v = request.get("environment_target")
    if not isinstance(v, str) or not v.strip():
        raise A126Error("A126 requires environment_target as a non-empty string")


async def run_a126_deployment_rollout(request: dict[str, Any]) -> RunResult:
    """Deployment Rollout Agent — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "release_manifest": request["release_manifest"],
        "environment_target": request["environment_target"],
        "current_version_map": request.get("current_version_map") or {},
        "health_baselines": request.get("health_baselines") or {},
        "change_window": request.get("change_window") or {},
        "rollback_policy": request.get("rollback_policy") or {},
        "stakeholder_list": request.get("stakeholder_list") or [],
        "prior_rollout_report": request.get("prior_rollout_report") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No live deployment or infrastructure mutation",
            "No secret exposure",
            "Health gates and rollback criteria must be measurable",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A126",
        "Produce a staged deployment rollout plan for the supplied release manifest and environment target. Include strategy, stages, health gates, rollback criteria, change window and communication plan. Return ONLY A126 JSON. Do not execute live deploy.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A126Error("A126 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "Obtain change approval; execute stages via platform CD with health gates; on failure apply rollback_criteria.")
    missing = REQUIRED - set(output)
    if missing:
        raise A126Error(f"A126 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A126Error("A126 confidence must be high, medium, or low")
    if not isinstance(output.get("rollout_strategy"), str) or not str(output.get("rollout_strategy")).strip():
        raise A126Error("A126 rollout_strategy must be a non-empty string")
    for f in ["stages", "health_gates", "rollback_criteria", "communication_plan", "risks", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A126Error(f"A126 {f} must be an array")
    if not isinstance(output.get("change_window"), dict):
        raise A126Error("A126 change_window must be an object")
    return RunResult(llm.run_id, "A126", "a126.ollama", "completed", result=output)
