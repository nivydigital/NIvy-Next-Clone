# Updated Plan & Architecture — Library Rescan 2026-09-20

**Source:** https://github.com/nivyindia/Raw-Repository/tree/main/external-solutions/business-structure-planning-ai-library  
**Rescan:** 2026-09-20  
**Core rule:** `DISCOVER → DECOMPOSE → REUSE → ADAPT → INTEGRATE → BUILD ONLY WHAT IS MISSING`

**Software policy:** Prefer **100% open-source** (or OSI-compatible) software. Proprietary SaaS only if no viable open-source alternative exists after evaluation. All production choices must have inspectable code + acceptable license.

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
| Lead Qualification | n8n qualify, enrichment MCPs, sales skills |
| Website Concierge / Receptionist | Intake + RAG + knowledge (file 52) |
| Appointment Setter | Calendar MCP + qualification |
| Support (basic) | Anthropic CS + support skills |

**Lead gen / scrape / extract stack (open-source):**
- Firecrawl, Crawl4AI, Browser Use, Skyvern, Playwright
- GPT Researcher, Hermes pipelines, Apify agent-skills (open parts)

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

### H. Runtime candidates (evaluate, don’t lock) — Open Source First

| Need | Open-source options (preferred) |
|------|----------------------------------|
| Orchestration | LangGraph, CrewAI, AutoGen/AG2, PydanticAI, smolagents, Agno, AgentScope |
| Local digital workers | Hermes Agent, Goose, OpenClaw, Agent Zero, OpenHands |
| Memory | Mem0, Zep, Graphiti, Letta, Cognee |
| RAG / Knowledge | LlamaIndex, Haystack, RAGFlow, Microsoft GraphRAG, AnythingLLM, Onyx |
| Automation / workflows | **n8n**, Flowise, Dify, Activepieces, Windmill, Temporal, Kestra |
| MCP / connectors | Official MCP servers, FastMCP |
| Voice / realtime | LiveKit Agents, Pipecat, Whisper, Coqui TTS, OpenVoice |
| Browser / computer use | Browser Use, Skyvern, Stagehand, Playwright |
| Local LLM runtime | **Ollama**, llama.cpp, vLLM, Open WebUI |
| Model gateway | LiteLLM |
| UI workspace | Open WebUI, AnythingLLM + custom shell |
| CRM (candidate) | Odoo Community, Relaticle, crmkit |
| ERP / Finance | Odoo Community, Hisaabo, lambda-erp |
| Identity | Keycloak, ZITADEL |
| Knowledge graph | Neo4j Community, Kuzu, Memgraph, FalkorDB |
| Scraping / crawl | Firecrawl, Crawl4AI, Playwright |

---

## 7. Canonical Open-Source Software List (Nivy Stack Preference)

**Policy:** Use only open-source / OSI-compatible software unless a critical gap has no viable FOSS alternative after evaluation.

### Core AI / Agent Runtime
| Software | License (typical) | Role |
|----------|-------------------|------|
| **Ollama** | MIT | Local LLM runtime |
| **llama.cpp** | MIT | Local inference |
| **vLLM** | Apache-2.0 | High-throughput inference |
| **Open WebUI** | BSD-3 | Local AI workspace / chat UI |
| **AnythingLLM** | MIT | Local RAG + workspace |
| **LiteLLM** | MIT | Multi-provider model gateway |
| **LangGraph** | MIT | Stateful agent orchestration |
| **CrewAI** | MIT | Multi-agent teams |
| **AutoGen / AG2** | Apache-2.0 / MIT | Multi-agent conversations |
| **PydanticAI** | MIT | Typed Python agents |
| **smolagents** | Apache-2.0 | Lightweight code agents |
| **Hermes Agent** | (check repo) | Self-improving local agent |
| **Goose** | Apache-2.0 | Local AI coworker |
| **OpenClaw** | (check repo) | Local agent ecosystem |
| **Agent Zero** | (check repo) | General computer-using agent |
| **OpenHands** | MIT | Autonomous coding agent |

