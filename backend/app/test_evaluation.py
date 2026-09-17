"""Phase 9 evaluation — offline pyramid (schema, fixtures, workflows, chains)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "agents"
FIXTURES = ROOT / "evaluation" / "fixtures" / "golden"
CHAINS = ROOT / "evaluation" / "chains.yaml"


def test_golden_fixture_index_or_generate_hint():
    """Fixtures may be generated via scripts/generate_golden_fixtures.py."""
    if not FIXTURES.exists():
        pytest.skip("run: python scripts/generate_golden_fixtures.py")
    index = FIXTURES / "INDEX.json"
    if index.exists():
        data = json.loads(index.read_text(encoding="utf-8"))
        assert data.get("count", 0) > 0


def test_sample_agents_have_schemas():
    for aid in ["A001", "A034", "A066", "A085", "A100", "A108"]:
        folder = AGENTS / aid
        if not folder.is_dir():
            pytest.skip(f"{aid} folder missing")
        assert (folder / "input.schema.json").exists(), aid
        assert (folder / "output.schema.json").exists(), aid


def test_chains_yaml_valid():
    assert CHAINS.exists()
    data = yaml.safe_load(CHAINS.read_text(encoding="utf-8"))
    assert data.get("chains")
    ids = {c["id"] for c in data["chains"]}
    assert "lead-path" in ids
    assert "inbound-comms" in ids
    assert "marketing-content" in ids


@pytest.mark.asyncio
async def test_workflow_dry_runs():
    from backend.app.runtime.workflows import run_workflow

    for wf_id in [
        "inbound-email-triage",
        "response-qa",
        "conversation-intel",
        "content-calendar",
        "seo-audit",
        "social-content-pipeline",
    ]:
        result = await run_workflow(
            wf_id,
            {
                "input": {"marketing_strategy": {"goals": ["test"]}},
                "inbound": {"message": {"subject": "hi", "body": "test"}, "mailbox": "inbox"},
            },
            dry_run=True,
        )
        assert result["workflow_id"] == wf_id
        assert result["dry_run"] is True
        assert result["state"] in {"completed", "await_approval"}
        assert result.get("history")


def test_schema_presence_control_learning():
    data = yaml.safe_load(CHAINS.read_text(encoding="utf-8"))
    for chain in data["chains"]:
        if chain.get("mode") != "schema_presence":
            continue
        for aid in chain.get("agents") or []:
            folder = AGENTS / aid
            # soft: skip if not scaffolded yet
            if not folder.is_dir():
                continue
            assert (folder / "agent.yaml").exists() or (folder / "input.schema.json").exists()


def test_runtime_modules_a100_a108():
    rt = ROOT / "backend" / "app" / "runtime"
    for i in range(100, 109):
        mod = rt / f"a{i}.py"
        assert mod.exists(), f"missing {mod}"
