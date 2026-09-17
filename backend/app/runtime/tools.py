from __future__ import annotations

import json
import os
import re
from typing import Any
from uuid import uuid4

import httpx

from .audit import audit_log
from .policy import enforce

_ALIAS_TO_CANONICAL = {
    "ollama.generate": "tool.ollama.generate",
    "ollama": "tool.ollama.generate",
    "tool.ollama.generate": "tool.ollama.generate",
    "email.send": "tool.email.send",
    "email": "tool.email.send",
    "tool.email.send": "tool.email.send",
    "web.fetch": "tool.web.fetch",
    "browser.fetch": "tool.web.fetch",
    "tool.web.fetch": "tool.web.fetch",
    "web.crawl": "tool.web.crawl",
    "tool.web.crawl": "tool.web.crawl",
    "email.verify": "tool.email.verify",
    "reacher.verify": "tool.email.verify",
    "verification.email": "tool.email.verify",
    "tool.email.verify": "tool.email.verify",
    "audit.write": "tool.audit.write",
    "tool.audit.write": "tool.audit.write",
    "lead.create": "tool.lead.create",
    "tool.lead.create": "tool.lead.create",
    "lead.read": "tool.lead.read",
    "tool.lead.read": "tool.lead.read",
    "lead.qualify": "tool.lead.qualify",
    "tool.lead.qualify": "tool.lead.qualify",
    "odoo.write": "tool.odoo.write",
    "tool.odoo.write": "tool.odoo.write",
    "crm.update": "tool.crm.update",
    "tool.crm.update": "tool.crm.update",
    "proposal.send": "tool.proposal.send",
    "tool.proposal.send": "tool.proposal.send",
}

_REDACT_KEYS = re.compile(
    r"(password|secret|token|api[_-]?key|authorization|bearer)",
    re.IGNORECASE,
)


def canonicalize_tool_id(tool_id: str) -> str:
    return _ALIAS_TO_CANONICAL.get(tool_id, tool_id)


def redact_args(arguments: dict[str, Any] | None) -> dict[str, Any]:
    if not arguments:
        return {}
    out: dict[str, Any] = {}
    for key, value in arguments.items():
        if _REDACT_KEYS.search(str(key)):
            out[key] = "***REDACTED***"
        elif isinstance(value, dict):
            out[key] = redact_args(value)
        elif isinstance(value, list):
            out[key] = [
                redact_args(v) if isinstance(v, dict) else v
                for v in value
            ]
        else:
            out[key] = value
    return out


