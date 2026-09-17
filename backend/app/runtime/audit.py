from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4


class AuditLog:
    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []
        self._lock = Lock()

    def record(self, *, event_type: str, actor: str, action: str, status: str, request_id: str | None = None, data: dict[str, Any] | None = None) -> dict[str, Any]:
        event = {
            "event_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id or str(uuid4()),
            "event_type": event_type,
            "actor": actor,
            "action": action,
            "status": status,
            "data": data or {},
        }
        with self._lock:
            self._events.append(event)
        return event

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._events)


audit_log = AuditLog()
