from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_a001_spec_is_complete_for_required_contract_layers():
    spec = yaml.safe_load((ROOT / "agents/A001/agent.yaml").read_text(encoding="utf-8"))
    for key in [
        "id", "name", "objective", "scope", "non_goals", "capabilities", "knowledge",
        "memory", "model", "inputs", "outputs", "permissions", "workflow", "guardrails",
        "verification", "evaluation", "observability", "runtime", "provenance",
    ]:
        assert key in spec, key
    assert spec["id"] == "A001"
    assert spec["inputs"]["required"] == ["research_question", "target_market"]
    assert spec["workflow"]["state_machine"] == "runtime/a001-market-research.yaml"
    assert spec["permissions"]["side_effects"] is False


def test_a001_reuses_canonical_binding_and_registered_prompt():
    bindings = yaml.safe_load((ROOT / "knowledge/agent-bindings/AGENT-SKILL-BINDINGS.yaml").read_text(encoding="utf-8"))
    binding = next(item for item in bindings["bindings"] if item["agent"] == "A001")
    assert binding["skills"] == ["SK001"]
    assert binding["prompts"] == ["PR001"]
    assert "tool.ollama.generate" in binding["tools"]

    prompts = yaml.safe_load((ROOT / "prompts/executable.yaml").read_text(encoding="utf-8"))
    assert prompts["prompts"]["PR001"]["body"]
    assert "without fabricating evidence" in prompts["prompts"]["PR001"]["body"]


def test_a001_input_and_output_contracts_exist_and_are_closed():
    input_schema = yaml.safe_load((ROOT / "agents/A001/input.schema.json").read_text(encoding="utf-8"))
    output_schema = yaml.safe_load((ROOT / "agents/A001/output.schema.json").read_text(encoding="utf-8"))
    assert input_schema["additionalProperties"] is False
    assert set(input_schema["required"]) == {"research_question", "target_market"}
    assert output_schema["additionalProperties"] is False
    assert {"research_question", "scope", "findings", "evidence", "implications", "confidence", "researched_at"}.issubset(
        set(output_schema["required"])
    )


def test_a001_runtime_contract_is_fail_closed_and_side_effect_free():
    contract = yaml.safe_load((ROOT / "runtime/a001-market-research.yaml").read_text(encoding="utf-8"))
    assert contract["execution"]["side_effects"] is False
    assert contract["failure"]["undeclared_tool"] == "deny"
    assert contract["failure"]["unauthorized_source_access"] == "deny"
    assert contract["verification"]["postconditions"]


def test_a001_never_claims_web_research_without_evidence():
    contract = yaml.safe_load((ROOT / "runtime/a001-market-research.yaml").read_text(encoding="utf-8"))
    assert "Every material claim must be traceable" in contract["research_boundary"]["rule"]
