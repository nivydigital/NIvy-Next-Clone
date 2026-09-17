"""Improvement Plan P2 tests."""
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
        assert step in STEP_SKILL_MAP and step in STEP_PROMPT_MAP


def test_advance_to_draft_records_skill_contracts():
    orch = LeadOutreachOrchestrator()
    run = orch.start(campaign_id="p2-camp", lead={"email": "p2@acme.test", "company": "Acme", "name": "Pat"}, dry_run=True)
    run = _run(orch.advance_to_draft(run.run_id))
    assert run.state == WorkflowState.AWAIT_APPROVAL
    skill = (run.artifacts.get("discover") or {}).get("skill")
    assert isinstance(skill, dict) and skill.get("skill_id") == "SK034"


def test_pr009_plus_bodies_resolvable():
    for pid in ["PR009", "PR010", "PR011", "PR012"]:
        assert (ROOT / "prompts" / "bodies" / f"{pid}.md").exists()
        assert len(resolve_prompt(pid, require_body=True)["body"]) > 20
    assert "PR009" in list_available_prompts()


def test_revenue_prompt_map_file():
    assert (ROOT / "prompts" / "revenue-path-prompts.yaml").exists()
