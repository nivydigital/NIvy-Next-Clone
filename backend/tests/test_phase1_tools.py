"""Phase 1 tool adapters — mock-mode contract tests (no live credentials required)."""
from __future__ import annotations

import asyncio
import os

os.environ["EMAIL_MOCK"] = "1"
os.environ["OLLAMA_MOCK"] = "1"
os.environ["WEB_FETCH_MOCK"] = "1"
os.environ["WEB_CRAWL_MOCK"] = "1"
os.environ["EMAIL_VERIFY_MOCK"] = "1"
os.environ["TOOLS_MOCK_ALL"] = "1"

from backend.app.runtime.tools import (
    canonicalize_tool_id,
    execute_tool,
    redact_args,
)
from backend.app.runtime.audit import audit_log
from backend.app.runtime.policy import PolicyDenied, decide


def test_ollama_generate_mock_json():
    result = asyncio.get_event_loop().run_until_complete(
        execute_tool(
            tool_id="tool.ollama.generate",
            arguments={"prompt": "hello", "format": "json"},
            actor="test",
        )
    )
    assert result["ok"] is True
    assert result["mock"] is True
    assert "response" in result


def test_ollama_requires_prompt():
    try:
        asyncio.get_event_loop().run_until_complete(
            execute_tool(tool_id="ollama.generate", arguments={"prompt": ""}, actor="test")
        )
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_email_send_mock_and_approval():
    try:
        asyncio.get_event_loop().run_until_complete(
            execute_tool(
                tool_id="tool.email.send",
                arguments={"to": "a@b.com", "subject": "hi", "body": "body"},
                actor="test",
                approved=False,
            )
        )
        assert False, "expected PolicyDenied"
    except PolicyDenied:
        pass
    result = asyncio.get_event_loop().run_until_complete(
        execute_tool(
            tool_id="email.send",
            arguments={"to": "a@b.com", "subject": "hi", "body": "body"},
            actor="test",
            approved=True,
        )
    )
    assert result["ok"] is True
    assert result["mock"] is True
    assert result["message_id"].startswith("mock-email-")


def test_web_fetch_mock():
    result = asyncio.get_event_loop().run_until_complete(
        execute_tool(
            tool_id="tool.web.fetch",
            arguments={"url": "https://example.com"},
            actor="test",
        )
    )
    assert result["ok"] is True
    assert result["mock"] is True
    assert "example.com" in result["body_text"]


def test_web_crawl_mock():
    result = asyncio.get_event_loop().run_until_complete(
        execute_tool(
            tool_id="tool.web.crawl",
            arguments={"seed_url": "https://example.com", "max_pages": 2},
            actor="test",
        )
    )
    assert result["ok"] is True
    assert len(result["pages"]) == 2


def test_email_verify_mock():
    ok = asyncio.get_event_loop().run_until_complete(
        execute_tool(
            tool_id="tool.email.verify",
            arguments={"email": "person@company.com"},
            actor="test",
        )
    )
    assert ok["is_reachable"] == "safe"
    bad = asyncio.get_event_loop().run_until_complete(
        execute_tool(
            tool_id="email.verify",
            arguments={"email": "x@invalid.test"},
            actor="test",
        )
    )
    assert bad["is_reachable"] == "invalid"


def test_redact_args():
    redacted = redact_args({"api_key": "secret-value", "to": "a@b.com", "nested": {"token": "xyz"}})
    assert redacted["api_key"] == "***REDACTED***"
    assert redacted["nested"]["token"] == "***REDACTED***"
    assert redacted["to"] == "a@b.com"


def test_canonicalize_and_policy():
    assert canonicalize_tool_id("ollama") == "tool.ollama.generate"
    assert decide(tool_id="tool.web.fetch").allowed is True
    assert decide(tool_id="tool.email.send", approved=False).allowed is False
    assert decide(tool_id="tool.email.send", approved=True).allowed is True


def test_audit_wrapper_records_events():
    before = len(audit_log.list())
    asyncio.get_event_loop().run_until_complete(
        execute_tool(
            tool_id="tool.ollama.generate",
            arguments={"prompt": "audit-me", "api_key": "should-redact"},
            actor="auditor",
            request_id="req-audit-1",
        )
    )
    events = audit_log.list()
    assert len(events) > before
    related = [e for e in events if e.get("request_id") == "req-audit-1"]
    assert any(e["event_type"] == "tool.authorized" for e in related)
    assert any(e["event_type"] == "tool.execution" and e["status"] == "completed" for e in related)
    auth = next(e for e in related if e["event_type"] == "tool.authorized")
    assert auth["data"]["args"].get("api_key") == "***REDACTED***"
