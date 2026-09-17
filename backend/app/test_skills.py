"""Phase 3 skill tests — coverage report and fail-closed resolution."""
from __future__ import annotations

import pytest

from backend.app.runtime.skills import (
    skill_coverage_report,
    skill_implementation_exists,
    load_skill_implementation,
    resolve_agent_skills,
)
from backend.app.runtime.engine import RuntimeDenied


def test_lead_path_skills_exist():
    for sid in [f"SK{i:03d}" for i in range(34, 51)]:
        assert skill_implementation_exists(sid), f"missing {sid}"


def test_load_sk034_has_required_fields():
    impl = load_skill_implementation("SK034")
    assert impl["id"] == "SK034"
    assert impl["procedure"]
    assert impl["quality_checks"]


def test_coverage_report_structure():
    report = skill_coverage_report()
    assert "registry_count" in report
    assert "implementation_count" in report
    assert "missing_implementations" in report


def test_resolve_unknown_agent_fails():
    with pytest.raises(RuntimeDenied):
        resolve_agent_skills("A99999")
