from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from .revenue import LeadStatus, revenue_engine
from .runtime.a001 import A001ResearchError, run_a001_research
from .runtime.a002 import A002ICPError, run_a002_icp
from .runtime.a003 import A003BuyerPersonaError, run_a003_persona
from .runtime.a004 import A004CompetitorError, run_a004_competitor
from .runtime.a005 import A005ChannelStrategyError, run_a005_channel
from .runtime.discovery import execute_agent, get_agent, list_agents
from .runtime.engine import RuntimeDenied, runtime_engine
from .runtime.skills import resolve_agent_skills, skill_coverage_report
from .runtime.workflows import list_workflow_defs, load_workflow, run_workflow
from .runtime.audit import audit_log

app = FastAPI(title="Nivy Next AIOS API", version="0.9.2")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class SendEmailRequest(BaseModel):
    to: EmailStr; subject: str; body: str; body_type: str = "text/html"; cc: str | None = None; bcc: str | None = None; from_email: EmailStr | None = None; verify_email: bool = True; send_after_verification: bool = True; request_id: str | None = None; approval_id: str | None = None
class LeadCreateRequest(BaseModel):
    name: str; email: EmailStr; company: str | None = None; source: str = "unknown"; request_id: str | None = None; actor: str = "system"
class LeadQualifyRequest(BaseModel): score: int
class AgentRunRequest(BaseModel): prompt: str | None = None; prompt_id: str | None = None; context: dict = Field(default_factory=dict)
class AgentExecuteRequest(BaseModel):
    prompt_id: str | None = None
    allow_llm_fallback: bool = True
    request_id: str | None = None
    payload: dict = Field(default_factory=dict)
class WorkflowRunRequest(BaseModel):
    payload: dict = Field(default_factory=dict)
    dry_run: bool | None = None
    stop_after_stage: str | None = None
class A001ResearchRequest(BaseModel): research_question: str; target_market: str; geography: str | None = None; industry: str | None = None; customer_segment: str | None = None; time_horizon: str | None = None; competitor_set: list[str] | None = None; source_policy: dict = Field(default_factory=dict); output_format: str | None = None; evidence: list[dict] = Field(default_factory=list)
class A002ICPRequest(BaseModel): market_research: dict; business_offer: dict = Field(default_factory=dict); existing_customers: list = Field(default_factory=list); constraints: dict = Field(default_factory=dict)
class A003PersonaRequest(BaseModel): icp: dict; market_context: dict = Field(default_factory=dict)
class A004CompetitorRequest(BaseModel): competitors: list[str]; market: str | None = None; dimensions: list[str] = Field(default_factory=list)
class A005ChannelRequest(BaseModel): icp: dict; persona: dict = Field(default_factory=dict); budget: dict = Field(default_factory=dict)
class ApprovalRequest(BaseModel): agent_id: str; tool_id: str; reason: str
class ToolRunRequest(BaseModel): payload: dict = Field(default_factory=dict); approval_id: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "nivy-next-aios"}

@app.get("/api/v1/system")
def system_status():
    h = runtime_engine.health()
    return {"status": "online", "runtime": h, "version": "0.9.2"}

@app.get("/api/v1/runtime/health")
def runtime_health():
    return runtime_engine.health()

@app.get("/api/v1/runtime/agents")
def agents_list():
    return list_agents()

