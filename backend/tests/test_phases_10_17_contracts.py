from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

PHASES = {
    10: ("finance-monetization.yaml", {"A078", "A079", "A080", "A081", "A082", "A083"}),
    11: ("marketing-growth.yaml", {"A084", "A085", "A086", "A087", "A088", "A089", "A090", "A091"}),
    12: ("control-intelligence.yaml", {"A092", "A093", "A094", "A095", "A096", "A097"}),
    13: ("evaluation-qa-observability.yaml", {"A098", "A099", "A100", "A101", "A102", "A103"}),
    14: ("learning-continuous-improvement.yaml", {"A104", "A105", "A106", "A107", "A108", "A109"}),
    15: ("agent-collaboration.yaml", {"A110", "A111", "A112", "A113", "A114", "A115"}),
    16: ("agent-factory-marketplace.yaml", {"A116", "A117", "A118", "A119", "A120", "A121"}),
    17: ("scale-reliability-multicompany.yaml", {"A122", "A123", "A124", "A125", "A126", "A127"}),
}


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_all_phase_10_17_contracts_exist_and_are_canonical():
    for phase, (filename, expected_agents) in PHASES.items():
        data = load(ROOT / "runtime" / filename)
        assert data["status"] == "canonical"
        assert data["phase"] == phase
        assert set(data["agents"]) == expected_agents
        assert data["controls"]["default_deny"] is True
        assert data["controls"]["autonomous_mode"] is False
        assert data["evidence_required"] is True


def test_phase_15_collaboration_is_bounded_and_audited():
    data = load(ROOT / "runtime" / "agent-collaboration.yaml")
    assert data["protocol"]["loops"] == "bounded"
    assert data["protocol"]["timeout"] == "required"
    assert data["protocol"]["audit"] == "every_handoff"


def test_phase_14_promotion_requires_evidence_and_rollback():
    data = load(ROOT / "runtime" / "learning-continuous-improvement.yaml")
    assert "evaluation_pass" in data["promotion_requires"]
    assert "regression_pass" in data["promotion_requires"]
    assert data["rollback_required"] is True


def test_phase_17_requires_company_isolation():
    data = load(ROOT / "runtime" / "scale-reliability-multicompany.yaml")
    assert set(data["company_isolation"]) >= {"tenant_id_required", "data_scope_required", "policy_scope_required"}
