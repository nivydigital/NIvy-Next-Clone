# New System Structure — Kya Kya Banega / Deliver Hoga

**Date:** 2026-09-19  
**Based on:** Full library rescan + High-Demand Agent Map + Master Registry + Sales OS  
**Principle:** Reuse ready-made agents/skills first → Adapt → Integrate → Build only gaps

---

## 1. Overall System Shape (Target Architecture)

```
                    ┌─────────────────────────┐
                    │   Human / Manager UI    │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  Natural-Language Router │
                    │  + Policy + Approval      │
                    └───────────┬─────────────┘
           ┌────────────────────┼────────────────────┐
           │                    │                    │
   ┌───────▼──────┐    ┌────────▼────────┐   ┌───────▼──────┐
   │ Intake Agents│    │ Specialist Agents│   │ Support/Ops  │
   │ (Lead/Chat/  │    │ (SDR, Research,  │   │ Agents       │
   │  Voice/Web)  │    │  Proposal, CS)   │   │              │
   └───────┬──────┘    └────────┬────────┘   └───────┬──────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  Tools / MCP / APIs     │
                    │  (CRM, Email, Calendar, │
                    │   Scrape, Enrich, RAG)  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  Approval Gate + Audit  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  Systems of Record      │
                    │  (CRM / ERP / Notion /  │
                    │   GitHub / Knowledge)   │
                    └─────────────────────────┘
```

**Not** one giant autonomous agent.  
**Yes** — small specialist agents + router + approval + audit.

---

## 2. What Will Be Delivered (Layers)

### Layer A — Foundation (Phase 0)
| Deliverable | Description | Source / Approach |
|-------------|-------------|-------------------|
| Asset Registry | Every agent/skill/workflow tracked (source, license, test status, approval) | Adopt structure from library file 77 |
| Control Plane | Identity → Registry → Policy → Router → Approval → Audit → Kill Switch | Library architecture |
| Evaluation rules | DISCOVERED → LICENSE_CHECK → POC → ADAPTED → INTEGRATED → PRODUCTION | File 04 rules |
| Provenance standard | Source URL + adaptation date + Nivy version on every asset | Mandatory |

### Layer B — P0 Revenue Agents (First Product Surface)
| Agent / Service | What it does | Ready sources to reuse |
|-----------------|--------------|------------------------|
| **AI SDR** | Account research → personalized outreach draft → CRM update → follow-up | Anthropic Sales, astDeniss skills, Autter agentic-sales-skills, n8n AI SDR, Hermes lead-gen pipeline |
| **Lead Qualification Agent** | Form/chat/voice intake → score → route to CRM | n8n qualify workflows, sales skills, Apollo/enrichment MCP |
| **Website AI Concierge** | Site visitor → FAQ + qualify + book meeting | Knowledge/RAG + intake pattern from file 52 |
| **AI Receptionist** | Inbound call/chat → FAQ + transfer + capture | Voice (LiveKit/Pipecat) + intake agent |
| **AI Appointment Setter** | Qualify + calendar handoff | Calendar MCP + qualification agent |
| **Customer Support Agent (basic)** | Ticket/FAQ → draft reply + escalate | Anthropic CS plugin + support skills |

**Architecture for each:**  
`Channel → Intake → Knowledge/RAG → Specialist → Tool/MCP → Approval → Action → CRM → Audit → Follow-up`

### Layer C — Lead Generation / Scraping / Extraction Stack
| Capability | Ready systems to plug in |
|------------|--------------------------|
| Web / social scraping | Firecrawl, Crawl4AI, Apify Agent Skills, Browser Use, Skyvern |
| Lead research | GPT Researcher, lead-research-agent, Hermes lead-gen, STORM |
| Enrichment | Apollo MCP, b2b-enrichment-mcp, Prospector MCP, OpenLeads |
| Multi-source acquisition | Library file 86 + registry REG-029 to REG-039 |
| Outbound sequences | astDeniss cold-email + LinkedIn skills + n8n sequences |

### Layer D — Sales Department OS (Phase 1)
- Full international sales operating model (library files 89 + 93)
- ICP → Acquisition → Enrichment → Outbound → Discovery → Proposal → CRM → Forecast → Handoff
- Quota, territory, compensation, coaching, partner sales, renewal, advocacy
- Only true gaps custom-built

### Layer E — Runtime & Infrastructure Choices (Evaluate, don’t lock yet)
| Need | Candidates |
|------|------------|
| Agent runtime / orchestration | LangGraph, CrewAI, OpenAI Agents SDK, Hermes Agent, Goose, OpenClaw |
| Local AI workspace | Open WebUI, AnythingLLM, Ollama |
| Memory | Mem0, Zep, Graphiti, Letta |
| RAG / Knowledge | LlamaIndex, Haystack, RAGFlow, GraphRAG |
| Automation / connectors | n8n + MCP servers + Composio |
| Voice | LiveKit Agents, Pipecat |
| Browser automation | Browser Use, Skyvern, Stagehand |

### Layer F — Company OS Composition (Phase 3)
- Cross-department router
- Value streams: Lead→Cash, Content→Revenue, Support→Learning, Monthly Business Review
- Specialist agents for Marketing, Ops, Finance, HR, Legal (P1/P2)
- Shared knowledge + audit + KPI layer

### Layer G — Governance & Scale (Phase 4)
- AgentOps / policy enforcement
- Production readiness checklist
- Test & evaluation suite
- Country / scale activation runbook
- Cost, exception, kill-switch controls

---

## 3. Delivery Sequence (What We Will Actually Do)

```
Week 1–2   Foundation
           → Asset Registry live
           → Control plane minimum
           → License + synthetic test rules fixed

Week 2–4   P0 Agents (first 3)
           → AI SDR
           → Lead Qualification
           → Website Concierge / Receptionist
           → Each: adapt from ready sources → synthetic test → approval gate → pilot

Week 4–6   Lead Gen / Scraping stack
           → Connect Firecrawl / Crawl4AI / Apollo / enrichment MCPs
           → Wire into SDR + Qualification agents

Week 6–8   Sales Department OS mapping
           → Map every sales capability to existing skills/agents
           → Fill only remaining gaps

Later      Runtime finalization (Hermes / Goose / OpenClaw / LangGraph hybrid)
           Marketing + Support + Ops agents
           Full Company OS composition
           Governance + multi-country scale
```

---

## 4. What We Will NOT Do

- Build one giant autonomous agent from scratch
- Custom outbound / CRM write without approval + audit
- Ignore ready-made sources that already cover ≥70% of the job
- Lock runtime before P0 agents are tested
- Skip license / security / synthetic-data checks

---

## 5. Success Definition (First Milestone)

When these three work end-to-end on synthetic + limited real data with human approval:

1. **AI SDR** produces research brief + personalized draft + CRM log  
2. **Lead Qualification** scores and routes a lead correctly  
3. **Website Concierge** answers FAQ + qualifies + books (or hands off)

→ Then system is considered “live P0 revenue surface”.

---

**Summary:**  
Naya system = **Router + specialist ready-made agents (SDR, Qualification, Concierge, Support…) + scraping/enrichment tools + approval/audit + CRM/ERP**.  
Khud se almost kuch nahi banana — mostly select, adapt, integrate, test.