@app.get("/api/v1/runtime/agents/{agent_id}")
def agent_get(agent_id: str):
    try:
        return get_agent(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/api/v1/runtime/agents/{agent_id}/execute")
async def agent_execute(agent_id: str, request: AgentExecuteRequest):
    try:
        return await execute_agent(
            agent_id,
            prompt_id=request.prompt_id,
            allow_llm_fallback=request.allow_llm_fallback,
            request_id=request.request_id,
            payload=request.payload,
        )
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.get("/api/v1/runtime/skills/coverage")
def skills_coverage():
    return skill_coverage_report()

@app.get("/api/v1/runtime/agents/{agent_id}/skills/resolve")
def agent_skills_resolve(agent_id: str):
    try:
        return resolve_agent_skills(agent_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.get("/api/v1/runtime/workflows")
def workflows_list():
    return {"items": list_workflow_defs()}

@app.get("/api/v1/runtime/workflows/{workflow_id}")
def workflow_get(workflow_id: str):
    try:
        return load_workflow(workflow_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/api/v1/runtime/workflows/{workflow_id}/run")
async def workflow_run(workflow_id: str, request: WorkflowRunRequest):
    try:
        return await run_workflow(
            workflow_id,
            payload=request.payload,
            dry_run=request.dry_run,
            stop_after_stage=request.stop_after_stage,
        )
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/api/v1/runtime/agents/{agent_id}/run")
async def agent_run(agent_id: str, request: AgentRunRequest):
    try:
        return await runtime_engine.run_llm(agent_id, request.prompt, request.prompt_id, request.context)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/api/v1/runtime/agents/A001/research")
async def a001_research(request: A001ResearchRequest):
    try:
        result = await run_a001_research(request.model_dump())
    except A001ResearchError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed":
        raise HTTPException(status_code=502, detail=result.error or "A001 runtime failed")
    return result.__dict__

@app.post("/api/v1/runtime/agents/A002/icp")
async def a002_icp(request: A002ICPRequest):
    try:
        result = await run_a002_icp(request.model_dump())
    except A002ICPError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed":
        raise HTTPException(status_code=502, detail=result.error or "A002 runtime failed")
    return result.__dict__

@app.post("/api/v1/runtime/agents/A003/persona")
async def a003_persona(request: A003PersonaRequest):
    try:
        result = await run_a003_persona(request.model_dump())
    except A003BuyerPersonaError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed":
        raise HTTPException(status_code=502, detail=result.error or "A003 runtime failed")
    return result.__dict__

@app.post("/api/v1/runtime/agents/A004/competitor")
async def a004_competitor(request: A004CompetitorRequest):
    try:
        result = await run_a004_competitor(request.model_dump())
    except A004CompetitorError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed":
        raise HTTPException(status_code=502, detail=result.error or "A004 runtime failed")
    return result.__dict__

@app.post("/api/v1/runtime/agents/A005/channel")
async def a005_channel(request: A005ChannelRequest):
    try:
        result = await run_a005_channel(request.model_dump())
    except A005ChannelStrategyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed":
        raise HTTPException(status_code=502, detail=result.error or "A005 runtime failed")
    return result.__dict__

@app.get("/api/v1/runtime/approvals")
def list_approvals():
    """Owner Console: list in-memory approvals (pending + recent)."""
    store = getattr(runtime_engine, "approvals", {}) or {}
    items = []
    if isinstance(store, dict):
        for key, value in store.items():
            if isinstance(value, dict):
                row = {"approval_id": key, **value}
            else:
                row = {"approval_id": key, "value": value}
            items.append(row)
    return {"items": items, "count": len(items)}

@app.post("/api/v1/runtime/approvals")
def request_approval(request: ApprovalRequest):
    try:
        return runtime_engine.request_approval(request.agent_id, request.tool_id, request.reason)
    except RuntimeDenied as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

@app.post("/api/v1/runtime/approvals/{approval_id}/approve")
def approve(approval_id: str):
    try:
        return runtime_engine.approve(approval_id)
    except RuntimeDenied as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.get("/api/v1/runtime/audit")
def list_audit(limit: int = 100):
    """Owner Console Phase 4: run history / audit browser."""
    engine_events = list(getattr(runtime_engine, "audit", []) or [])
    log_events = audit_log.list()
    # Prefer engine list if populated; merge unique by event_id
    by_id = {}
    for e in log_events + engine_events:
        if isinstance(e, dict):
            eid = e.get("event_id") or e.get("request_id") or str(id(e))
            by_id[eid] = e
    items = list(by_id.values())
    items.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
    if limit and limit > 0:
        items = items[:limit]
    return {"items": items, "count": len(items)}

@app.get("/api/v1/runtime/observability/summary")
def observability_summary():
    """Owner Console Phase 4: lightweight ops cards (no Grafana required)."""
    engine_events = list(getattr(runtime_engine, "audit", []) or [])
    log_events = audit_log.list()
    events = engine_events if engine_events else log_events
    total = len(events)
    by_status: dict[str, int] = {}
    by_type: dict[str, int] = {}
    errors = 0
    for e in events:
        if not isinstance(e, dict):
            continue
        st = str(e.get("status") or "unknown")
        et = str(e.get("event_type") or e.get("action") or "unknown")
        by_status[st] = by_status.get(st, 0) + 1
        by_type[et] = by_type.get(et, 0) + 1
        if st in ("error", "failed", "denied"):
            errors += 1
    health = runtime_engine.health()
    approvals = getattr(runtime_engine, "approvals", {}) or {}
    pending = sum(1 for v in approvals.values() if isinstance(v, dict) and v.get("status") == "pending")
    return {
        "audit_events": total,
        "errors": errors,
        "by_status": by_status,
        "by_event_type": by_type,
        "pending_approvals": pending,
        "runtime_health": health,
        "panels_spec": "ops/observability/dashboard-spec.yaml",
        "note": "Full Grafana embed is optional; these cards are the MVP ops surface.",
    }

@app.post("/api/v1/runtime/agents/{agent_id}/tools/{tool_id}/execute")
async def execute_tool(agent_id: str, tool_id: str, request: ToolRunRequest):
    result = await runtime_engine.execute(agent_id, tool_id, dict(request.payload), request.approval_id)
    if result.status == "failed" and result.error and ("approval" in result.error or "protected" in result.error):
        raise HTTPException(status_code=403, detail=result.error)
    return result.__dict__

@app.post("/api/v1/email/send")
async def send_email(request: SendEmailRequest):
    payload = request.model_dump()
    if not request.approval_id:
        raise HTTPException(status_code=403, detail="approval_id required for email send")
    result = await runtime_engine.execute("email", "send", payload, request.approval_id)
    return result.__dict__

@app.get("/api/v1/revenue/leads")
def list_leads():
    return {"items": [lead.to_dict() for lead in revenue_engine.list_leads()]}

@app.post("/api/v1/revenue/leads")
def create_lead(request: LeadCreateRequest):
    lead = revenue_engine.create_lead(
        name=request.name,
        email=str(request.email),
        company=request.company,
        source=request.source,
        request_id=request.request_id,
        actor=request.actor,
    )
    return lead.to_dict()

@app.post("/api/v1/revenue/leads/{lead_id}/qualify")
def qualify_lead(lead_id: str, request: LeadQualifyRequest):
    try:
        return revenue_engine.qualify(lead_id, score=request.score).to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="lead not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/api/v1/revenue/leads/{lead_id}/proposal/request")
def request_proposal_approval(lead_id: str):
    try:
        return revenue_engine.request_proposal_approval(lead_id).to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="lead not found") from exc

@app.post("/api/v1/revenue/leads/{lead_id}/proposal/approve")
def approve_proposal(lead_id: str):
    try:
        return revenue_engine.approve_proposal(lead_id, actor="human").to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="lead not found") from exc

