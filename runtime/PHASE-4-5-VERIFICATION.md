# Phase 4–5 Verification Contract

## Phase 4 — Policy, Approval, Safety & Trust

Implemented controls:
- default-deny for undeclared tools
- agent-to-tool binding enforcement
- protected side effects require explicit approval
- approval request/approve API
- credentials are environment-backed and never accepted as tool payload secrets
- audit events for agent runs, approval decisions and tool execution
- autonomous mode is disabled by default

## Phase 5 — Infrastructure & Runtime Fabric

Implemented runtime foundation:
- FastAPI executable runtime boundary
- registry-backed agent loading
- Ollama inference adapter
- n8n email integration adapter
- Odoo integration boundary
- runtime health endpoint
- runtime evaluation endpoint
- Docker service architecture for PostgreSQL, Redis, Qdrant, MinIO, Ollama, n8n and Reacher
- `.env.runtime.example` for local configuration

## Runtime gates

An agent is not considered production-autonomous merely because its registry declaration exists. Activation requires:
1. declared agent
2. bound capability
3. policy allow
4. approval where protected
5. configured integration credentials
6. dependency health
7. evaluation evidence
8. durable audit/observability

## Local verification

```powershell
Copy-Item .env.runtime.example .env
# Fill only local secrets/credentials.
docker compose up -d --build
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/api/v1/evaluation/runtime
```

Protected email execution must first create an approval and then execute using the returned approval ID. No secret belongs in Git.
