import pytest

from app.runtime.a002 import A002ICPError, _validate_market_research, _validate_output


def test_a002_rejects_missing_evidence():
    with pytest.raises(A002ICPError):
        _validate_market_research({"status": "success"})


def test_a002_rejects_evidence_without_provenance():
    with pytest.raises(A002ICPError):
        _validate_market_research({"evidence": [{"title": "Unattributed source"}]})


def test_a002_accepts_provenance_and_valid_shape():
    evidence = _validate_market_research({"evidence": [{"title": "Source", "url": "https://example.com"}]})
    assert len(evidence) == 1


def test_a002_output_contract():
    output = {
        "status": "success",
        "icp_definition": {
            "target_segments": [{"name": "US SMB HVAC"}],
            "firmographics": {"geography": ["United States"]},
            "buyer_roles": [{"role": "Owner"}],
            "pain_points": [{"pain": "Lead acquisition"}],
            "buying_signals": [{"signal": "Hiring sales staff"}],
            "exclusions": ["Unsupported geography"],
            "confidence": "medium",
            "assumptions": [],
            "derived_from": [{"url": "https://example.com"}],
            "discovery_rules": [{"field": "industry", "operator": "equals", "value": "HVAC"}],
        },
        "evidence": [{"url": "https://example.com"}],
        "warnings": [],
        "errors": [],
        "next_action": "downstream discovery",
    }
    _validate_output(output)


def test_a002_rejects_invalid_confidence():
    output = {
        "status": "success",
        "icp_definition": {
            "target_segments": [], "firmographics": {}, "buyer_roles": [],
            "pain_points": [], "buying_signals": [], "exclusions": [],
            "confidence": "certain", "assumptions": [], "derived_from": [],
            "discovery_rules": [],
        },
        "evidence": [], "warnings": [], "errors": [], "next_action": "review",
    }
    with pytest.raises(A002ICPError):
        _validate_output(output)
