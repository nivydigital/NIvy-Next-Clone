from __future__ import annotations

import os
from typing import Any
import httpx

from .audit import audit_log
from .policy import enforce


async def execute_tool(*, tool_id: str, arguments: dict[str, Any], actor: str, approved: bool = False, request_id: str | None = None) -> dict[str, Any]:
    decision = enforce(tool_id=tool_id, approved=approved)
    audit_log.record(event_type="tool.authorized", actor=actor, action=tool_id, status="allowed", request_id=request_id, data={"approval": decision.reason})
    try:
        if tool_id == "lead.create":
            return {"ok": True, "tool": tool_id, "result": arguments}
        if tool_id == "lead.read":
            return {"ok": True, "tool": tool_id, "result": arguments}
        if tool_id == "lead.qualify":
            return {"ok": True, "tool": tool_id, "result": arguments}
        if tool_id == "audit.write":
            return audit_log.record(event_type="tool.audit", actor=actor, action="audit.write", status="ok", request_id=request_id, data=arguments)
        if tool_id == "ollama.generate":
            url = os.getenv("OLLAMA_URL", "http://ollama:11434") + "/api/generate"
            payload = {"model": os.getenv("OLLAMA_MODEL", "llama3.2:3b"), "prompt": str(arguments.get("prompt", "")), "stream": False}
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return {"ok": True, "tool": tool_id, "result": response.json()}
        if tool_id == "email.send":
            # Actual delivery is delegated to the configured n8n webhook.
            n8n = os.getenv("N8N_URL", "http://n8n:5678")
            webhook = os.getenv("N8N_EMAIL_WEBHOOK", "/webhook/nivy/send-email")
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(n8n + webhook, json=arguments)
                response.raise_for_status()
                return {"ok": True, "tool": tool_id, "result": response.json()}
        if tool_id == "odoo.write":
            base = os.getenv("ODOO_URL", "").rstrip("/")
            if not base:
                raise RuntimeError("ODOO_URL is not configured")
            # Odoo adapter endpoint is intentionally explicit; credentials remain environment-backed.
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(base + "/api/aios/write", json=arguments)
                response.raise_for_status()
                return {"ok": True, "tool": tool_id, "result": response.json()}
        if tool_id in {"crm.update", "proposal.send"}:
            raise RuntimeError(f"{tool_id} requires an installed adapter")
        raise RuntimeError(f"unsupported tool: {tool_id}")
    except Exception as exc:
        audit_log.record(event_type="tool.execution", actor=actor, action=tool_id, status="error", request_id=request_id, data={"error": str(exc)})
        raise
