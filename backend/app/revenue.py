from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from threading import Lock
from typing import Any
from uuid import uuid4


class LeadStatus(StrEnum):
    NEW = "new"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    WON = "won"
    LOST = "lost"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RevenueLead:
    id: str
    name: str
    email: str
    company: str | None = None
    source: str = "unknown"
    status: LeadStatus = LeadStatus.NEW
    score: int = 0
    next_action: str = "qualify"
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "email": self.email, "company": self.company, "source": self.source, "status": self.status.value, "score": self.score, "next_action": self.next_action, "created_at": self.created_at, "updated_at": self.updated_at}


class RevenueEngine:
    """Portable Revenue Engine with SQLite persistence, idempotency, and audit trail.

    Protected side effects are not executed here. Approval is explicit and auditable.
    Set NIVY_REVENUE_DB_PATH=:memory: for isolated tests; defaults to data/revenue.db.
    """

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or os.getenv("NIVY_REVENUE_DB_PATH", "data/revenue.db")
        if self.db_path != ":memory:":
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self._lock = Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS leads (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
                company TEXT, source TEXT NOT NULL, status TEXT NOT NULL,
                score INTEGER NOT NULL, next_action TEXT NOT NULL,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS approvals (
                lead_id TEXT PRIMARY KEY, approved_at TEXT NOT NULL, actor TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS idempotency_keys (
                request_id TEXT PRIMARY KEY, lead_id TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT NOT NULL,
                lead_id TEXT, actor TEXT NOT NULL, request_id TEXT, payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """)

    @staticmethod
    def _row_to_lead(row: sqlite3.Row) -> RevenueLead:
        return RevenueLead(id=row["id"], name=row["name"], email=row["email"], company=row["company"], source=row["source"], status=LeadStatus(row["status"]), score=row["score"], next_action=row["next_action"], created_at=row["created_at"], updated_at=row["updated_at"])

    def _audit(self, conn: sqlite3.Connection, event_type: str, lead_id: str | None, actor: str, request_id: str | None, payload: dict[str, Any]) -> None:
        import json
        conn.execute("INSERT INTO audit_events(event_type,lead_id,actor,request_id,payload,created_at) VALUES (?,?,?,?,?,?)", (event_type, lead_id, actor, request_id, json.dumps(payload, sort_keys=True), _now()))

    def create_lead(self, *, name: str, email: str, company: str | None, source: str, request_id: str | None = None, actor: str = "system") -> RevenueLead:
        with self._lock, self._connect() as conn:
            if request_id:
                existing = conn.execute("SELECT lead_id FROM idempotency_keys WHERE request_id=?", (request_id,)).fetchone()
                if existing:
                    row = conn.execute("SELECT * FROM leads WHERE id=?", (existing["lead_id"],)).fetchone()
                    return self._row_to_lead(row)
            lead = RevenueLead(id=str(uuid4()), name=name, email=email, company=company, source=source)
            conn.execute("INSERT INTO leads VALUES (?,?,?,?,?,?,?,?,?,?)", (lead.id, lead.name, lead.email, lead.company, lead.source, lead.status.value, lead.score, lead.next_action, lead.created_at, lead.updated_at))
            if request_id:
                conn.execute("INSERT INTO idempotency_keys VALUES (?,?)", (request_id, lead.id))
            self._audit(conn, "lead_created", lead.id, actor, request_id, lead.to_dict())
            return lead

    def list_leads(self) -> list[RevenueLead]:
        with self._lock, self._connect() as conn:
            return [self._row_to_lead(r) for r in conn.execute("SELECT * FROM leads ORDER BY created_at")]

    def get_lead(self, lead_id: str) -> RevenueLead | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
            return self._row_to_lead(row) if row else None

    def _mutate(self, lead_id: str, event_type: str, actor: str, request_id: str | None, fn) -> RevenueLead:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
            if not row:
                raise KeyError(lead_id)
            lead = self._row_to_lead(row)
            fn(lead)
            lead.updated_at = _now()
            conn.execute("UPDATE leads SET status=?,score=?,next_action=?,updated_at=? WHERE id=?", (lead.status.value, lead.score, lead.next_action, lead.updated_at, lead.id))
            self._audit(conn, event_type, lead.id, actor, request_id, lead.to_dict())
            return lead

    def qualify(self, lead_id: str, *, score: int, actor: str = "system", request_id: str | None = None) -> RevenueLead:
        if not 0 <= score <= 100:
            raise ValueError("score must be between 0 and 100")
        return self._mutate(lead_id, "lead_qualified", actor, request_id, lambda lead: (setattr(lead, "score", score), setattr(lead, "status", LeadStatus.QUALIFIED if score >= 50 else LeadStatus.NEW), setattr(lead, "next_action", "prepare_proposal" if score >= 50 else "nurture")))

    def request_proposal_approval(self, lead_id: str, actor: str = "system", request_id: str | None = None) -> RevenueLead:
        return self._mutate(lead_id, "proposal_approval_requested", actor, request_id, lambda lead: setattr(lead, "next_action", "approval_required"))

    def approve_proposal(self, lead_id: str, actor: str = "human", request_id: str | None = None) -> RevenueLead:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
            if not row:
                raise KeyError(lead_id)
            lead = self._row_to_lead(row)
            lead.status, lead.next_action, lead.updated_at = LeadStatus.PROPOSAL, "send_proposal", _now()
            conn.execute("UPDATE leads SET status=?,next_action=?,updated_at=? WHERE id=?", (lead.status.value, lead.next_action, lead.updated_at, lead.id))
            conn.execute("INSERT OR REPLACE INTO approvals VALUES (?,?,?)", (lead_id, lead.updated_at, actor))
            self._audit(conn, "proposal_approved", lead.id, actor, request_id, lead.to_dict())
            return lead

    def approval_exists(self, lead_id: str) -> bool:
        with self._lock, self._connect() as conn:
            return conn.execute("SELECT 1 FROM approvals WHERE lead_id=?", (lead_id,)).fetchone() is not None

    def audit_events(self, lead_id: str | None = None) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute("SELECT event_type,lead_id,actor,request_id,payload,created_at FROM audit_events WHERE (? IS NULL OR lead_id=?) ORDER BY id", (lead_id, lead_id)).fetchall()
            import json
            return [{**dict(r), "payload": json.loads(r["payload"])} for r in rows]


revenue_engine = RevenueEngine()
