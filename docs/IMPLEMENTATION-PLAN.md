# Nivy Next AIOS — Complete Implementation Plan

## Purpose

This document is the master execution plan for turning the current Nivy Next AIOS foundation into a working, testable, production-oriented multi-agent automation platform.

**Rule:** We do not mark a phase complete because files exist. A phase is complete only when its code, integration, tests, configuration, documentation, and end-to-end acceptance checks pass.

## Status Legend

- `[ ]` Not started
- `[~]` In progress
- `[x]` Complete and verified
- `[!]` Blocked / requires external credential or decision

## Overall Progress

**0% — Planning baseline**

| Phase | Area | Status | Exit condition |
|---|---|---:|---|
| 0 | Baseline & repository governance | [x] | Plan and tracker committed |
| 1 | AIOS runtime foundation | [ ] | Agents can execute through one runtime |
| 2 | Persistence & database | [ ] | Runs/tasks/business state persist reliably |
| 3 | Tool & skill execution | [ ] | Skills dispatch approved tools with audit |
| 4 | Memory / RAG / documents | [ ] | Ingestion and retrieval work end-to-end |
| 5 | Orchestration & job execution | [ ] | Async/retry/locking/scheduling works |
| 6 | Lead-generation pipeline | [ ] | Lead discovery through verified storage works |
| 7 | Email outreach & follow-up | [ ] | Approval-controlled outreach lifecycle works |
| 8 | Inbound email & customer communication | [ ] | Replies are classified and handled safely |
| 9 | Content / social automation | [ ] | Multi-platform content pipeline works with approval |
| 10 | SEO automation | [ ] | SEO audit/research/content workflow works |
| 11 | Frontend AIOS control plane | [ ] | UI controls and observes the runtime |
| 12 | Governance, security & observability | [ ] | Secrets, permissions, audit and health are enforced |
| 13 | Evaluation & regression testing | [ ] | Agent quality and workflows are continuously tested |
| 14 | Production hardening & release | [ ] | Repeatable deployment and recovery are verified |
| 15 | End-to-end acceptance | [ ] | Realistic business scenarios pass |

---

# Phase 0 — Baseline & Repository Governance

**Status: [x]**

- [x] Agent registry exists.
- [x] Skill catalog exists.
- [x] Tool registry exists.
- [x] Automation map exists.
- [x] This implementation plan exists.
- [ ] Verify every registry path against the repository.
- [ ] Add a machine-readable progress tracker.
- [ ] Define Definition of Done and release gates.

**Exit test:** Repository has one authoritative implementation plan and no ambiguous source of truth.

# Phase 1 — AIOS Runtime Foundation

**Status: [ ]**

Build the execution engine behind the existing agent definitions.

- [ ] Registry loader for agents, skills, tools and workflows.
- [ ] Prompt loader/versioning.
- [ ] Agent execution service.
- [ ] Ollama client with model/config abstraction.
- [ ] Structured agent input/output contracts.
- [ ] Agent run lifecycle: queued → running → waiting → succeeded/failed/cancelled.
- [ ] Context builder.
- [ ] Timeout and cancellation handling.
- [ ] Structured error model.
- [ ] `POST /api/v1/agents/run` API.
- [ ] `GET /api/v1/agents/runs/{id}` API.
- [ ] Runtime unit/integration tests.

**Exit test:** A registered agent can receive a task, load its prompt/skills, call Ollama, return structured output, and persist a run record.

# Phase 2 — Persistence & Database

**Status: [ ]**

Create versioned migrations and repositories for:

- [ ] agents
- [ ] agent_runs
- [ ] tasks
- [ ] tool_calls
- [ ] workflows
- [ ] workflow_runs
- [ ] leads
- [ ] campaigns
- [ ] campaign_leads
- [ ] contacts
- [ ] messages
- [ ] approvals
- [ ] audit_logs
- [ ] memory_items
- [ ] documents
- [ ] evaluation_runs

Also add:

- [ ] indexes for common searches
- [ ] status/state constraints
- [ ] timestamps and correlation IDs
- [ ] migration strategy
- [ ] repository/data-access layer
- [ ] database integration tests

**Exit test:** A complete agent run and a lead/campaign lifecycle survive API/container restart.

# Phase 3 — Tool & Skill Execution

**Status: [ ]**

- [ ] Skill dispatcher.
- [ ] Tool permission checks.
- [ ] Tool input/output schemas.
- [ ] PostgreSQL adapter.
- [ ] Redis adapter.
- [ ] Qdrant adapter.
- [ ] MinIO adapter.
- [ ] Ollama adapter.
- [ ] n8n adapter.
- [ ] Reacher adapter.
- [ ] Email provider abstraction.
- [ ] Browser/web research adapter.
- [ ] Apify adapter where credentials are configured.
- [ ] Tool-call audit events.
- [ ] Retry policy per tool.
- [ ] Credential/config validation.

