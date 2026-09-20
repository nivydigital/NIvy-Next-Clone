# Updated Plan & Architecture — Library Rescan 2026-09-20

**Source:** https://github.com/nivyindia/Raw-Repository/tree/main/external-solutions/business-structure-planning-ai-library  
**Rescan:** 2026-09-20  
**Core rule:** `DISCOVER → DECOMPOSE → REUSE → ADAPT → INTEGRATE → BUILD ONLY WHAT IS MISSING`

---

## 1. New Library Structure (Current)

| Folder | Purpose |
|--------|---------|
| **00-navigation-governance** | Indexes, master automation list, evaluation rules |
| **01-discovery-research** | Discovery scope, trackers, source ledgers |
| **02-company-department-models** | International company + department completeness models |
| **03-solution-catalogs** | Agents, skills, prompts, workflows, templates, AI company catalogs (L0–L10) |
| **04-ai-technology-agent-systems** | Agent universe, memory/RAG, ready-made AI tech systems |
| **05-architecture-infrastructure** | Control plane, identity, integrations, workforce architecture |
| **06-adoption-implementation** | Adoption maps, registry, P0 specs, test suite, scale runbook |
| **07-department-sales** | Complete international sales OS + micro audit |
| **08-unified-company-ui-workspace** | **NEW** — One company UI / employee dashboard / portal |
| **09-business-planning-strategy** | **NEW** — Business model, plan, strategy, canvas → AI company |

**Master navigation file:**  
`00-navigation-governance/00-README.md` + `01-MASTER-BUSINESS-AUTOMATION-LIST-2026-09.md`

**Automation hierarchy (canonical):**  
**L0 Atomic Actions → L1 Micro Tasks → L2 Task Automations → L3 Workflows → L4 Business Processes → L5 Department Systems → L6 Cross-Department → L7 AI Managers → L8 AI Executives → L9 Control Tower → L10 Autonomous Company**

Latest library status: L0–L10 all in **Discovery**.

---

## 2. Target Architecture (Updated)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ONE NIVY WORKSPACE (UI Shell)                 │
│  Home · My Work · Company · People · Departments · Customers    │
│  Projects · Finance · Documents · Knowledge · Analytics         │
│  AI Workforce · Automations · Approvals · Governance            │
│  Role-aware: Owner → Exec → Dept Head → Manager → Employee      │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              CONTROL PLANE                                        │
│  Identity · Policy · Router · Registry · Approval · Audit         │
│  Observability · Cost · Exceptions · Kill Switch                  │
└────────────────────────────┬────────────────────────────────────┘
           ┌─────────────────┼─────────────────┐
           │                 │                 │
