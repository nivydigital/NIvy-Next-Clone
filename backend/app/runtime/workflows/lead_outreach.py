"""Lead → Outreach orchestrator (Phase 4 + P2 skill contracts)."""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from threading import Lock
from typing import Any
from uuid import uuid4

from ..audit import audit_log
from ..tools import execute_tool
from .skill_steps import STEP_ORDER, STEP_PROMPT_MAP, STEP_SKILL_MAP, run_pipeline_steps

__all__ = ["WorkflowState", "LeadOutreachOrchestrator", "lead_outreach", "make_idempotency_key", "STEP_ORDER", "STEP_SKILL_MAP", "STEP_PROMPT_MAP"]


class WorkflowState(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    AWAIT_APPROVAL = "await_approval"
    APPROVED = "approved"
    SENDING = "sending"
    SENT = "sent"
    FOLLOWING_UP = "following_up"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


ALLOWED_TRANSITIONS: dict[WorkflowState, set[WorkflowState]] = {
    WorkflowState.PENDING: {WorkflowState.RUNNING, WorkflowState.CANCELLED},
    WorkflowState.RUNNING: {WorkflowState.AWAIT_APPROVAL, WorkflowState.FAILED, WorkflowState.CANCELLED},
    WorkflowState.AWAIT_APPROVAL: {WorkflowState.APPROVED, WorkflowState.CANCELLED, WorkflowState.FAILED},
    WorkflowState.APPROVED: {WorkflowState.SENDING, WorkflowState.CANCELLED},
    WorkflowState.SENDING: {WorkflowState.SENT, WorkflowState.FAILED},
    WorkflowState.SENT: {WorkflowState.FOLLOWING_UP, WorkflowState.DONE},
    WorkflowState.FOLLOWING_UP: {WorkflowState.DONE, WorkflowState.AWAIT_APPROVAL, WorkflowState.FAILED},
    WorkflowState.DONE: set(),
    WorkflowState.FAILED: set(),
    WorkflowState.CANCELLED: set(),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_idempotency_key(campaign_id: str, lead: dict[str, Any]) -> str:
    email = str(lead.get("email") or "").strip().lower()
    company = str(lead.get("company") or "").strip().lower()
    external = str(lead.get("external_id") or lead.get("id") or "").strip()
    digest = hashlib.sha256(f"{campaign_id}|{email}|{company}|{external}".encode()).hexdigest()[:16]
    return f"lead-outreach:{campaign_id}:{digest}"


@dataclass
class WorkflowRun:
    run_id: str
    campaign_id: str
    idempotency_key: str
    state: WorkflowState = WorkflowState.PENDING
    dry_run: bool = True
    actor: str = "system"
    lead: dict[str, Any] = field(default_factory=dict)
    steps_completed: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "campaign_id": self.campaign_id,
            "idempotency_key": self.idempotency_key,
            "state": self.state.value,
            "dry_run": self.dry_run,
            "actor": self.actor,
            "lead": self.lead,
            "steps_completed": list(self.steps_completed),
            "artifacts": dict(self.artifacts),
            "errors": list(self.errors),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class LeadOutreachOrchestrator:
    def __init__(self) -> None:
        self._runs: dict[str, WorkflowRun] = {}
        self._by_idempotency: dict[str, str] = {}
        self._lock = Lock()

    def _transition(self, run: WorkflowRun, new_state: WorkflowState, event: str) -> None:
        allowed = ALLOWED_TRANSITIONS.get(run.state, set())
        if new_state not in allowed:
            raise ValueError(f"illegal transition {run.state.value} → {new_state.value} on {event}")
        old = run.state
        run.state = new_state
        run.updated_at = _now()
        audit_log.record(
            event_type="workflow.transition",
            actor=run.actor,
            action="lead-outreach",
            status=new_state.value,
            request_id=run.run_id,
            data={"from": old.value, "to": new_state.value, "event": event},
        )

    def start(self, *, campaign_id: str, lead: dict[str, Any], dry_run: bool | None = None, actor: str = "system", seed_artifacts: dict[str, Any] | None = None) -> WorkflowRun:
        if not campaign_id:
            raise ValueError("campaign_id is required")
        if not isinstance(lead, dict) or not lead:
            raise ValueError("lead object is required")
        if dry_run is None:
            dry_run = os.getenv("LEAD_OUTREACH_DRY_RUN", "1") != "0"
        key = make_idempotency_key(campaign_id, lead)
        with self._lock:
            existing_id = self._by_idempotency.get(key)
            if existing_id and existing_id in self._runs:
                return self._runs[existing_id]
            run = WorkflowRun(
                run_id=str(uuid4()),
                campaign_id=campaign_id,
                idempotency_key=key,
                dry_run=bool(dry_run),
                actor=actor,
                lead=dict(lead),
                artifacts=dict(seed_artifacts or {}),
            )
            self._runs[run.run_id] = run
            self._by_idempotency[key] = run.run_id
        audit_log.record(
            event_type="workflow.started",
            actor=actor,
            action="lead-outreach",
            status="pending",
            request_id=run.run_id,
            data={"campaign_id": campaign_id, "idempotency_key": key, "dry_run": run.dry_run},
        )
        return run

    def get(self, run_id: str) -> WorkflowRun | None:
        return self._runs.get(run_id)

    async def advance_to_draft(self, run_id: str) -> WorkflowRun:
        run = self._require(run_id)
        if run.state == WorkflowState.PENDING:
            self._transition(run, WorkflowState.RUNNING, "start")
        if run.state != WorkflowState.RUNNING:
            if run.state == WorkflowState.AWAIT_APPROVAL:
                return run
            raise ValueError(f"cannot advance_to_draft from state {run.state.value}")
        lead = run.lead
        steps, artifacts, errors = run_pipeline_steps(
            lead=lead,
            campaign_id=run.campaign_id,
            dry_run=run.dry_run,
            actor=run.actor,
            steps_completed=list(run.steps_completed),
            artifacts=dict(run.artifacts),
            mock_step=self._mock_step,
        )
        run.steps_completed = steps
        run.artifacts = artifacts
        run.errors.extend(errors)
        for step in steps:
            skill_meta = (run.artifacts.get(step) or {}).get("skill") if isinstance(run.artifacts.get(step), dict) else {}
            audit_log.record(
                event_type="workflow.step",
                actor=run.actor,
                action=step,
                status="completed",
                request_id=run.run_id,
                data={
                    "step": step,
                    "skill_id": (skill_meta or {}).get("skill_id"),
                    "prompt_id": (skill_meta or {}).get("prompt_id"),
                    "dry_run": run.dry_run,
                    "mode": (skill_meta or {}).get("mode"),
                },
            )
        email = str(lead.get("email") or "").strip()
        if email and "verify" in run.steps_completed:
            try:
                run.artifacts["verify_tool"] = await execute_tool(
                    tool_id="tool.email.verify",
                    arguments={"email": email},
                    actor=run.actor,
                    approved=False,
                    request_id=run.run_id,
                )
            except Exception as exc:  # noqa: BLE001
                run.errors.append(f"verify: {exc}")
        draft_art = run.artifacts.get("draft") or {}
        run.artifacts["email_draft"] = {
            "to": email,
            "subject": draft_art.get("subject") or f"Intro for {lead.get('company') or lead.get('name') or 'you'}",
            "body": draft_art.get("body") or f"Hi {lead.get('name') or 'there'},\n\nDraft for {lead.get('company') or 'your team'}.\n",
        }
        self._transition(run, WorkflowState.AWAIT_APPROVAL, "draft_ready")
        return run

    def approve(self, run_id: str, *, actor: str = "human") -> WorkflowRun:
        run = self._require(run_id)
        if run.state != WorkflowState.AWAIT_APPROVAL:
            raise ValueError(f"approve only from await_approval, got {run.state.value}")
        run.actor = actor
        run.artifacts["approval"] = {"approved_at": _now(), "actor": actor, "draft": run.artifacts.get("email_draft")}
        self._transition(run, WorkflowState.APPROVED, "approve")
        return run

    def reject(self, run_id: str, *, actor: str = "human", reason: str = "") -> WorkflowRun:
        run = self._require(run_id)
        if run.state != WorkflowState.AWAIT_APPROVAL:
            raise ValueError(f"reject only from await_approval, got {run.state.value}")
        run.artifacts["rejection"] = {"at": _now(), "actor": actor, "reason": reason}
        self._transition(run, WorkflowState.CANCELLED, "reject")
        return run

    async def send(self, run_id: str) -> WorkflowRun:
        run = self._require(run_id)
        if run.state != WorkflowState.APPROVED:
            raise ValueError(f"send only from approved, got {run.state.value}")
        self._transition(run, WorkflowState.SENDING, "send")
        draft = run.artifacts.get("email_draft") or {}
        to = str(draft.get("to") or run.lead.get("email") or "").strip()
        subject = str(draft.get("subject") or "").strip()
        body = str(draft.get("body") or "").strip()
        if not to or not subject or not body:
            run.errors.append("email draft incomplete")
            self._transition(run, WorkflowState.FAILED, "send_fail")
            return run
        try:
            if run.dry_run:
                os.environ.setdefault("EMAIL_MOCK", "1")
                receipt = {"ok": True, "mock": True, "dry_run": True, "message_id": f"dry-run-{run.run_id[:8]}", "to": to, "subject": subject}
            else:
                receipt = await execute_tool(
                    tool_id="tool.email.send",
                    arguments={"to": to, "subject": subject, "body": body},
                    actor=run.actor,
                    approved=True,
                    request_id=run.run_id,
                )
            run.artifacts["send_receipt"] = receipt
            run.steps_completed.append("send")
            self._transition(run, WorkflowState.SENT, "send_ok")
        except Exception as exc:  # noqa: BLE001
            run.errors.append(str(exc))
            self._transition(run, WorkflowState.FAILED, "send_fail")
        return run

    def schedule_followup(self, run_id: str) -> WorkflowRun:
        run = self._require(run_id)
        if run.state != WorkflowState.SENT:
            raise ValueError(f"followup only from sent, got {run.state.value}")
        run.artifacts["followup_plan"] = {"scheduled": True, "cadence_days": 3, "note": "Mock follow-up plan (A050)"}
        run.steps_completed.append("followup")
        self._transition(run, WorkflowState.FOLLOWING_UP, "schedule_followup")
        return run

    def complete(self, run_id: str) -> WorkflowRun:
        run = self._require(run_id)
        if run.state not in {WorkflowState.FOLLOWING_UP, WorkflowState.SENT}:
            raise ValueError(f"complete only from following_up|sent, got {run.state.value}")
        self._transition(run, WorkflowState.DONE, "complete")
        return run

    def _require(self, run_id: str) -> WorkflowRun:
        run = self._runs.get(run_id)
        if not run:
            raise KeyError(f"unknown run_id: {run_id}")
        return run

    def _mock_step(self, step: str, lead: dict[str, Any], prior: dict[str, Any]) -> dict[str, Any]:
        name = lead.get("name") or "unknown"
        company = lead.get("company") or "unknown"
        email = lead.get("email") or ""
        base = {"step": step, "lead_ref": email or name, "mock": True}
        if step == "discover":
            return {**base, "candidate_leads": [lead]}
        if step == "enrich":
            return {**base, "enriched": {**lead, "industry": prior.get("industry", "unknown")}}
        if step == "quality":
            return {**base, "quality_score": 0.9, "issues": []}
        if step == "verify":
            return {**base, "email": email, "verification": "pending_tool"}
        if step == "score":
            return {**base, "score": int(lead.get("score") or 70)}
        if step == "research":
            return {**base, "account_context": {"company": company, "notes": []}}
        if step == "plan":
            return {**base, "sequence": ["intro", "followup"], "channel": "email"}
        if step == "personalize":
            return {**base, "hooks": [f"relevance to {company}"]}
        if step == "draft":
            return {**base, "subject": f"Quick idea for {company}", "body": f"Hi {name},\n\nSharing a brief idea for {company}.\n"}
        return base


lead_outreach = LeadOutreachOrchestrator()
