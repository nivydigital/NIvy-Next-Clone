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
from .runtime.observability import audit_summary, health_snapshot

app = FastAPI(title="Nivy Next AIOS API", version="0.9.1")
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
class A001ResearchRequest(BaseModel): research_question: str; target_market: str; geography: str | None = None; industry: str | None = None; customer_segment: str | None = None; time_horizon: str | None = None; competitor_set: list[str] = Field(default_factory=list); source_policy: dict = Field(default_factory=dict); output_format: str | None = None; evidence: list[dict] = Field(default_factory=list)
class A002ICPRequest(BaseModel): market_research: dict; business_offer: dict = Field(default_factory=dict); existing_customers: list[dict] = Field(default_factory=list); exclusions: list[str] = Field(default_factory=list); geography: str | None = None; revenue_targets: dict = Field(default_factory=dict); request_id: str | None = None
class A003PersonaRequest(BaseModel): icp_definition: dict; market_research: dict = Field(default_factory=dict); business_offer: dict = Field(default_factory=dict); customer_interviews: list[dict] = Field(default_factory=list); exclusions: list[str] = Field(default_factory=list); request_id: str | None = None
class A004CompetitorRequest(BaseModel): market_research: dict; icp_definition: dict = Field(default_factory=dict); business_offer: dict = Field(default_factory=dict); competitor_set: list[str] = Field(default_factory=list); geography: str | None = None; request_id: str | None = None
class A005ChannelRequest(BaseModel): market_research: dict; icp_definition: dict; competitor_intelligence: dict = Field(default_factory=dict); business_offer: dict = Field(default_factory=dict); channel_constraints: list[str] = Field(default_factory=list); historical_performance: list[dict] = Field(default_factory=list); request_id: str | None = None
class ToolRunRequest(BaseModel): payload: dict = Field(default_factory=dict); approval_id: str | None = None
class ApprovalRequest(BaseModel): agent_id: str; tool_id: str; reason: str

@app.get("/health")
def health(): return {"status": "ok", "service": "nivy-backend", "version": "0.9.1", "runtime": runtime_engine.health()}
@app.get("/api/v1/system")
def system(): return {"name": "Nivy Next AIOS", "status": "online", "llm": "Ollama", "memory": "Qdrant", "automation": "n8n", "crm": "Odoo", "runtime": "fail-closed", "revenue_persistence": "sqlite", "api_version": "0.9.1"}
@app.get("/api/v1/runtime/health")
def runtime_health(): return runtime_engine.health()

@app.get("/api/v1/runtime/agents")
def runtime_list_agents():
    return list_agents()

@app.get("/api/v1/runtime/agents/{agent_id}")
def runtime_get_agent(agent_id: str):
    try:
        return get_agent(agent_id.upper() if agent_id[0].lower() == "a" else agent_id)
    except RuntimeDenied as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/api/v1/runtime/agents/{agent_id}/execute")
async def runtime_execute_agent(agent_id: str, request: AgentExecuteRequest):
    aid = agent_id.upper() if agent_id[:1].lower() == "a" else agent_id
    body = dict(request.payload or {})
    if request.request_id and "request_id" not in body:
        body["request_id"] = request.request_id
    try:
        result = await execute_agent(aid, body, prompt_id=request.prompt_id, allow_llm_fallback=request.allow_llm_fallback)
    except RuntimeDenied as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        msg = str(exc)
        if "requires" in msg or "missing" in msg.lower():
            raise HTTPException(status_code=422, detail=msg) from exc
        raise HTTPException(status_code=500, detail=msg) from exc
    if getattr(result, "status", None) == "failed":
        raise HTTPException(status_code=502, detail=result.error or f"{aid} runtime failed")
    return result.__dict__ if hasattr(result, "__dict__") else result

@app.get("/api/v1/runtime/skills/coverage")
def skills_coverage():
    return skill_coverage_report()

@app.get("/api/v1/runtime/agents/{agent_id}/skills/resolve")
def skills_resolve(agent_id: str):
    aid = agent_id.upper() if agent_id[:1].lower() == "a" else agent_id
    try:
        return resolve_agent_skills(aid)
    except RuntimeDenied as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

@app.get("/api/v1/runtime/workflows")
def runtime_list_workflows():
    return {"items": list_workflow_defs()}

@app.get("/api/v1/runtime/workflows/{workflow_id}")
def runtime_get_workflow(workflow_id: str):
    try:
        return load_workflow(workflow_id)
    except RuntimeDenied as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/api/v1/runtime/workflows/{workflow_id}/run")
async def runtime_run_workflow(workflow_id: str, request: WorkflowRunRequest):
    try:
        return await run_workflow(
            workflow_id,
            dict(request.payload or {}),
            dry_run=request.dry_run,
            stop_after_stage=request.stop_after_stage,
        )
    except RuntimeDenied as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/api/v1/runtime/agents/{agent_id}/run")
async def run_agent(agent_id: str, request: AgentRunRequest):
    try: result = await runtime_engine.run_llm(agent_id, request.prompt or "", request.prompt_id, dict(request.context))
    except RuntimeDenied as exc: raise HTTPException(status_code=403, detail=str(exc)) from exc
    return result.__dict__
@app.post("/api/v1/runtime/agents/A001/research")
async def run_a001(request: A001ResearchRequest):
    try: result = await run_a001_research(request.model_dump())
    except A001ResearchError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed": raise HTTPException(status_code=502, detail=result.error or "A001 runtime failed")
    return result.__dict__
@app.post("/api/v1/runtime/agents/A002/icp")
async def run_a002(request: A002ICPRequest):
    try: result = await run_a002_icp(request.model_dump())
    except A002ICPError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed": raise HTTPException(status_code=502, detail=result.error or "A002 runtime failed")
    return result.__dict__