@app.get("/api/v1/revenue/leads/{lead_id}/audit")
def lead_audit(lead_id: str):
    return {"items": revenue_engine.audit_events(lead_id)}

@app.get("/api/v1/revenue/summary")
def revenue_summary():
    leads = revenue_engine.list_leads()
    counts = {status.value: 0 for status in LeadStatus}
    for lead in leads:
        counts[lead.status.value] += 1
    return {"total_leads": len(leads), "by_status": counts}

@app.get("/api/v1/evaluation/runtime")
def runtime_evaluation():
    discovery = list_agents()
    coverage = skill_coverage_report()
    wfs = list_workflow_defs()
    checks = {
        "registry_loaded": len(runtime_engine.registry.get("agents", [])) > 0,
        "default_deny": runtime_engine.registry.get("policy", {}).get("default_deny", True) is True,
        "approval_store": isinstance(runtime_engine.approvals, dict),
        "audit_store": isinstance(runtime_engine.audit, list),
        "health": runtime_engine.health().get("status") == "ok",
        "executable_prompt_library": len(runtime_engine.prompt_library.get("prompts", {})) >= 8,
        "agent_discovery": discovery.get("count", 0) > 0,
        "structured_entrypoint_count": discovery.get("structured_entrypoint_count", 0) > 0,
        "lead_skills_sk034_sk050": all(f"SK{i:03d}" not in coverage.get("missing_implementations", []) for i in range(34, 51)),
        "phase5_workflows": len([w for w in wfs if w.get("id") in {"inbound-email-triage", "response-qa", "conversation-intel"}]) >= 3,
    }
    return {"passed": sum(checks.values()), "total": len(checks), "checks": checks, "skill_coverage": coverage, "workflows": wfs}
