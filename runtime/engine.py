from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import httpx

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "runtime" / "agent-runtime-registry.json"


class RuntimeDenied(Exception):
    pass


@dataclass
class RunResult:
    run_id: str
    agent_id: str
    status: str
    output: Any = None
    approval_id: str | None = None
    error: str | None = None
    elapsed_ms: int = 0


class RuntimeEngine:
    """Small production-oriented execution boundary.

    It deliberately fails closed. Agents and tools must be declared in the runtime registry,
    protected tools require an approval token, and credentials are read only from environment.
    """

    def __init__(self) -> None:
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.approvals: dict[str, dict[str, Any]] = {}
        self.audit: list[dict[str, Any]] = []

    def _agent(self, agent_id: str) -> dict[str, Any]:
        for agent in self.registry["agents"]:
            if agent["id"] == agent_id:
                return agent
        raise RuntimeDenied(f"agent not declared: {agent_id}")

    def _tool(self, tool_id: str) -> dict[str, Any]:
        for tool in self.registry["tools"]:
            if tool["id"] == tool_id:
                return tool
        raise RuntimeDenied(f"tool not declared: {tool_id}")

    def request_approval(self, agent_id: str, tool_id: str, reason: str) -> dict[str, Any]:
        self._agent(agent_id)
        tool = self._tool(tool_id)
        approval_id = "apr_" + uuid.uuid4().hex
        item = {"id": approval_id, "agent_id": agent_id, "tool_id": tool_id,
                "reason": reason, "status": "pending", "created_at": time.time()}
        self.approvals[approval_id] = item
        self._audit("approval.requested", item)
        return item

    def approve(self, approval_id: str) -> dict[str, Any]:
        item = self.approvals.get(approval_id)
        if not item:
            raise RuntimeDenied("approval not found")
        item["status"] = "approved"
        item["approved_at"] = time.time()
        self._audit("approval.approved", item)
        return item

    def _check(self, agent_id: str, tool_id: str, approval_id: str | None) -> dict[str, Any]:
        agent = self._agent(agent_id)
        tool = self._tool(tool_id)
        if tool_id not in agent.get("tools", []):
            raise RuntimeDenied(f"tool {tool_id} is not bound to agent {agent_id}")
        if tool.get("protected", False):
            approval = self.approvals.get(approval_id or "")
            if not approval or approval["status"] != "approved" or approval["tool_id"] != tool_id:
                raise RuntimeDenied("protected side effect requires an approved approval_id")
        return tool

    async def execute(self, agent_id: str, tool_id: str, payload: dict[str, Any], approval_id: str | None = None) -> RunResult:
        started = time.time()
        run_id = "run_" + uuid.uuid4().hex
        try:
            tool = self._check(agent_id, tool_id, approval_id)
            output = await self._dispatch(tool, payload)
            result = RunResult(run_id, agent_id, "succeeded", output=output,
                               approval_id=approval_id, elapsed_ms=int((time.time()-started)*1000))
            self._audit("run.succeeded", {**asdict(result), "tool_id": tool_id})
            return result
        except Exception as exc:
            result = RunResult(run_id, agent_id, "failed", approval_id=approval_id,
                               error=str(exc), elapsed_ms=int((time.time()-started)*1000))
            self._audit("run.failed", {**asdict(result), "tool_id": tool_id})
            return result

    async def run_llm(self, agent_id: str, prompt: str) -> RunResult:
        started = time.time()
        run_id = "run_" + uuid.uuid4().hex
        try:
            agent = self._agent(agent_id)
            model = agent.get("model") or os.getenv("OLLAMA_MODEL", "llama3.2:3b")
            url = os.getenv("OLLAMA_URL", "http://ollama:11434") + "/api/generate"
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(url, json={"model": model, "prompt": prompt, "stream": False})
                r.raise_for_status()
                data = r.json()
            result = RunResult(run_id, agent_id, "succeeded", output=data.get("response", ""),
                               elapsed_ms=int((time.time()-started)*1000))
            self._audit("llm.succeeded", asdict(result))
            return result
        except Exception as exc:
            result = RunResult(run_id, agent_id, "failed", error=str(exc),
                               elapsed_ms=int((time.time()-started)*1000))
            self._audit("llm.failed", asdict(result))
            return result

    async def _dispatch(self, tool: dict[str, Any], payload: dict[str, Any]) -> Any:
        kind = tool["kind"]
        if kind == "n8n_webhook":
            base = os.getenv("N8N_URL", "http://n8n:5678")
            path = payload.pop("path", tool["path"])
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.post(base.rstrip("/") + path, json=payload)
                r.raise_for_status()
                return r.json() if "application/json" in r.headers.get("content-type", "") else r.text
        if kind == "odoo_jsonrpc":
            url = os.getenv("ODOO_URL")
            db = os.getenv("ODOO_DB")
            user = os.getenv("ODOO_USER")
            password = os.getenv("ODOO_PASSWORD")
            if not all([url, db, user, password]):
                raise RuntimeDenied("Odoo credentials are not configured")
            async with httpx.AsyncClient(timeout=60) as client:
                auth = await client.post(url.rstrip("/") + "/jsonrpc", json={"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[db,user,password,{}]},"id":1})
                uid = auth.json().get("result")
                if not uid:
                    raise RuntimeDenied("Odoo authentication failed")
                args = payload.get("args", [])
                kwargs = payload.get("kwargs", {})
                call = await client.post(url.rstrip("/") + "/jsonrpc", json={"jsonrpc":"2.0","method":"call","params":{"service":"object","method":"execute_kw","args":[db,uid,password,payload["model"],payload["method"],args,kwargs]},"id":2})
                call.raise_for_status()
                data = call.json()
                if data.get("error"):
                    raise RuntimeDenied(str(data["error"]))
                return data.get("result")
        if kind == "email_webhook":
            base = os.getenv("N8N_URL", "http://n8n:5678")
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.post(base.rstrip("/") + os.getenv("N8N_EMAIL_WEBHOOK", "/webhook/nivy/send-email"), json=payload)
                r.raise_for_status()
                return r.json()
        raise RuntimeDenied(f"unsupported tool kind: {kind}")

    def _audit(self, event: str, data: dict[str, Any]) -> None:
        self.audit.append({"event": event, "timestamp": time.time(), "data": data})

    def health(self) -> dict[str, Any]:
        return {"agents": len(self.registry["agents"]), "tools": len(self.registry["tools"]),
                "approvals": len(self.approvals), "audit_events": len(self.audit)}


runtime_engine = RuntimeEngine()