**Exit test:** An agent can invoke an allowed tool through the registry; a disallowed tool is rejected and audited.

# Phase 4 — Memory / RAG / Documents

**Status: [ ]**

- [ ] MinIO document storage.
- [ ] Text extraction pipeline.
- [ ] Chunking.
- [ ] Embedding provider abstraction.
- [ ] Qdrant collection management.
- [ ] Metadata in PostgreSQL.
- [ ] Retrieval service.
- [ ] Source/evidence tracking.
- [ ] Memory write policy.
- [ ] Memory retrieval policy.
- [ ] Delete/update/re-index support.
- [ ] RAG integration into agent context.

**Exit test:** Upload a document, index it, retrieve relevant passages, and produce an answer with source references.

# Phase 5 — Orchestration & Job Execution

**Status: [ ]**

- [ ] Task queue using Redis.
- [ ] Worker process.
- [ ] Distributed lock/idempotency strategy.
- [ ] Retry/backoff.
- [ ] Dead-letter handling.
- [ ] Scheduled jobs.
- [ ] Workflow state machine.
- [ ] n8n trigger adapter.
- [ ] Callback/webhook handling.
- [ ] Correlation IDs.
- [ ] Recovery after process restart.

**Exit test:** A multi-step workflow can pause, retry a failed step, resume, and finish without duplicating side effects.

# Phase 6 — Lead Generation Pipeline

**Status: [ ]**

Flow:

`source → discover → normalize → dedupe → enrich → verify → score → store`

- [ ] Lead source abstraction.
- [ ] Google Maps/Apify workflow.
- [ ] Website discovery.
- [ ] Contact extraction.
- [ ] Normalization.
- [ ] Deduplication.
- [ ] Lead scoring rules.
- [ ] Reacher verification.
- [ ] Verification status persistence.
- [ ] Source/evidence storage.
- [ ] Campaign assignment.
- [ ] Lead API/UI.

**Exit test:** A batch of leads can be imported, deduplicated, enriched, verified and viewed with complete status history.

# Phase 7 — Email Outreach & Follow-up

**Status: [ ]**

- [ ] Email provider abstraction.
- [ ] Gmail integration.
- [ ] Outlook integration.
- [ ] SMTP integration.
- [ ] Personalization agent.
- [ ] Template/version management.
- [ ] Human approval gate.
- [ ] Send operation.
- [ ] Message/event tracking.
- [ ] Bounce/failed-send handling.
- [ ] Follow-up #1.
- [ ] Follow-up #2.
- [ ] Stop conditions: reply, unsubscribe, bounce, campaign stop.
- [ ] Scheduling.
- [ ] Rate limits.
- [ ] Safe sending policies.

**External credential gate:** Gmail/Outlook/SMTP credentials must be supplied and configured by the user. Do not commit secrets.

**Exit test:** A test campaign can generate a message, request approval, send it through a configured provider, record the event, and stop follow-ups when a reply/opt-out condition occurs.

# Phase 8 — Inbound Email & Customer Communication

**Status: [ ]**

- [ ] IMAP/provider inbox adapter.
- [ ] Poll/webhook strategy.
- [ ] Thread matching.
- [ ] Reply classification.
- [ ] Intent detection.
- [ ] Auto-reply detection.
- [ ] Human escalation.
- [ ] Draft reply generation.
- [ ] Approval before external response where policy requires.
- [ ] Customer/contact history.
- [ ] Unsubscribe/opt-out handling.

**Exit test:** An inbound message is matched to the correct contact/campaign, classified, and routed to draft/approval/escalation safely.

# Phase 9 — Content & Social Automation

**Status: [ ]**

- [ ] Content brief intake.
- [ ] Research/context gathering.
- [ ] Content generation.
- [ ] Editing/quality checks.
- [ ] Platform-specific formatting.
- [ ] LinkedIn output.
- [ ] Instagram output.
- [ ] Facebook output.
- [ ] X output.
- [ ] TikTok/short-form output.
- [ ] Threads output.
- [ ] YouTube Shorts output.
- [ ] Approval workflow.
- [ ] Publishing-provider abstraction.
- [ ] Scheduling.
- [ ] Result/audit storage.

**Exit test:** One brief produces platform-specific drafts, passes validation, requests approval, and can publish through a configured provider.

# Phase 10 — SEO Automation

**Status: [ ]**

- [ ] Keyword research adapter.
- [ ] Website crawl/input.
- [ ] Technical SEO checks.
- [ ] On-page checks.
- [ ] Content gap analysis.
- [ ] Keyword clustering.
- [ ] SEO brief generation.
- [ ] Content generation.
- [ ] Optimization/editing.
- [ ] Report persistence.
- [ ] Evidence/source capture.

**Exit test:** A website/project can produce a reproducible SEO audit and content brief with evidence and stored results.

# Phase 11 — Frontend AIOS Control Plane

**Status: [ ]**

