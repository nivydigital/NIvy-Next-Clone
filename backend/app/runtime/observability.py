"""Lightweight observability helpers (Phase 10 / P10.3)."""
from __future__ import annotations

from collections import Counter
from typing import Any

from .audit import audit_log


def audit_summary() -> dict[str, Any]:
    events = audit_log.list()
    by_type = Counter(e.get("event_type") for e in events)
    by_status = Counter(e.get("status") for e in events)
    errors = [e for e in events if e.get("status") in {"error", "failed"}]
    return {
        "total_events": len(events),
        "by_event_type": dict(by_type),
        "by_status": dict(by_status),
        "error_count": len(errors),
        "recent_errors": errors[-10:],
    }


def health_snapshot(*, checks: dict[str, bool] | None = None) -> dict[str, Any]:
    checks = checks or {}
    return {"ok": all(checks.values()) if checks else True, "checks": checks, "audit": audit_summary()}