┌──────────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│  Intake Agents    │ │ Specialist  │ │ AI Managers /   │
│  (Lead/Chat/Voice │ │ Agents      │ │ Executives /    │
│   /Web/Forms)     │ │ (SDR, CS,   │ │ Control Tower   │
│                   │ │  Research,  │ │ (L7–L9)         │
│                   │ │  Ops…)      │ │                 │
└──────────┬────────┘ └──────┬──────┘ └────────┬────────┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│         TOOLS / MCP / CONNECTORS / AUTOMATION LAYER               │
│  CRM · Email · Calendar · Scrape · Enrich · RAG · n8n · Browser  │
│  Voice · Payments · ERP · Knowledge · Analytics                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              SYSTEMS OF RECORD + KNOWLEDGE + MEMORY               │
│  CRM/ERP · Notion/GitHub · Vector/Graph memory · Audit logs       │
└─────────────────────────────────────────────────────────────────┘
```

**Key design rules (from library foundation plan):**
- One system of record per master object
- External communication + financial moves = human-approved first
- Agents get minimum required tools
- Every production action has actor + outcome + audit trail
- Production vs experimental assets separated
- Retries idempotent; human fallback always exists

---

## 3. What We Will Deliver (Updated Layers)

### A. Foundation (Wave 0)
- Master Asset Registry (schema from file 77)
- Control plane minimum (identity, policy, approval classes, audit schema)
- Autonomy levels: Recommend → Approve → Guided Execute → Bounded Autonomous
- Secrets never in Git/prompts

### B. P0 Revenue Spine (Wave 1) — First live surface
```
Lead intake → normalize → enrich/research → CRM → qualify 
→ outreach draft → human approval → send → response capture 
→ calendar → meeting prep → debrief → CRM update → follow-up
```

**Ready agents/services to reuse:**
| Service | Sources |
|---------|---------|
| AI SDR | Anthropic Sales, astDeniss, Autter agentic-sales-skills, n8n AI SDR, Hermes lead-gen |
| Lead Qualification | n8n qualify, enrichment MCPs (Apollo, Prospector), sales skills |
| Website Concierge / Receptionist | Intake + RAG + knowledge (file 52) |
| Appointment Setter | Calendar MCP + qualification |
| Support (basic) | Anthropic CS + support skills |

**Lead gen / scrape / extract stack:**
- Firecrawl, Crawl4AI, Apify, Browser Use, Skyvern
- Apollo MCP, b2b-enrichment-mcp, OpenLeads, GPT Researcher, Hermes pipelines

### C. Delivery Spine (Wave 2)
```
Won deal → handoff → intake → project/tasks → SOP/context 
→ delivery → QA → client update → invoice → CS handoff
```

### D. Finance + Workforce (Wave 3)
- Invoice → accounting → reconciliation → cash snapshot
- Candidate → employee → role → KRA/KPI → tasks → review → learning

### E. Unified Company UI (from folder 08)
**One shell, role-aware views** — not many isolated apps.  
Navigation: Home → My Work → Company → People → Departments → Customers/Leads → Projects → Finance → Documents → Knowledge → Analytics → AI Workforce → Automations → Approvals → Governance

### F. Sales Department OS (folder 07)
- Full international sales operating model (file 89)
- Micro-level completeness audit (file 93)
- Map every capability to existing skills/agents; build only gaps

### G. Higher layers (later)
- L7 Department AI Managers
- L8 Company AI Executives
- L9 Control Tower
- L10 Autonomous Company patterns (discovery only for now)

### H. Runtime candidates (evaluate, don’t lock)
| Need | Options |
|------|---------|
| Orchestration | LangGraph, CrewAI, OpenAI Agents SDK |
| Local digital workers | Hermes Agent, Goose, OpenClaw, Agent Zero |
| Memory | Mem0, Zep, Graphiti, Letta |
| RAG | LlamaIndex, Haystack, RAGFlow, GraphRAG |
| Automation | n8n + MCP + Composio |
| Voice | LiveKit Agents, Pipecat |
| UI workspace | Open WebUI / AnythingLLM patterns + custom shell |

---

## 4. Delivery Sequence (Practical)

| Phase | Focus | Outcome |
|-------|--------|---------|
| **0** | Foundation | Registry + control plane + approval/audit rules live |
| **1** | Revenue spine | AI SDR + Qualification + Concierge working with approval gates |
| **1b** | Lead stack | Scrape/enrich MCPs wired into SDR/Qualification |
| **2** | Delivery spine | Won-deal → onboarding → delivery → invoice path |
| **3** | UI shell | One Nivy workspace (role-aware) over existing systems |
| **4** | Sales OS map | Every sales capability mapped; gaps only custom |
| **5** | Finance/HR | Invoice + workforce basic loops |
| **6** | Managers / Control Tower | L7–L9 patterns after P0/P1 stable |

---

## 5. What Changed Since Last Plan

| Area | Before | Now |
|------|--------|-----|
| Folders | 00–07 | **+08 UI workspace +09 Business planning/strategy** |
| Hierarchy | Implicit | Explicit **L0→L10** automation universe |
| UI | Not primary | **One unified company UI** is now a first-class target |
| Catalogs | Skills + agents | Full catalogs through Control Tower + Autonomous Company |
| Foundation plan | Conceptual | Concrete Wave 0–5 + non-negotiable design rules |
| Master checklist | Partial | Canonical **Master Business Automation List** (micro → company) |

---

## 6. Immediate Next Actions

1. Freeze Asset Registry schema (from file 77 + foundation plan).
2. Implement control-plane minimum (approval classes + audit schema).
3. Pick 3 P0 services: **AI SDR + Lead Qualification + Website Concierge**.
4. Map each to concrete ready sources; synthetic test; add approval gate.
5. Only then wire scrape/enrich MCPs and CRM writes.

**Do not** build L7–L10 autonomous layers before P0 revenue spine is stable and audited.

---

**Bottom line:**  
Library ab full **Company OS + Unified UI + L0–L10 automation hierarchy** tak cover karti hai.  
Nivy ka kaam: **Foundation → P0 Revenue Agents → Lead stack → UI shell → Sales OS map**.  
Khud se banana almost nahi — mostly reuse + adapt + govern.
