"""Deferred live A002 test.

Do not run during implementation. Execute later with the centralized all-agent
live test batch after runtime services and Ollama are configured.
"""

import os

import pytest

from app.runtime.a002 import run_a002_icp


@pytest.mark.asyncio
@pytest.mark.skipif(os.getenv("AIOS_LIVE_TESTS") != "1", reason="Live tests deferred to batch execution")
async def test_a002_live_with_approved_evidence():
    request = {
        "market_research": {
            "status": "success",
            "evidence": [
                {
                    "title": "Approved research source",
                    "url": "https://example.com/approved-source",
                    "provenance": {"provider": "approved-test-fixture"},
                    "content": "Test fixture evidence describing a target SMB market and observable demand signals.",
                }
            ],
        },
        "business_offer": {"service": "B2B growth and automation"},
        "geography": "United States",
    }
    result = await run_a002_icp(request)
    assert result.status == "completed"
    assert result.result["icp_definition"]["discovery_rules"]
