from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from .audit import audit_log
from .policy import PolicyDenied, decide
from .prompt_loader import PromptLoadError, resolve_prompt

ROOT = Path(__file__).resolve().parents[3]

@dataclass
class RunResult:
    run_id: str
    agent_id: str
    tool_id: str | None
    status: str
    result: Any = None
    error: str | None = None

class RuntimeEngine:
    def __init__(self) -> None:
        self.approvals: dict[str, dict[str, Any]] = {}
        self.audit: list[dict[str, Any]] = []
        self.registry = self._load_registry()
        self.prompt_library = self._load_prompt_library()

    def _load_registry(self) -> dict[str, Any]:
        path = ROOT / "agents" / "registry.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
        data = data or {}
        if isinstance(data, list): data = {"agents": data}
        ext = ROOT / "agents" / "implementation-registry.yaml"
        if ext.exists():
            extra = yaml.safe_load(ext.read_text(encoding="utf-8")) or {}
            data.setdefault("agents", [])
            data["agents"].extend(extra.get("agents", []))
        data.setdefault("agents", [])
        data.setdefault("policy", {"default_deny": True})
        data.setdefault("tools", [])
        return data

    def _load_prompt_library(self) -> dict[str, Any]:
        path = ROOT / "prompts" / "executable.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
        data = data or {}
        data.setdefault("common", {})
        data.setdefault("prompts", {})
        return data

    def _agent(self, agent_id: str) -> dict[str, Any]:
        for agent in self.registry.get("agents", []):
            if isinstance(agent, dict) and agent.get("id") == agent_id: return agent
        raise PolicyDenied(f"undeclared agent: {agent_id}")

    def _bound_tools(self, agent: dict[str, Any]) -> list[str]:
        return [x.get("id") if isinstance(x, dict) else str(x) for x in (agent.get("tools", []) or [])]

    def _bound_prompts(self, agent: dict[str, Any]) -> list[str]:
        return [x.get("id") if isinstance(x, dict) else str(x) for x in (agent.get("prompts", []) or [])]

    def build_prompt(self, agent_id: str, prompt_id: str | None, context: dict[str, Any] | None, raw_prompt: str | None) -> str:
        agent = self._agent(agent_id)
        selected = prompt_id or ((self._bound_prompts(agent) or [None])[0])
        if selected:
            if selected not in self._bound_prompts(agent): raise PolicyDenied(f"prompt {selected} is not bound to agent {agent_id}")
            try:
                resolved = resolve_prompt(selected, require_body=True)
            except PromptLoadError as exc:
                raise PolicyDenied(str(exc)) from exc
            variable_text = json.dumps(context or {}, ensure_ascii=False, default=str)
            common = resolved.get("common") or self.prompt_library.get("common", {})
            body = resolved.get("body") or ""
            return f"{common.get('system','')}\n\nAGENT: {agent.get('name')} ({agent_id})\nPROMPT_ID: {selected}\nTASK CONTEXT:\n{variable_text}\n\nTASK INSTRUCTIONS:\n{body}\n\n{common.get('output','')}"
        if raw_prompt: return str(raw_prompt)
        raise PolicyDenied(f"agent {agent_id} has no executable prompt")

    def health(self) -> dict[str, Any]:
        policy = self.registry.get("policy", {})
        return {"status":"ok","agents":len(self.registry.get("agents", [])),"executable_prompts":len(self.prompt_library.get("prompts", {})),"approvals":len(self.approvals),"audit_events":len(self.audit),"default_deny":policy.get("default_deny", True) is True,"autonomous_mode":policy.get("autonomous_mode", False) is True}

    def _record(self, **kwargs: Any) -> None: self.audit.append(audit_log.record(**kwargs))

    async def run_llm(self, agent_id: str, prompt: str, prompt_id: str | None = None, context: dict[str, Any] | None = None) -> RunResult:
        run_id = str(uuid4())
        try:
            self._agent(agent_id)
            effective_prompt = self.build_prompt(agent_id, prompt_id, context, prompt)
            self._record(event_type="agent.run", actor="runtime", action=agent_id, status="started", request_id=run_id, data={"prompt_id": prompt_id})
            import httpx
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(os.getenv("OLLAMA_URL", "http://ollama:11434") + "/api/generate", json={"model":os.getenv("OLLAMA_MODEL","llama3.2:3b"),"prompt":effective_prompt,"stream":False})
                response.raise_for_status(); result=response.json()
            self._record(event_type="agent.run", actor="runtime", action=agent_id, status="completed", request_id=run_id, data={"prompt_id":prompt_id})
            return RunResult(run_id,agent_id,"ollama","completed",result=result)
        except Exception as exc:
            self._record(event_type="agent.run", actor="runtime", action=agent_id, status="failed", request_id=run_id, data={"error":str(exc),"prompt_id":prompt_id})
            return RunResult(run_id,agent_id,"ollama","failed",error=str(exc))

    def request_approval(self, agent_id: str, tool_id: str, reason: str) -> dict[str, Any]:
        agent=self._agent(agent_id)
        if tool_id not in self._bound_tools(agent): raise PolicyDenied(f"tool {tool_id} is not bound to agent {agent_id}")
        if not decide(tool_id=tool_id).requires_approval: raise PolicyDenied("approval is only available for protected side effects")
        approval_id=str(uuid4()); item={"approval_id":approval_id,"agent_id":agent_id,"tool_id":tool_id,"reason":reason,"status":"pending"}; self.approvals[approval_id]=item
        self._record(event_type="approval.requested",actor=agent_id,action=tool_id,status="pending",request_id=approval_id,data=item); return item

    def approve(self, approval_id: str) -> dict[str, Any]:
        item=self.approvals.get(approval_id)
        if not item: raise PolicyDenied("approval not found")
        if item.get("status")!="pending": raise PolicyDenied(f"approval is not pending: {item.get('status')}")
        item["status"]="approved"; self._record(event_type="approval.decided",actor="human",action=item["tool_id"],status="approved",request_id=approval_id,data=item); return item

    async def execute(self, agent_id: str, tool_id: str, payload: dict[str, Any], approval_id: str | None) -> RunResult:
        run_id=str(uuid4())
        try:
            agent=self._agent(agent_id)
            if tool_id not in self._bound_tools(agent): raise PolicyDenied(f"tool {tool_id} is not bound to agent {agent_id}")
            approval=self.approvals.get(approval_id) if approval_id else None
            approved=bool(approval and approval.get("status")=="approved" and approval.get("agent_id")==agent_id and approval.get("tool_id")==tool_id)
            if not decide(tool_id=tool_id,approved=approved).allowed: raise PolicyDenied("protected side effect requires a valid approval")
            if tool_id in {"tool.ollama.generate","ollama"}: return await self.run_llm(agent_id,str(payload.get("prompt",payload)),payload.get("prompt_id"),payload.get("context"))
            if tool_id in {"tool.email.send","email"}:
                import httpx
                async with httpx.AsyncClient(timeout=30) as client:
                    response=await client.post(os.getenv("N8N_URL","http://n8n:5678")+os.getenv("N8N_EMAIL_WEBHOOK","/webhook/nivy/send-email"),json=payload); response.raise_for_status(); result=response.json()
            elif tool_id in {"tool.odoo.write","odoo"}:
                base=os.getenv("ODOO_URL","").rstrip("/")
                if not base: raise RuntimeError("ODOO_URL is not configured")
                import httpx
                async with httpx.AsyncClient(timeout=30) as client:
                    response=await client.post(base+"/api/aios/write",json=payload); response.raise_for_status(); result=response.json()
            else: raise RuntimeError(f"no adapter registered for {tool_id}")
            self._record(event_type="tool.execution",actor=agent_id,action=tool_id,status="completed",request_id=run_id,data={"approval_id":approval_id}); return RunResult(run_id,agent_id,tool_id,"completed",result=result)
        except Exception as exc:
            self._record(event_type="tool.execution",actor=agent_id,action=tool_id,status="failed",request_id=run_id,data={"error":str(exc)}); return RunResult(run_id,agent_id,tool_id,"failed",error=str(exc))

RuntimeDenied=PolicyDenied
runtime_engine=RuntimeEngine()
