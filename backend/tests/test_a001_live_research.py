import asyncio
from datetime import datetime, timezone

import pytest

from app.runtime import a001


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def post(self, url, **kwargs):
        assert url.endswith("/search")
        assert kwargs["json"]["query"]
        return FakeResponse({"success": True, "id": "search-1", "data": {"web": [{"title": "Example source", "url": "https://example.com/source", "markdown": "Verified market evidence"}]}})


def test_firecrawl_adapter_normalizes_provenance(monkeypatch):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    monkeypatch.setattr(a001.httpx, "AsyncClient", FakeClient)
    evidence = asyncio.run(a001._firecrawl_search({"research_question": "demand", "target_market": "US"}))
    assert len(evidence) == 1
    assert evidence[0]["url"] == "https://example.com/source"
    assert evidence[0]["provenance"]["provider"] == "Firecrawl"


def test_a001_output_validation_accepts_contract_shape():
    payload = {
        "status": "success",
        "research_question": "demand",
        "scope": {"target_market": "US"},
        "findings": [{"claim": "Example", "evidence_urls": ["https://example.com/source"]}],
        "evidence": [{"title": "Example source", "url": "https://example.com/source"}],
        "implications": [{"text": "Validate before action"}],
        "confidence": "medium",
        "researched_at": datetime.now(timezone.utc).isoformat(),
    }
    a001._validate_output(payload)


def test_a001_output_validation_rejects_missing_provenance_fields():
    payload = {
        "status": "success",
        "research_question": "demand",
        "scope": {},
        "findings": [],
        "evidence": [],
        "implications": [],
        "confidence": "medium",
    }
    with pytest.raises(a001.A001ResearchError):
        a001._validate_output(payload)
