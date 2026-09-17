"""A4 — Unit tests for lead-path skills SK034–SK050 (STD-01 load + run)."""
from __future__ import annotations

import pytest

from backend.app.runtime.skill_resolver import (
    SkillResolveError,
    list_skill_ids,
    load_skill,
    run_skill,
)

LEAD_SKILLS = [f"SK{i:03d}" for i in range(34, 51)]


def test_lead_skills_present():
    ids = set(list_skill_ids())
    missing = [s for s in LEAD_SKILLS if s not in ids]
    assert not missing, f"missing lead skill files: {missing}"


@pytest.mark.parametrize("skill_id", LEAD_SKILLS)
def test_lead_skill_loads_std01(skill_id: str):
    data = load_skill(skill_id)
    assert data["id"] == skill_id
    assert data.get("version")
    assert data.get("objective")
    assert data.get("non_goals") is not None
    assert data.get("inputs") is not None
    assert data.get("outputs") is not None
    assert isinstance(data.get("procedure"), list) and len(data["procedure"]) >= 3
    assert data.get("quality_checks") is not None
    assert data.get("failure_policy")
    assert data.get("evidence_policy")
    assert data.get("dependencies") is not None
    assert data.get("acceptance_criteria") is not None
    assert data.get("evaluation") is not None
    assert data.get("provenance") is not None


@pytest.mark.parametrize("skill_id", ["SK034", "SK036", "SK039", "SK044", "SK049"])
def test_priority_skills_run_happy_path(skill_id: str):
    result = run_skill(skill_id, context={"sample": True, "icp": {"industry": "saas"}})
    assert result.status in {"completed", "partial"}
    assert result.skill_id == skill_id
    assert result.procedure_log
    assert result.run_id


@pytest.mark.parametrize("skill_id", ["SK034", "SK036", "SK039", "SK044", "SK049"])
def test_priority_skills_fail_closed_empty_context(skill_id: str):
    result = run_skill(skill_id, context={})
    assert result.status == "failed"
    assert result.errors


def test_unknown_skill_raises():
    with pytest.raises(SkillResolveError):
        load_skill("SK999")
