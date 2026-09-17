from __future__ import annotations

from typing import Any


def evaluate_runtime(engine) -> dict[str, Any]:
    """Deterministic smoke/evaluation suite for the control boundary."""
    checks: dict[str, bool] = {}
    checks["registry_nonempty"] = bool(engine.registry.get("agents")) and bool(engine.registry.get("tools"))
    checks["default_deny"] = engine.registry.get("policy", {}).get("default_deny") is True
    checks["all_agents_have_tools"] = all(a.get("tools") for a in engine.registry.get("agents", []))
    checks["protected_side_effects_declared"] = any(t.get("protected") for t in engine.registry.get("tools", []))
    checks["approval_required_for_protected"] = _approval_gate(engine)
    return {"passed": sum(checks.values()), "total": len(checks), "checks": checks,
            "release_gate": all(checks.values())}


def _approval_gate(engine) -> bool:
    try:
        engine._check("A044", "tool.email.send", None)
    except Exception:
        return True
    return False
