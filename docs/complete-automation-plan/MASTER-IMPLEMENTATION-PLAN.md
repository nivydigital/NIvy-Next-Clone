# Master Implementation Plan — Complete Automation

**Goal:** Move from agent scaffolding to closed-loop revenue and ops automation.

**Principles**
- Fail closed on missing skill/prompt/tool resolution
- Side effects only via registered tools + approval policy
- Reuse registry IDs; do not invent parallel systems
- Testing deferred until workstreams below allow meaningful suites (then execute `TESTING-PLAN-DEFERRED.md`)

---

## Phase 0 — Inventory & wiring (foundation)

| ID | Task | Exit criteria |
|----|------|----------------|
| P0.1 | Inventory all agent folders vs `agents/registry.yaml` | Diff report in this folder |
| P0.2 | Inventory skills/prompts/tools IDs referenced by agents | Coverage matrix JSON/YAML |
| P0.3 | Register all `a0XX` runtimes in API discovery | `/agents` lists implemented IDs |
| P0.4 | Standard run path: validate → authorize → execute → audit | Single entrypoint documented |

---

## Phase 1 — Tools (unlock real actions)

| ID | Task | Exit criteria |
|----|------|----------------|
| P1.1 | Expand `tools/TOOL-REGISTRY.yaml` with arg schemas + side_effect flags | All tools documented |
| P1.2 | Implement `tool.ollama.generate` hardening (timeouts, JSON mode) | Unit tests |
| P1.3 | Implement `tool.email.send` + mock provider | Mock works in CI |
| P1.4 | Implement `tool.web.fetch` / crawl (public data only) | Mock + live optional |
| P1.5 | Implement verification tool (e.g. email verify) mock | Contract tests |
| P1.6 | Audit wrapper: every tool call logs run_id, args redacted, result status | Logs queryable |

---

## Phase 2 — Prompts (executable bodies)

| ID | Task | Exit criteria |
|----|------|----------------|
| P2.1 | Create `prompts/bodies/` structure | Layout committed |
| P2.2 | Executable bodies for PR001–PR008 | Each has variables + output instructions |
| P2.3 | Map each agent to primary prompt; add agent-specific bodies where needed | No agent references missing PR |
| P2.4 | Align prompt variables to input schemas | Schema check script |

---

## Phase 3 — Skills (procedures)

| ID | Task | Exit criteria |
|----|------|----------------|
| P3.1 | For each skill in `skills/registry.yaml`, add implementation file (procedure, I/O, acceptance) | SK* files present |
| P3.2 | Prioritize skills used by A034–A060 (lead/sales) | Lead path skills green |
| P3.3 | Runtime resolves Agent → Skill → Tool; fail closed if missing | Integration test |
| P3.4 | Skill unit tests (happy + negative) | CI job |

---

## Phase 4 — Workflow: Lead → Outreach (priority revenue path)

Implement as workflow definition + orchestrator steps matching `AIOS-AUTOMATION-MAP` §1:

| Step | Agents / tools |
|------|----------------|
| Discover | A034, A035 |
| Enrich / quality / verify | A036, A037, A038 |
| Score / research | A039, A041 |
| Plan / personalize / draft | A043, A049, A044 |
| Approve | Human gate |
| Send | tool.email.send |
| Follow-up / triage | A050, A052 |

| ID | Task | Exit criteria |
|----|------|----------------|
| P4.1 | Workflow YAML: `workflows/lead-outreach/workflow.yaml` | Valid registry entry |
| P4.2 | State machine: pending → running → await_approval → sent → following_up → done |
| P4.3 | Idempotency keys per lead/campaign |
| P4.4 | Dry-run mode (no external send) |
| P4.5 | Controlled E2E with mocks | Evidence folder |

---

## Phase 5 — Workflow: Inbound + Comms

| ID | Task | Agents |
|----|------|--------|
| P5.1 | Inbound triage workflow | A066, A052 |
| P5.2 | Response draft + QA | A068, A071 |
| P5.3 | Conversation / meeting intel hooks | A067, A069, A070 |

---

## Phase 6 — Remaining agents + control/eval/learning

| ID | Task |
|----|------|
| P6.1 | Implement A100–A103 (Trace, Runtime Quality, Cost, Evidence) |
| P6.2 | Implement A104–A108 (Feedback, Prompt/Skill improvement, Experiment Manager, Regression Guard) |
| P6.3 | Promote registry statuses only after Phase 2–3 resolve for that agent |

---

## Phase 7 — Knowledge, memory, RAG

| ID | Task |
|----|------|
| P7.1 | Complete knowledge packs KP* referenced by registry |
| P7.2 | Agent-bindings complete for active agents |
| P7.3 | Ingest pipeline: extract → chunk → embed → Qdrant + MinIO + PG |
| P7.4 | Memory policy defaults (read/write/retention) |

---

## Phase 8 — Marketing / SEO / Social workflows

| ID | Task |
|----|------|
| P8.1 | Content workflow A084→A085→A091 |
| P8.2 | SEO workflow A086 |
| P8.3 | Social + paid analysis A087–A088 (publish gated) |

---

## Phase 9 — Evaluation (lift deferred testing)

| ID | Task |
|----|------|
| P9.1 | Generate golden fixtures from schemas |
| P9.2 | Run pyramid per `TESTING-PLAN-DEFERRED.md` |
| P9.3 | Chain tests (lead, comms, CS, finance, marketing, control) |
| P9.4 | CI regression job |
| P9.5 | Only then mark agents COMPLETE in progress trackers |

---

## Phase 10 — Hardening & ops

| ID | Task |
|----|------|
| P10.1 | Secrets only in env/secret store |
| P10.2 | Backup/restore drill |
| P10.3 | Observability dashboards |
| P10.4 | Production activation checklist per DEFINITION-OF-DONE |

---

## Suggested execution sequence (near term)

1. P0 inventory + runtime registration  
2. P1 tools (mock-first)  
3. P2 prompts PR001–PR008  
4. P3 skills for lead pipeline  
5. P4 lead-outreach workflow dry-run  
6. Continue agents A100–A108 in parallel once P0 done  
7. P9 testing when P4 dry-run is stable  

Track status in **PROGRESS-TRACKER.md**.
