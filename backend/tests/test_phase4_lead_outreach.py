"""Phase 4 — Lead → Outreach workflow contract tests (mock / dry-run)."""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

os.environ["TOOLS_MOCK_ALL"] = "1"
os.environ["EMAIL_MOCK"] = "1"
os.environ["LEAD_OUTREACH_DRY_RUN"] = "1"

from backend.app.runtime.workflows.lead_outreach import (
    LeadOutreachOrchestrator,
    WorkflowState,
    make_idempotency_key,
)

EVIDENCE_DIR = Path(__file__).resolve().parents[2] / "docs" / "complete-automation-plan" / "evidence" / "phase4-lead-outreach"


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_idempotency_key_stable():
    lead = {"email": "A@B.com", "company": "Acme", "external_id": "x1"}
    k1 = make_idempotency_key("camp-1", lead)
    k2 = make_idempotency_key("camp-1", {"email": "a@b.com", "company": "acme", "external_id": "x1"})
    assert k1 == k2
    assert k1.startswith("lead-outreach:camp-1:")


def test_start_idempotent():
    orch = LeadOutreachOrchestrator()
    lead = {"email": "idem@example.com", "company": "IdemCo", "name": "Idem"}
    r1 = orch.start(campaign_id="c1", lead=lead, dry_run=True, actor="test")
    r2 = orch.start(campaign_id="c1", lead=lead, dry_run=True, actor="test")
    assert r1.run_id == r2.run_id


def test_state_machine_happy_path_dry_run():
    orch = LeadOutreachOrchestrator()
    lead = {"email": "prospect@acme.test", "company": "Acme", "name": "Alex", "score": 75}
    run = orch.start(campaign_id="rev-q3", lead=lead, dry_run=True, actor="tester")
    assert run.state == WorkflowState.PENDING
    run = _run(orch.advance_to_draft(run.run_id))
    assert run.state == WorkflowState.AWAIT_APPROVAL
    run = orch.approve(run.run_id, actor="human:owner")
    assert run.state == WorkflowState.APPROVED
    run = _run(orch.send(run.run_id))
    assert run.state == WorkflowState.SENT
    assert run.artifacts["send_receipt"].get("dry_run") or run.artifacts["send_receipt"].get("mock")
    run = orch.schedule_followup(run.run_id)
    assert run.state == WorkflowState.FOLLOWING_UP
    run = orch.complete(run.run_id)
    assert run.state == WorkflowState.DONE
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    (EVIDENCE_DIR / "happy_path_dry_run.json").write_text(json.dumps({"run": run.to_dict(), "notes": "Controlled E2E with mocks"}, indent=2))


def test_reject_cancels():
    orch = LeadOutreachOrchestrator()
    run = orch.start(campaign_id="c-reject", lead={"email": "r@x.com", "company": "X", "name": "R"}, dry_run=True)
    _run(orch.advance_to_draft(run.run_id))
    run = orch.reject(run.run_id, actor="human", reason="off brand")
    assert run.state == WorkflowState.CANCELLED


def test_send_requires_approval_state():
    orch = LeadOutreachOrchestrator()
    run = orch.start(campaign_id="c-no-approve", lead={"email": "n@x.com", "company": "X", "name": "N"}, dry_run=True)
    try:
        _run(orch.send(run.run_id))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_illegal_transition():
    orch = LeadOutreachOrchestrator()
    run = orch.start(campaign_id="c-illegal", lead={"email": "i@x.com", "company": "X", "name": "I"}, dry_run=True)
    try:
        orch.approve(run.run_id)
        assert False, "expected ValueError"
    except ValueError:
        pass