### Memory / RAG / Knowledge
| Software | Role |
|----------|------|
| **Mem0** | Long-term agent memory |
| **Zep** | Temporal / agent memory |
| **Graphiti** | Temporal knowledge graph |
| **Letta** | Stateful agents + memory |
| **LlamaIndex** | RAG + agents |
| **Haystack** | RAG pipelines |
| **RAGFlow** | Document RAG platform |
| **Microsoft GraphRAG** | Knowledge-graph RAG |
| **Onyx** | Enterprise search / RAG |
| **Neo4j Community** | Graph DB |
| **Kuzu / Memgraph / FalkorDB** | Embedded / alternative graph DBs |

### Automation / Workflows / Connectors
| Software | Role |
|----------|------|
| **n8n** | Primary workflow automation (self-host) |
| **Flowise** | Visual LLM/agent flows |
| **Dify** | LLM app platform |
| **Activepieces** | Open automation |
| **Windmill** | Developer-centric workflows |
| **Temporal** | Durable workflow engine |
| **Kestra** | Orchestration |
| **Playwright** | Browser automation |
| **Browser Use** | LLM browser control |
| **Skyvern** | Vision + browser workflows |
| **Stagehand** | AI browser automation |
| **Crawl4AI** | Web crawling for agents |
| **Firecrawl** | Web scraping / crawl (open parts) |
| **Official MCP + FastMCP** | Tool / connector protocol |

### Voice / Speech / Realtime
| Software | Role |
|----------|------|
| **LiveKit Agents** | Realtime voice/video agents |
| **Pipecat** | Voice + multimodal pipelines |
| **Whisper** | Speech recognition |
| **Coqui TTS** | Voice synthesis |
| **OpenVoice** | Voice cloning research |

### Business Systems (CRM / ERP / OS)
| Software | Role |
|----------|------|
| **Odoo Community** | CRM + ERP + accounting baseline |
| **Relaticle** | AI-first CRM (AGPL) |
| **crmkit** | Portable AI CRM skills |
| **Hisaabo** | India/SMB finance OS candidate |
| **Keycloak** | Identity & access |
| **ZITADEL** | Modern identity alternative |

### Sales / Lead / Skills Libraries (open)
| Software / Repo | Role |
|-----------------|------|
| **astDeniss/business-skills** | 69 business SKILL.md playbooks |
| **Autter-dev/agentic-sales-skills** | 11 agents + 48 sales skills |
| **TheCraigHewitt/sales-skills** | B2B sales lifecycle skills |
| **Anthropic knowledge-work-plugins** | Official sales/marketing/ops plugins |
| **Anthropic skills** | Skill authoring standard |
| **gtm-skills/gtm** | Agentic GTM OS |
| **GPT Researcher** | Deep research agent |
| **Apify agent-skills** | Web/social acquisition skills |

### Observability / Governance / Infra helpers
| Software | Role |
|----------|------|
| **OpenMetadata / DataHub / OpenLineage** | Data catalog & lineage |
| Git + structured logs | Audit trail baseline |
| **Prefect** (optional) | Workflow observability |

### Explicitly deferred / evaluate only if FOSS fails
- Closed SaaS CRMs, closed voice platforms, closed enrichment APIs — only after open alternatives are tested and fail license/control/quality gates.

---

## 8. Open-Source Decision Rules

1. **Default = open source.** Every new tool must be checked against the list above first.
2. Prefer **self-hostable** (n8n, Ollama, Open WebUI, Keycloak, Odoo Community).
3. License must allow commercial use and modification (MIT, Apache-2.0, BSD preferred; AGPL only with clear isolation).
4. No credentials in Git, prompts, or docs.
5. If a proprietary tool is proposed, document: why FOSS failed, data residency impact, exit plan.
6. All adopted assets stay in the Master Asset Registry with source URL + license + adaptation date.

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
| Software policy | Mixed | **Open-source first** (full FOSS list added) |

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
**Stack policy = open source first** (Ollama, n8n, LangGraph/CrewAI, Mem0, LlamaIndex, Playwright, Odoo Community, Keycloak, etc.).  
Khud se banana almost nahi — mostly FOSS reuse + adapt + govern.