def _env_truthy(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on", "mock"}


def _mock_mode(tool_env: str | None = None) -> bool:
    if _env_truthy("TOOLS_MOCK_ALL"):
        return True
    if tool_env and _env_truthy(tool_env):
        return True
    return False


async def _ollama_generate(arguments: dict[str, Any]) -> dict[str, Any]:
    prompt = str(arguments.get("prompt") or "").strip()
    if not prompt:
        raise ValueError("tool.ollama.generate requires non-empty prompt")
    if _mock_mode("OLLAMA_MOCK"):
        fmt = str(arguments.get("format") or "text")
        if fmt == "json":
            body = json.dumps({"mock": True, "summary": "ollama mock response", "prompt_len": len(prompt)})
        else:
            body = f"[mock-ollama] echo: {prompt[:200]}"
        return {
            "ok": True,
            "tool": "tool.ollama.generate",
            "response": body,
            "model": arguments.get("model") or os.getenv("OLLAMA_MODEL", "mock"),
            "mock": True,
        }
    base = (os.getenv("OLLAMA_URL") or os.getenv("OLLAMA_BASE_URL") or "http://ollama:11434").rstrip("/")
    model = str(arguments.get("model") or os.getenv("OLLAMA_MODEL", "llama3.2:3b"))
    timeout = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))
    payload: dict[str, Any] = {"model": model, "prompt": prompt, "stream": False}
    if arguments.get("system"):
        payload["system"] = str(arguments["system"])
    if arguments.get("format") == "json":
        payload["format"] = "json"
    if arguments.get("temperature") is not None:
        payload["options"] = {"temperature": float(arguments["temperature"])}
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(f"{base}/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
    return {
        "ok": True,
        "tool": "tool.ollama.generate",
        "response": data.get("response", ""),
        "model": data.get("model", model),
        "raw": data,
        "mock": False,
    }


async def _email_send(arguments: dict[str, Any]) -> dict[str, Any]:
    to = str(arguments.get("to") or "").strip()
    subject = str(arguments.get("subject") or "").strip()
    body = str(arguments.get("body") or "").strip()
    if not to or not subject or not body:
        raise ValueError("tool.email.send requires to, subject, and body")
    use_mock = _mock_mode("EMAIL_MOCK") or (not os.getenv("N8N_URL") and not os.getenv("FORCE_LIVE_EMAIL"))
    if os.getenv("FORCE_LIVE_EMAIL") == "1":
        use_mock = False
    if use_mock:
        return {
            "ok": True,
            "tool": "tool.email.send",
            "message_id": f"mock-email-{uuid4().hex[:12]}",
            "to": to,
            "subject": subject,
            "mock": True,
        }
    n8n = os.getenv("N8N_URL", "http://n8n:5678").rstrip("/")
    webhook = os.getenv("N8N_EMAIL_WEBHOOK", "/webhook/nivy/send-email")
    timeout = float(os.getenv("EMAIL_TIMEOUT_SECONDS", "30"))
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(n8n + webhook, json=arguments)
        response.raise_for_status()
        return {"ok": True, "tool": "tool.email.send", "result": response.json(), "mock": False}


async def _web_fetch(arguments: dict[str, Any]) -> dict[str, Any]:
    url = str(arguments.get("url") or "").strip()
    if not url.startswith(("http://", "https://")):
        raise ValueError("tool.web.fetch requires http(s) url")
    if _mock_mode("WEB_FETCH_MOCK") or not os.getenv("ALLOW_LIVE_WEB_FETCH"):
        return {
            "ok": True,
            "tool": "tool.web.fetch",
            "status_code": 200,
            "content_type": "text/plain",
            "body_text": f"[mock-fetch] content for {url}",
            "url": url,
            "mock": True,
        }
    method = str(arguments.get("method") or "GET").upper()
    if method not in {"GET", "HEAD"}:
        raise ValueError("tool.web.fetch only allows GET or HEAD")
    max_bytes = int(arguments.get("max_bytes") or 500_000)
    timeout = float(os.getenv("WEB_FETCH_TIMEOUT_SECONDS", "30"))
    headers = arguments.get("headers") if isinstance(arguments.get("headers"), dict) else {}
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        response = await client.request(method, url, headers=headers)
        text = response.text[:max_bytes]
    return {
        "ok": True,
        "tool": "tool.web.fetch",
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "body_text": text,
        "url": str(response.url),
        "mock": False,
    }


async def _web_crawl(arguments: dict[str, Any]) -> dict[str, Any]:
    seed = str(arguments.get("seed_url") or "").strip()
    if not seed.startswith(("http://", "https://")):
        raise ValueError("tool.web.crawl requires http(s) seed_url")
    max_pages = min(int(arguments.get("max_pages") or 3), 10)
    if _mock_mode("WEB_CRAWL_MOCK") or not os.getenv("ALLOW_LIVE_WEB_CRAWL"):
        pages = [{"url": seed, "title": "Mock seed page", "excerpt": f"[mock-crawl] page 1 of {seed}"}]
        for i in range(2, max_pages + 1):
            pages.append({"url": f"{seed.rstrip('/')}/page-{i}", "title": f"Mock page {i}", "excerpt": f"[mock-crawl] page {i}"})
        return {"ok": True, "tool": "tool.web.crawl", "pages": pages, "mock": True}
    fetched = await _web_fetch({"url": seed, "method": "GET"})
    pages = [{"url": seed, "title": "", "excerpt": str(fetched.get("body_text", ""))[:500]}]
    return {"ok": True, "tool": "tool.web.crawl", "pages": pages[:max_pages], "mock": False}


async def _email_verify(arguments: dict[str, Any]) -> dict[str, Any]:
    email = str(arguments.get("email") or "").strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("tool.email.verify requires a plausible email")
    if _mock_mode("EMAIL_VERIFY_MOCK") or not os.getenv("REACHER_BASE_URL"):
        is_reachable = "invalid" if email.endswith("@invalid.test") else "safe"
        return {"ok": True, "tool": "tool.email.verify", "email": email, "is_reachable": is_reachable, "mock": True}
    base = os.getenv("REACHER_BASE_URL", "").rstrip("/")
    timeout = float(os.getenv("EMAIL_VERIFY_TIMEOUT_SECONDS", "30"))
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(f"{base}/v0/check_email", json={"to_email": email})
        response.raise_for_status()
        data = response.json()
    return {
        "ok": True,
        "tool": "tool.email.verify",
        "email": email,
        "is_reachable": data.get("is_reachable", data.get("result", "unknown")),
        "raw": data,
        "mock": False,
    }


async def _odoo_write(arguments: dict[str, Any]) -> dict[str, Any]:
    base = os.getenv("ODOO_URL", "").rstrip("/")
    if not base:
        raise RuntimeError("ODOO_URL is not configured")
    timeout = float(os.getenv("ODOO_TIMEOUT_SECONDS", "30"))
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(base + "/api/aios/write", json=arguments)
        response.raise_for_status()
        return {"ok": True, "tool": "tool.odoo.write", "result": response.json(), "mock": False}


async def execute_tool(
    *,
    tool_id: str,
    arguments: dict[str, Any],
    actor: str,
    approved: bool = False,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Authorize, execute, and audit a tool call. Arguments are redacted in logs."""
    canonical = canonicalize_tool_id(tool_id)
    run_id = request_id or str(uuid4())
    redacted = redact_args(arguments if isinstance(arguments, dict) else {})
    decision = enforce(tool_id=canonical, approved=approved)
    audit_log.record(
        event_type="tool.authorized",
        actor=actor,
        action=canonical,
        status="allowed",
        request_id=run_id,
        data={"approval": decision.reason, "args": redacted},
    )
    try:
        if canonical == "tool.ollama.generate":
            result = await _ollama_generate(arguments)
        elif canonical == "tool.email.send":
            result = await _email_send(arguments)
        elif canonical == "tool.web.fetch":
            result = await _web_fetch(arguments)
        elif canonical == "tool.web.crawl":
            result = await _web_crawl(arguments)
        elif canonical == "tool.email.verify":
            result = await _email_verify(arguments)
        elif canonical == "tool.audit.write":
            result = audit_log.record(
                event_type=str(arguments.get("event_type", "tool.audit")),
                actor=actor,
                action="tool.audit.write",
                status="ok",
                request_id=run_id,
                data=redact_args(arguments.get("data") if isinstance(arguments.get("data"), dict) else arguments),
            )
            result = {"ok": True, "tool": canonical, "result": result}
        elif canonical in {"tool.lead.create", "tool.lead.read", "tool.lead.qualify"}:
            result = {"ok": True, "tool": canonical, "result": arguments, "mock": True}
        elif canonical == "tool.odoo.write":
            result = await _odoo_write(arguments)
        elif canonical in {"tool.crm.update", "tool.proposal.send"}:
            raise RuntimeError(f"{canonical} requires an installed adapter")
        else:
            raise RuntimeError(f"unsupported tool: {tool_id} (canonical={canonical})")
        audit_log.record(
            event_type="tool.execution",
            actor=actor,
            action=canonical,
            status="completed",
            request_id=run_id,
            data={"ok": True, "mock": bool(result.get("mock")) if isinstance(result, dict) else False},
        )
        return result
    except Exception as exc:
        audit_log.record(
            event_type="tool.execution",
            actor=actor,
            action=canonical,
            status="error",
            request_id=run_id,
            data={"error": str(exc), "args": redacted},
        )
        raise
