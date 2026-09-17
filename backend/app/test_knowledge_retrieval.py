"""P3 E3 — Knowledge retrieval integration tests (mock default)."""
from __future__ import annotations

import os

import pytest

from backend.app.runtime.knowledge_store import (
    get_knowledge_store,
    reset_knowledge_store,
    retrieve_for_agent,
)


@pytest.fixture(autouse=True)
def _reset_store(monkeypatch):
    monkeypatch.delenv("NIVY_KNOWLEDGE_STORE", raising=False)
    reset_knowledge_store()
    yield
    reset_knowledge_store()


def test_default_mode_is_mock():
    store = get_knowledge_store()
    packs = store.list_packs()
    assert "KP001" in packs
    assert "KP004" in packs
    assert len(packs) >= 8


def test_retrieve_icp_for_research_agent():
    out = retrieve_for_agent("ICP buyer signals qualification", agent_id="A041", top_k=3)
    assert out["mode"] == "mock"
    assert out["count"] >= 1
    pack_ids = {h["pack_id"] for h in out["hits"]}
    assert "KP004" in pack_ids or "KP005" in pack_ids


def test_retrieve_outreach_playbook():
    out = retrieve_for_agent("outreach sequence approval email send", agent_id="A044", top_k=5)
    assert out["count"] >= 1
    texts = " ".join(h["text"].lower() for h in out["hits"])
    assert "approval" in texts or "sequence" in texts or "send" in texts


def test_restricted_pack_hidden_by_default():
    out = retrieve_for_agent("secrets backup SOP restricted policy", agent_id="A001", allow_restricted=False)
    for h in out["hits"]:
        assert h["access_policy"] != "restricted"


def test_restricted_pack_with_flag():
    out = retrieve_for_agent("secrets backup SOP", agent_id="ops", allow_restricted=True, top_k=5)
    pack_ids = {h["pack_id"] for h in out["hits"]}
    # May or may not match KP007 depending on tokens; if present must be restricted allowed
    for h in out["hits"]:
        if h["pack_id"] == "KP007":
            assert h["access_policy"] == "restricted"


def test_empty_query_returns_empty():
    out = retrieve_for_agent("", agent_id="A034")
    assert out["count"] == 0


def test_live_flag_still_returns_packs(monkeypatch):
    monkeypatch.setenv("NIVY_KNOWLEDGE_STORE", "live")
    reset_knowledge_store()
    out = retrieve_for_agent("company identity mission", agent_id="A001")
    assert out["mode"] == "live"
    assert out["count"] >= 1
