"""Improvement Plan P2 — skill-wired workflow + prompt coverage."""
from __future__ import annotations

import asyncio
from pathlib import Path

from backend.app.runtime.prompt_loader import list_available_prompts, resolve_prompt
from backend.app.runtime.workflows.lead_outreach import LeadOutreachOrchestrator, WorkflowState
from backend.app.runtime.workflows.skill_steps import STEP_ORDER, STEP_PROMPT_MAP, STEP_SKILL_MAP

ROOT = Path(__file__).resolve().parents[2]


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_step_skill_map_covers_pipeline():
    for step in STEP_ORDER:
        assert step in STEP_SKILL_MAP
        assert step in STEP_PROMPT_MAP


def test_advance_to_draft_records_skill_contracts():
    orch = LeadOutreachOrchestrator()
    lead = {"email": "p2@acme.test", "company": "Acme", "name": "Pat", "score": 80}
    run = orch.start(campaign_id="p2-camp", lead=lead, dry_run=True, actor="test")
    run = _run(orch.advance_to_draft(run.run_id))
    assert run.state == WorkflowState.AWAIT_APPROVAL
    disc = run.artifacts.get("discover") or {}
    skill = disc.get("skill") if isinstance(disc, dict) else None
    assert isinstance(skill, dict)
    assert skill.get("skill_id") == "SK034"
    assert skill.get("mode") in {"skill_contract", "mock_fallback", "mock_only"}
    assert (run.artifacts.get("email_draft") or {}).get("to") == "p2@acme.test"


def test_pr009_plus_bodies_resolvable():
    for pid in ["PR009", "PR010", "PR011", "PR012"]:
        assert (ROOT / "prompts" / "bodies" / f"{pid}.md").exists()
        assert len(resolve_prompt(pid, require_body=True)["body"]) > 40
    assert "PR009" in list_available_prompts()


def test_revenue_prompt_map_file():
    text = (ROOT / "prompts" / "agent-prompt-map.yaml").read_text()
    assert "revenue_path:" in text or "A044" in text