- [ ] Agent list/details.
- [ ] Start task/run.
- [ ] Run status/log viewer.
- [ ] Workflow monitor.
- [ ] Lead management.
- [ ] Campaign management.
- [ ] Email/message history.
- [ ] Approval inbox.
- [ ] Memory/document browser.
- [ ] System health dashboard.
- [ ] Error/retry controls.
- [ ] Role-aware UI.

**Exit test:** A user can start and monitor the main workflows without directly editing backend data.

# Phase 12 — Governance, Security & Observability

**Status: [ ]**

- [ ] Secret management via environment/secret store.
- [ ] Remove insecure default secrets from production mode.
- [ ] Authentication.
- [ ] Authorization/RBAC.
- [ ] Tool allowlists.
- [ ] Approval policies.
- [ ] Input validation.
- [ ] Output validation.
- [ ] Audit logs.
- [ ] Structured application logs.
- [ ] Metrics/health checks.
- [ ] Correlation IDs.
- [ ] PII/data-retention policy.
- [ ] Rate limiting.
- [ ] Safe external-side-effect policy.
- [ ] Backup/restore procedure.

**Exit test:** Every external side effect is attributable to a user/task/run, permission-checked, and auditable.

# Phase 13 — Evaluation & Regression Testing

**Status: [ ]**

- [ ] Agent test cases.
- [ ] Prompt regression suite.
- [ ] Structured-output validation tests.
- [ ] Tool-call tests.
- [ ] Workflow integration tests.
- [ ] Lead pipeline tests.
- [ ] Email lifecycle tests.
- [ ] RAG retrieval tests.
- [ ] Failure/retry tests.
- [ ] Safety/governance tests.
- [ ] Evaluation reports.
- [ ] CI test execution.

**Exit test:** A code/prompt change can be evaluated against a repeatable regression suite before release.

# Phase 14 — Production Hardening & Release

**Status: [ ]**

- [ ] Pin critical container versions.
- [ ] Fix installer defaults and remove hard-coded drive assumptions.
- [ ] Make image pulling optional/configurable for offline/local development.
- [ ] Environment validation.
- [ ] Production compose profile/config.
- [ ] Database migrations on deployment.
- [ ] Backup and restore test.
- [ ] Health/readiness checks.
- [ ] Resource limits.
- [ ] Upgrade procedure.
- [ ] Rollback procedure.
- [ ] Security review.
- [ ] Documentation for Windows local deployment.

**Exit test:** A clean machine can be configured from documented instructions and the system can be upgraded or rolled back safely.

# Phase 15 — End-to-End Acceptance

**Status: [ ]**

The following scenarios must pass from the UI/API without manually editing database rows:

1. [ ] Run a research task.
2. [ ] Generate and persist leads.
3. [ ] Enrich and verify leads.
4. [ ] Create a campaign.
5. [ ] Generate personalized outreach.
6. [ ] Approve and send a test email.
7. [ ] Detect an inbound reply.
8. [ ] Stop follow-ups after reply/opt-out.
9. [ ] Generate multi-platform social content.
10. [ ] Approve a content item.
11. [ ] Ingest a document and retrieve it through RAG.
12. [ ] Run an SEO audit.
13. [ ] Inspect audit trail for all external side effects.
14. [ ] Restart containers and verify state recovery.
15. [ ] Run the regression suite successfully.

**Final exit condition:** The platform is considered complete only when all critical acceptance scenarios pass and all required external credentials/providers have been explicitly configured.

---

# Repository Organization

The implementation should remain organized around clear ownership:

```text
Nivy-Next-AIOS/
├── agents/                 # agent definitions/registry
├── skills/                 # skill definitions/catalog
├── prompts/                # versioned agent prompts
├── tools/                  # tool definitions/permissions/contracts
├── workflows/              # workflow definitions and n8n exports
├── schemas/                # JSON schemas/contracts
├── backend/
│   └── app/
│       ├── aios/           # runtime/orchestration implementation
│       ├── api/             # HTTP API routes
│       ├── db/              # database access/migrations adapters
│       ├── integrations/    # external service adapters
│       └── tests/           # backend tests
├── frontend/               # AIOS control plane
├── database/               # migrations and initialization
├── docs/                   # architecture/runbooks/plans
├── setup/                  # local installation/setup scripts
├── tests/                  # cross-service/e2e tests
└── docker-compose.yml
```

## Progress Update Rule

After each implementation batch:

1. Update this document's phase status.
2. Update `docs/PROGRESS.md`.
3. Record the commit/change summary.
4. Record tests executed and their result.
5. Record blockers/required credentials.
6. Do not mark a phase `[x]` until its exit test passes.

## Dependency Order

`0 → 1 → 2 → 3 → 5 → 6 → 7 → 8`

Parallel after core runtime:

`4, 9, 10, 11, 12, 13`

Final:

`14 → 15`

## Working Principle

Build vertically, not just file-by-file. Every phase should connect real code to the running Docker stack and have a demonstrable acceptance test.