@app.post("/api/v1/runtime/agents/A003/persona")
async def run_a003(request: A003PersonaRequest):
    try: result = await run_a003_persona(request.model_dump())
    except A003BuyerPersonaError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed": raise HTTPException(status_code=502, detail=result.error or "A003 runtime failed")
    return result.__dict__
@app.post("/api/v1/runtime/agents/A004/competitor")
async def run_a004(request: A004CompetitorRequest):
    try: result = await run_a004_competitor(request.model_dump())
    except A004CompetitorError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed": raise HTTPException(status_code=502, detail=result.error or "A004 runtime failed")
    return result.__dict__
@app.post("/api/v1/runtime/agents/A005/channel")
async def run_a005(request: A005ChannelRequest):
    try: result = await run_a005_channel(request.model_dump())
    except A005ChannelStrategyError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    if result.status == "failed": raise HTTPException(status_code=502, detail=result.error or "A005 runtime failed")
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

@app.get("/api/v1/runtime/audit")
def list_runtime_audit(limit: int = 100, event_type: str | None = None, status: str | None = None):
    """Owner Console Phase 4 / OC-4.1 — run history / audit browser."""
    events = list(runtime_engine.audit) if isinstance(getattr(runtime_engine, "audit", None), list) else []
    if not events:
        events = audit_log.list()
    if event_type:
        events = [e for e in events if e.get("event_type") == event_type]
    if status:
        events = [e for e in events if e.get("status") == status]
    events = list(reversed(events))[: max(1, min(limit, 500))]
    return {"items": events, "count": len(events)}

@app.get("/api/v1/runtime/observability/summary")
def observability_summary():
    """Owner Console Phase 4 / OC-4.2 — ops summary for console embeds."""
    summary = audit_summary()
    snap = health_snapshot(checks={"audit_store": True, "approval_store": isinstance(runtime_engine.approvals, dict)})
    pending = 0
    store = getattr(runtime_engine, "approvals", {}) or {}
    if isinstance(store, dict):
        pending = sum(1 for a in store.values() if isinstance(a, dict) and a.get("status") == "pending")
    return {
        "audit": summary,
        "health": snap,
        "approvals_pending": pending,
        "dashboard_spec": "ops/observability/dashboard-spec.yaml",
    }

@app.post("/api/v1/runtime/approvals")
def request_approval(request: ApprovalRequest):
    try: return runtime_engine.request_approval(request.agent_id, request.tool_id, request.reason)
    except RuntimeDenied as exc: raise HTTPException(status_code=403, detail=str(exc)) from exc
@app.post("/api/v1/runtime/approvals/{approval_id}/approve")
def approve(approval_id: str):
    try: return runtime_engine.approve(approval_id)
    except RuntimeDenied as exc: raise HTTPException(status_code=404, detail=str(exc)) from exc
@app.post("/api/v1/runtime/agents/{agent_id}/tools/{tool_id}/execute")
async def execute_tool(agent_id: str, tool_id: str, request: ToolRunRequest):
    result = await runtime_engine.execute(agent_id, tool_id, dict(request.payload), request.approval_id)
    if result.status == "failed" and result.error and ("approval" in result.error or "protected" in result.error): raise HTTPException(status_code=403, detail=result.error)
    return result.__dict__
@app.post("/api/v1/email/send")
async def send_email(request: SendEmailRequest):
    payload = request.model_dump()
    if not request.approval_id:
        approval = runtime_engine.request_approval("A044", "tool.email.send", "Explicit approval required before outbound email")
        return {"status": "approval_required", "approval": approval, "next": "Resend with approval_id set to approval.approval_id after human approval"}
    result = await runtime_engine.execute("A044", "tool.email.send", payload, request.approval_id)
    if result.status == "failed": return {"status": "failed", "run": result.__dict__}
    return result.__dict__
@app.post("/api/v1/revenue/leads", status_code=201)
def create_lead(request: LeadCreateRequest):
    return revenue_engine.create_lead(name=request.name, email=str(request.email), company=request.company, source=request.source, request_id=request.request_id, actor=request.actor).to_dict()
@app.get("/api/v1/revenue/leads")
def list_leads(): return {"items": [lead.to_dict() for lead in revenue_engine.list_leads()]}
@app.post("/api/v1/revenue/leads/{lead_id}/qualify")
def qualify_lead(lead_id: str, request: LeadQualifyRequest):
    try: return revenue_engine.qualify(lead_id, score=request.score).to_dict()
    except KeyError as exc: raise HTTPException(status_code=404, detail="lead not found") from exc
    except ValueError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
@app.post("/api/v1/revenue/leads/{lead_id}/proposal/request")
def request_proposal_approval(lead_id: str):
    try: return revenue_engine.request_proposal_approval(lead_id).to_dict()
    except KeyError as exc: raise HTTPException(status_code=404, detail="lead not found") from exc
@app.post("/api/v1/revenue/leads/{lead_id}/proposal/approve")
def approve_proposal(lead_id: str):
    try: return revenue_engine.approve_proposal(lead_id, actor="human").to_dict()
    except KeyError as exc: raise HTTPException(status_code=404, detail="lead not found") from exc
@app.get("/api/v1/revenue/leads/{lead_id}/audit")
def lead_audit(lead_id: str): return {"items": revenue_engine.audit_events(lead_id)}
@app.get("/api/v1/revenue/summary")
def revenue_summary():
    leads = revenue_engine.list_leads(); counts = {status.value: 0 for status in LeadStatus}
    for lead in leads: counts[lead.status.value] += 1
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
