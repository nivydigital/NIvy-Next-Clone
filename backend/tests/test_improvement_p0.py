"""Improvement Plan P0 — skill resolver + prompt loader."""
from __future__ import annotations

from backend.app.runtime.prompt_loader import (
    PromptLoadError,
    build_messages,
    list_available_prompts,
    load_body_file,
    resolve_prompt,
)
from backend.app.runtime.skill_resolver import (
    SkillResolveError,
    list_skill_ids,
    load_skill,
    run_skill,
)


def test_at_least_50_skills_present():
    ids = list_skill_ids()
    assert len(ids) >= 50, f"expected >=50 skills, got {len(ids)}"


def test_load_skill_std01_fields():
    skill = load_skill("SK034")
    assert skill["id"] == "SK034"
    assert "procedure" in skill


def test_run_skill_happy_path():
    result = run_skill("SK034", context={"icp": {"industry": "saas"}}, actor="test")
    assert result.status == "completed"
    assert result.result.get("skill_id") == "SK034"


def test_run_skill_fail_closed_empty_context():
    result = run_skill("SK034", context={}, actor="test")
    assert result.status == "failed"
    assert result.errors


def test_unknown_skill_raises():
    try:
        load_skill("SK999")
        assert False
    except SkillResolveError:
        pass


def test_prompt_bodies_exist():
    assert load_body_file("PR001")
    assert "PR001" in list_available_prompts()


def test_resolve_prompt_merges_body():
    resolved = resolve_prompt("PR001", require_body=True)
    assert resolved["id"] == "PR001"
    assert len(resolved["body"]) > 50


def test_build_messages_includes_context():
    text = build_messages("PR003", agent_id="A034", agent_name="Lead Discovery", context={"icp_definition": {"name": "test"}})
    assert "A034" in text and "PR003" in text and "icp_definition" in text


def test_unknown_prompt_raises():
    try:
        resolve_prompt("PR999", require_body=True)
        assert False
    except PromptLoadError:
        pass
