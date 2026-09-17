from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine


class A116Error(RuntimeError):
    pass


REQUIRED = {
    "package_manifest", "dependency_lock", "skill_bindings", "install_readiness", "gaps", "status", "confidence", "assumptions", "derived_from", "warnings", "errors", "next_action",
}


def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("agent_spec"), dict):
        raise A116Error("A116 requires agent_spec as an object")
    if not isinstance(request.get("certification_verdict"), dict):
        raise A116Error("A116 requires certification_verdict as an object")


async def run_a116_agent_package_builder(request: dict[str, Any]) -> RunResult:
    """Agent Package Builder — governed analysis/plan only; no unauthorized side effects."""
    _check(request)
    context = {
        "agent_spec": request["agent_spec"],
        "certification_verdict": request["certification_verdict"],
        "dependency_map": request.get("dependency_map") or {},
        "skill_bindings": request.get("skill_bindings") or {},
        "schema_versions": request.get("schema_versions") or {},
        "prior_package": request.get("prior_package") or {},
        "packaging_constraints": request.get("packaging_constraints") or {},
        "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]},
        "constraints": [
            "No publish or install side effects",
            "No secret exposure",
            "Install readiness must be explicit",
        ],
    }
    llm = await runtime_engine.run_llm(
        "A116",
        "Build an agent package from the agent_spec and certification_verdict. Produce package_manifest, dependency_lock, skill_bindings, install_readiness and gaps. Return ONLY A116 JSON. Do not publish or install.",
        "PR005",
        context,
    )
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A116Error("A116 model did not return valid JSON") from exc
    output.setdefault("warnings", [])
    output.setdefault("errors", [])
    output.setdefault("next_action", "If install_readiness is green, hand package to Marketplace Curator (A120) for listing; otherwise close gaps.")
    missing = REQUIRED - set(output)
    if missing:
        raise A116Error(f"A116 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A116Error("A116 confidence must be high, medium, or low")
    for f in ["skill_bindings", "gaps", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list):
            raise A116Error(f"A116 {f} must be an array")
    for f in ["package_manifest", "dependency_lock", "install_readiness"]:
        if not isinstance(output.get(f), dict):
            raise A116Error(f"A116 {f} must be an object")
    return RunResult(llm.run_id, "A116", "a116.ollama", "completed", result=output)
