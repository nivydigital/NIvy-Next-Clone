import asyncio
import json
from datetime import datetime, timezone

import pytest

from app.runtime import a001
from app.runtime.engine import RunResult


GOOD_EVIDENCE = [{"title": "Authoritative source", "url": "https://example.com/source", "content": "Demand increased in the measured period."}]


def _good_output():
    return {
        "status": "success",
        "research_question": "What is demand?",
        "scope": {"target_market": "United States"},
        "findings": [{"claim": "Demand signal exists", "evidence_urls": ["https://example.com/source"]}],
        "evidence": GOOD_EVIDENCE,
        "implications": [{"text": "Validate before investment"}],
        "confidence": "medium",
        "researched_at": datetime.now(timezone.utc).isoformat(),
    }


def test_eval_missing_input_fails_closed():
    with pytest.raises(a001.A001ResearchError):
        asyncio.run(a001.run_a001_research({"target_market": "United States"}))


def test_eval_supplied_approved_evidence_path(monkeypatch):
    async def fake_run_llm(*args, **kwargs):
        return RunResult("eval-1", "A001", "ollama", "completed", result={"response": json.dumps(_good_output())})

    monkeypatch.setattr(a001.runtime_engine, "run_llm", fake_run_llm)
    result = asyncio.run(a001.run_a001_research({"research_question": "What is demand?", "target_market": "United States", "evidence": GOOD_EVIDENCE}))
    assert result.status == "completed"
    assert result.result["status"] == "success"


def test_eval_no_evidence_escalates(monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    monkeypatch.delenv("BROWSER_USE_API_KEY", raising=False)
    with pytest.raises(a001.A001ResearchError, match="No research evidence"):
        asyncio.run(a001.run_a001_research({"research_question": "What is demand?", "target_market": "United States"}))


def test_eval_malformed_model_output_rejected(monkeypatch):
    async def fake_run_llm(*args, **kwargs):
        return RunResult("eval-2", "A001", "ollama", "completed", result={"response": "not-json"})

    monkeypatch.setattr(a001.runtime_engine, "run_llm", fake_run_llm)
    with pytest.raises(a001.A001ResearchError, match="valid JSON"):
        asyncio.run(a001.run_a001_research({"research_question": "What is demand?", "target_market": "United States", "evidence": GOOD_EVIDENCE}))


def test_eval_schema_failure_rejected(monkeypatch):
    async def fake_run_llm(*args, **kwargs):
        return RunResult("eval-3", "A001", "ollama", "completed", result={"response": '{"status":"success"}'})

    monkeypatch.setattr(a001.runtime_engine, "run_llm", fake_run_llm)
    with pytest.raises(a001.A001ResearchError, match="missing required fields"):
        asyncio.run(a001.run_a001_research({"research_question": "What is demand?", "target_market": "United States", "evidence": GOOD_EVIDENCE}))
