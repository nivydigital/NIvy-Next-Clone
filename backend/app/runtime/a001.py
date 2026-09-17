from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Any

import httpx

from .engine import RunResult, runtime_engine


class A001ResearchError(RuntimeError):
    pass


REQUIRED_OUTPUT_FIELDS = {
    "status",
    "research_question",
    "scope",
    "findings",
    "evidence",
    "implications",
    "confidence",
    "researched_at",
}


def _firecrawl_enabled() -> bool:
    return bool(os.getenv("FIRECRAWL_API_KEY"))


def _browser_use_enabled() -> bool:
    return bool(os.getenv("BROWSER_USE_API_KEY"))


async def _firecrawl_search(request: dict[str, Any]) -> list[dict[str, Any]]:
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        return []
    base = os.getenv("FIRECRAWL_URL", "https://api.firecrawl.dev/v2").rstrip("/")
    query = " ".join(
        x
        for x in [
            request.get("research_question"),
            request.get("target_market"),
            request.get("geography"),
            request.get("industry"),
            request.get("customer_segment"),
            request.get("time_horizon"),
        ]
        if x
    )
    policy = request.get("source_policy") or {}
    payload: dict[str, Any] = {
        "query": query,
        "limit": int(policy.get("max_sources", 8)),
        "sources": ["web"],
        "scrapeOptions": {"formats": [{"type": "markdown"}]},
    }
    if policy.get("include_domains"):
        payload["includeDomains"] = policy["include_domains"]
    if policy.get("exclude_domains"):
        payload["excludeDomains"] = policy["exclude_domains"]
    if request.get("geography"):
        payload["location"] = request["geography"]
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            f"{base}/search",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
    results = ((data.get("data") or {}).get("web") or [])
    evidence = []
    for item in results:
        url = item.get("url") or ((item.get("metadata") or {}).get("url"))
        if not url:
            continue
        evidence.append(
            {
                "source_type": "firecrawl.search",
                "title": item.get("title") or ((item.get("metadata") or {}).get("title")) or url,
                "url": url,
                "description": item.get("description"),
                "content": item.get("markdown") or "",
                "provenance": {"provider": "Firecrawl", "search_id": data.get("id")},
            }
        )
    return evidence


async def _browser_use_research(request: dict[str, Any]) -> list[dict[str, Any]]:
    api_key = os.getenv("BROWSER_USE_API_KEY")
    if not api_key:
        return []
    base = os.getenv("BROWSER_USE_URL", "https://api.browser-use.com/api/v3").rstrip("/")
    task = (
        "Research the following market question using public sources only. "
        "Return concise factual findings with source title and URL for each material claim. "
        "Do not access private accounts, submit forms, purchase anything, or make external changes.\n\n"
        f"Question: {request.get('research_question')}\n"
        f"Target market: {request.get('target_market')}\n"
        f"Geography: {request.get('geography') or request.get('target_market')}\n"
        f"Industry: {request.get('industry') or 'not specified'}\n"
        f"Customer segment: {request.get('customer_segment') or 'not specified'}\n"
        f"Time horizon: {request.get('time_horizon') or 'current'}"
    )
    headers = {"X-Browser-Use-API-Key": api_key, "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(f"{base}/sessions", headers=headers, json={"task": task, "keepAlive": False})
        response.raise_for_status()
        session = response.json()
        session_id = session.get("id")
        if not session_id:
            raise A001ResearchError("Browser Use returned no session id")
        for _ in range(60):
            poll = await client.get(f"{base}/sessions/{session_id}", headers={"X-Browser-Use-API-Key": api_key})
            poll.raise_for_status()
            result = poll.json()
            status = str(result.get("status", "")).lower()
            if status in {"finished", "completed", "stopped", "failed"}:
                output = result.get("output")
                if isinstance(output, dict):
                    text = json.dumps(output, ensure_ascii=False)
                else:
                    text = str(output or result.get("lastStepSummary") or "")
                if status == "failed":
                    raise A001ResearchError("Browser Use research session failed")
                return [{"source_type": "browser_use.research", "title": "Browser Use research session", "url": "", "content": text, "provenance": {"provider": "Browser Use", "session_id": session_id}}]
            await asyncio.sleep(2)
    raise A001ResearchError("Browser Use research session timed out")


def _validate_output(output: dict[str, Any]) -> None:
    missing = REQUIRED_OUTPUT_FIELDS - set(output)
    if missing:
        raise A001ResearchError(f"A001 output missing required fields: {sorted(missing)}")
    if output.get("status") not in {"success", "partial", "failed", "escalated"}:
        raise A001ResearchError("A001 output has invalid status")
    if not isinstance(output.get("findings"), list) or not isinstance(output.get("evidence"), list) or not isinstance(output.get("implications"), list):
        raise A001ResearchError("A001 findings/evidence/implications must be arrays")
    if output.get("confidence") not in {"high", "medium", "low"}:
        raise A001ResearchError("A001 confidence must be high, medium, or low")
    datetime.fromisoformat(str(output["researched_at"]).replace("Z", "+00:00"))


async def run_a001_research(request: dict[str, Any]) -> RunResult:
    if not request.get("research_question") or not request.get("target_market"):
        raise A001ResearchError("A001 requires research_question and target_market")

    evidence: list[dict[str, Any]] = []
    errors: list[str] = []
    if _firecrawl_enabled():
        try:
            evidence.extend(await _firecrawl_search(request))
        except Exception as exc:
            errors.append(f"Firecrawl adapter failed: {exc}")
    if _browser_use_enabled():
        try:
            evidence.extend(await _browser_use_research(request))
        except Exception as exc:
            errors.append(f"Browser Use adapter failed: {exc}")

    if not evidence:
        supplied = request.get("evidence") or []
        if isinstance(supplied, list):
            evidence.extend(x for x in supplied if isinstance(x, dict))

    if not evidence:
        raise A001ResearchError(
            "No research evidence available. Configure FIRECRAWL_API_KEY and/or BROWSER_USE_API_KEY, or supply approved evidence."
        )

    context = dict(request)
    context["approved_research_evidence"] = evidence
    context["adapter_status"] = {"firecrawl": _firecrawl_enabled(), "browser_use": _browser_use_enabled()}
    context["adapter_errors"] = errors
    context["output_schema"] = {
        "required": sorted(REQUIRED_OUTPUT_FIELDS),
        "status_values": ["success", "partial", "failed", "escalated"],
        "confidence_values": ["high", "medium", "low"],
    }
    context["researched_at_now"] = datetime.now(timezone.utc).isoformat()
    llm = await runtime_engine.run_llm("A001", "Produce the A001 research report from the supplied evidence.", "PR001", context)
    if llm.status != "completed":
        return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try:
        output = json.loads(str(raw))
    except json.JSONDecodeError as exc:
        raise A001ResearchError("A001 model did not return valid JSON") from exc
    output.setdefault("researched_at", context["researched_at_now"])
    output.setdefault("warnings", [])
    output.setdefault("errors", errors)
    _validate_output(output)
    return RunResult(llm.run_id, "A001", "research.adapters+ollama", "completed", result=output)
