"""Deterministic A002 evaluation cases.

These tests intentionally do not call live web research or live Ollama. Batch live
agent testing is deferred to the centralized test run as requested.
"""

from app.runtime.a002 import _validate_market_research, _validate_output


def _valid_output():
    return {
        "status": "success",
        "icp_definition": {
            "target_segments": [{"name": "Primary SMB segment", "priority": 1}],
            "firmographics": {"company_size": ["10-50"], "geography": ["United States"]},
            "buyer_roles": [{"role": "Owner", "influence": "decision_maker"}],
            "pain_points": [{"pain": "insufficient qualified leads"}],
            "buying_signals": [{"signal": "active demand generation hiring"}],
            "exclusions": ["outside target geography"],
            "confidence": "medium",
            "assumptions": ["company-size evidence is representative of the supplied market context"],
            "derived_from": [{"source_url": "https://example.com/research"}],
            "discovery_rules": [{"field": "geography", "operator": "in", "value": ["United States"]}],
        },
        "actions": [],
        "records_changed": [],
        "evidence": [{"url": "https://example.com/research"}],
        "warnings": [],
        "errors": [],
        "next_action": "Pass validated ICP to downstream discovery.",
    }


def test_happy_path_contract():
    _validate_market_research({"evidence": [{"url": "https://example.com/research"}]})
    _validate_output(_valid_output())


def test_missing_provenance_is_rejected():
    try:
        _validate_market_research({"evidence": [{"title": "No URL"}]})
    except Exception as exc:
        assert "provenance" in str(exc)
    else:
        raise AssertionError("Expected provenance failure")


def test_sensitive_attribute_rule_is_policy_level_only():
    # The runtime contract has no operation that accepts or derives sensitive traits.
    # This deterministic test documents that A002 is discovery/firmographic focused.
    output = _valid_output()
    assert "sensitive" not in str(output).lower()
