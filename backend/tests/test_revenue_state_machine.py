import pytest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_machine():
    return yaml.safe_load((ROOT / "runtime" / "revenue-state-machine.yaml").read_text(encoding="utf-8"))


def test_revenue_state_machine_has_required_states():
    machine = load_machine()
    assert set(machine["states"]) >= {"new", "qualified", "proposal", "won", "lost"}


def test_revenue_state_machine_rejects_undefined_transition():
    machine = load_machine()
    valid = {(x["from"], x["event"]) for x in machine["transitions"]}
    assert ("new", "send_proposal") not in valid


def test_protected_revenue_events_require_approval():
    machine = load_machine()
    assert machine["policy"]["protected_events_require_approval"] is True
    assert set(machine["policy"]["protected_events"]) >= {"proposal_approved", "deal_won"}


def test_revenue_agent_factory_requires_evaluation():
    factory = yaml.safe_load((ROOT / "runtime" / "revenue-agent-factory.yaml").read_text(encoding="utf-8"))
    assert factory["evaluation"]["evidence_required"] is True
    assert "evaluation_pass" in factory["lifecycle"]["activation_requires"]
    assert factory["safety"]["autonomous_mode_default"] is False
