from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(name):
    return yaml.safe_load((ROOT / "runtime" / name).read_text(encoding="utf-8"))


def test_phase_8_has_seeded_agents_and_governance():
    contract = load_yaml("communications-intelligence.yaml")
    assert set(contract["seed_agents"]) == {"A066", "A067", "A068", "A069", "A070", "A071"}
    assert contract["tool_policy"]["default_deny"] is True
    assert contract["tool_policy"]["autonomous_mode_default"] is False
    assert contract["safety"]["external_message_send_requires_approval"] is True


def test_phase_9_has_customer_lifecycle_and_seeded_agents():
    contract = load_yaml("customer-success-retention.yaml")
    assert set(contract["seed_agents"]) == {"A072", "A073", "A074", "A075", "A076", "A077"}
    assert set(contract["customer_lifecycle"]["states"]) >= {"onboarding", "active", "at_risk", "renewal_due", "renewed", "churned"}
    assert contract["tool_policy"]["default_deny"] is True
    assert contract["safety"]["outbound_communication_requires_approval"] is True


def test_phase_8_9_use_canonical_platform_boundaries():
    p8 = load_yaml("communications-intelligence.yaml")
    p9 = load_yaml("customer-success-retention.yaml")
    for contract in (p8, p9):
        assert contract["integrations"]["workflow_engine"] == "n8n"
        assert contract["integrations"]["crm_system_of_record"] == "Odoo"
        assert contract["integrations"]["vector_store"] == "Qdrant"


def test_phase_8_9_agents_are_approval_gated_by_default():
    registry = yaml.safe_load((ROOT / "agents" / "registry.yaml").read_text(encoding="utf-8"))
    ids = {agent["id"] for agent in registry["agents"]}
    assert {f"A{i:03d}" for i in range(66, 78)} <= ids
    for agent in registry["agents"]:
        if agent["id"] in {f"A{i:03d}" for i in range(66, 78)}:
            assert "tool.ollama.generate" in agent["tools"]
            assert agent["permissions"]["side_effects"] is False
