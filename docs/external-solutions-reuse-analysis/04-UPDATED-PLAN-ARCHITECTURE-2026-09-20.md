# Updated Plan & Architecture — Library Rescan 2026-09-20

**Source:** https://github.com/nivyindia/Raw-Repository/tree/main/external-solutions/business-structure-planning-ai-library  
**Rescan:** 2026-09-20 (expanded FOSS company-wide list)  
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
| **08-unified-company-ui-workspace** | One company UI / employee dashboard / portal |
| **09-business-planning-strategy** | Business model, plan, strategy, canvas → AI company |

**Master navigation:** `00-README.md` + `01-MASTER-BUSINESS-AUTOMATION-LIST-2026-09.md`  
**Hierarchy:** L0 Atomic → L1 Micro → L2 Task → L3 Workflow → L4 Process → L5 Dept → L6 Cross-Dept → L7 AI Managers → L8 Executives → L9 Control Tower → L10 Autonomous Company

---

## 2. Target Architecture

```
ONE NIVY WORKSPACE (role-aware UI shell)
        ↓
CONTROL PLANE (Identity · Policy · Router · Registry · Approval · Audit · Kill Switch)
        ↓
Intake Agents + Specialist Agents + AI Managers / Executives
        ↓
TOOLS / MCP / n8n / Scrape / Enrich / RAG / Voice / Browser
        ↓
SYSTEMS OF RECORD + Knowledge + Memory + Storage
```

**Rules:** One system of record per object · External comms + money = human-approved · Min tools per agent · Full audit trail · Idempotent retries · Human fallback always.

---

## 3. Delivery Layers (Summary)

| Wave | Focus |
|------|--------|
| 0 | Foundation: Registry + control plane + approval/audit |
| 1 | Revenue spine: AI SDR + Qualification + Concierge |
| 1b | Lead gen / scrape / enrich stack |
| 2 | Delivery spine: won deal → onboarding → invoice |
| 3 | Unified UI shell |
| 4 | Sales OS map + Marketing + HR basics |
| 5 | Finance / workforce loops |
| 6 | L7–L9 managers / control tower (after P0 stable) |

---

## 7. Canonical Open-Source Software List — FULL COMPANY COVERAGE

**Policy:** Default = open source + self-hostable. Check this list before any new tool.

### A. Core AI / Agent Runtime
| Software | Role |
|----------|------|
| **Ollama** | Local LLM runtime |
| **llama.cpp / vLLM** | Local / high-throughput inference |
| **Open WebUI / AnythingLLM** | Local AI workspace + RAG UI |
| **LiteLLM** | Multi-provider model gateway |
| **LangGraph / CrewAI / AutoGen(AG2)** | Agent orchestration |
| **PydanticAI / smolagents / Agno** | Typed / lightweight agents |
| **Hermes Agent / Goose / OpenClaw / Agent Zero / OpenHands** | Local digital workers |

### B. Memory / RAG / Knowledge Graphs
| Software | Role |
|----------|------|
| **Mem0 / Zep / Graphiti / Letta / Cognee** | Agent long-term + temporal memory |
| **LlamaIndex / Haystack / RAGFlow** | RAG frameworks |
| **Microsoft GraphRAG / Onyx** | Graph RAG + enterprise search |
| **Neo4j Community / Kuzu / Memgraph / FalkorDB** | Graph databases |

### C. Automation / Workflows / Connectors
| Software | Role |
|----------|------|
| **n8n** | Primary workflow automation (self-host) |
| **Flowise / Dify / Activepieces / Windmill** | Visual / LLM workflows |
| **Temporal / Kestra** | Durable orchestration |
| **Playwright / Browser Use / Skyvern / Stagehand** | Browser automation |
| **Crawl4AI / Firecrawl** | Web crawl / scrape |
| **Official MCP + FastMCP** | Tool/connector protocol |

### D. CRM / Sales / ERP (core business systems)
| Software | Role |
|----------|------|
| **Odoo Community** | CRM + ERP + accounting + inventory baseline |
| **ERPNext** | Full open ERP (sales, inventory, HR, manufacturing) |
| **Dolibarr** | Lightweight SMB ERP/CRM |
| **Twenty CRM** | Modern developer-first CRM |
| **EspoCRM / SuiteCRM / Krayin** | Classic open CRMs |
| **Relaticle / crmkit** | AI-native CRM patterns |

### E. Marketing / Digital Marketing / SEO / Content
| Software | Role |
|----------|------|
| **Listmonk** | Newsletter / email campaigns (self-host) |
| **Mautic** | Marketing automation (campaigns, segments, forms) |
| **Matomo / Plausible / Umami** | Web analytics (privacy-first GA alternative) |
| **PostHog** | Product analytics + session replay |
| **Ghost** | Blog / content CMS |
| **Strapi / Payload / Directus** | Headless CMS for content |
| **Docusaurus** | Docs / public knowledge sites |
| **Penpot** | Design (Figma alternative) |
| SEO skills from **astDeniss/business-skills** + Anthropic marketing plugins | SEO audit, content strategy, keyword work |
| Social scheduling via **n8n** + open APIs | Cross-post, queues, monitoring |
| **scayver/marketing-skills** | Marketing skill library |

### F. Social Media / Community / Reputation
| Software | Role |
|----------|------|
| **n8n workflows** | Post scheduling, mention monitoring, reply drafts |
| **Chatwoot** | Social + live chat + customer messaging |
| **Rocket.Chat / Mattermost** | Internal + community chat |
| Browser agents (Browser Use / Skyvern) | Authenticated social actions (with policy) |
| Mention/sentiment via scrape + LLM classification | Reputation monitoring |

### G. HR / Employees / Workforce
| Software | Role |
|----------|------|
| **OrangeHRM** | Core HRIS (self-host) |
| **IceHrm** | Modern HRIS |
| **Odoo HR / ERPNext HR / Open HRMS** | HR inside ERP suite |
| **TimeTrex Community** | Time, attendance, payroll |
| **Sentrifugo** | Appraisals + employee self-service |
| Recruitment: CV parse + score via agents + n8n | Screening workflows |
| Onboarding checklists via **n8n** + wiki | Employee lifecycle |

### H. Calendar / Scheduling / Meetings
| Software | Role |
|----------|------|
| **Cal.com** (self-host / Cal.diy fork) | Booking + scheduling (Calendly alternative) |
| **Nextcloud Calendar** | Team calendar + contacts |
| **Xandikos** | CalDAV / CardDAV server |
| **Baikal** | Lightweight CalDAV/CardDAV |
| Meeting notes → tasks via agents + n8n | Transcript → decisions → CRM |

### I. Storage / Files / Collaboration Docs
| Software | Role |
|----------|------|
| **Nextcloud** | Primary file sync, share, Office (Collabora/OnlyOffice) |
| **Seafile** | Alternative file sync |
| **MinIO** | S3-compatible object storage |
| **Collabora Online / OnlyOffice** | Real-time office editing |
| **CryptPad** | Encrypted collaborative docs |
| **HedgeDoc / AFFiNE / Docmost** | Collaborative notes / whiteboards |

### J. Wiki / Knowledge Base / Internal Docs
| Software | Role |
|----------|------|
| **BookStack** | Structured internal wiki (books/chapters/pages) |
| **Outline** | Modern team knowledge base |
| **Wiki.js** | Developer-friendly wiki (Git-backed) |
| **Docmost** | Self-hosted Notion/Confluence alternative + AI |
| **DokuWiki / MediaWiki / XWiki** | Classic / large-scale wikis |
| **Docusaurus** | Public/docs sites |
| **AFFiNE** | Docs + whiteboard + databases |

### K. Project / Task / Delivery Management
| Software | Role |
|----------|------|
| **Plane** | Modern product/project management |
| **OpenProject** | Program/portfolio + Gantt + wiki |
| **Taiga** | Agile / Scrum |
| **Leantime** | Goal-oriented small teams |
| **Redmine** | Classic issues + wiki + Gantt |
| **Focalboard** (Mattermost) | Kanban boards |
| **Huly** | Project + chat + docs (Linear/Notion/Slack alt) |
| **Odoo Project / ERPNext Project** | Projects inside ERP |

### L. Team Chat / Communication
| Software | Role |
|----------|------|
| **Mattermost** | Slack alternative (enterprise) |
| **Rocket.Chat** | Team chat + customer channels |
| **Zulip** | Threaded team chat |
| **Element (Matrix)** | Decentralized secure chat |
| **Huly** | All-in-one chat + projects + docs |

### M. Customer Support / Helpdesk
| Software | Role |
|----------|------|
| **Chatwoot** | Live chat + omnichannel support |
| **Zammad** | Helpdesk + ticketing |
| **FreeSCOUT** | Lightweight helpdesk |
| **OsTicket** | Classic ticket system |
| AI support drafts via Anthropic CS skills + RAG | Reply assist + escalate |

### N. Email / Newsletter / Forms
| Software | Role |
|----------|------|
| **Listmonk** | Newsletters + campaigns |
| **Postal / Mailcow / docker-mailserver** | Self-hosted mail stack |
| **Formbricks** | Forms / surveys (Typeform alt) |
| **Mautic** | Marketing automation + forms |
| Outbound sequences via **n8n** + approval gates | Sales/email sequences |

### O. Analytics / BI / Reporting
| Software | Role |
|----------|------|
| **Metabase** | Business intelligence / dashboards |
| **Apache Superset** | Advanced BI |
| **Grafana** | Metrics + observability dashboards |
| **Matomo / Plausible / Umami** | Web analytics |
| **PostHog** | Product + session analytics |
| **Lightdash** | dbt-native BI |

### P. Identity / Security / Secrets
| Software | Role |
|----------|------|
| **Keycloak / ZITADEL** | SSO, IAM, RBAC |
| **Vaultwarden** | Password manager (Bitwarden-compatible) |
| **Authelia / Authentik** | Auth gateway |
| **Trilium / structured audit logs** | Audit baseline |

### Q. Finance / Accounting (beyond ERP modules)
| Software | Role |
|----------|------|
| **Odoo Accounting / ERPNext Accounting** | Core books |
| **Akaunting** | Lightweight accounting |
| **Firefly III** | Personal/SMB finance tracking |
| Invoice + payment matching via n8n + agents | Collections workflows |

### R. Sales / Marketing Skills Libraries (reuse)
| Source | Role |
|--------|------|
| **astDeniss/business-skills** | 69 operational playbooks |
| **Autter agentic-sales-skills** | 11 agents + 48 sales skills |
| **TheCraigHewitt/sales-skills** | B2B sales lifecycle |
| **Anthropic knowledge-work-plugins** | Sales, marketing, CS, ops plugins |
| **scayver/marketing-skills** | Marketing skills |
| **gtm-skills/gtm** | GTM OS |
| **GPT Researcher** | Deep research |

### S. Infra / Hosting helpers
| Software | Role |
|----------|------|
| **Coolify / CapRover** | Self-host app platform |
| **PostgreSQL / Redis / MinIO** | Data + cache + object store |
| **Prometheus + Grafana** | Monitoring |
| **OpenMetadata / DataHub** | Data catalog |

### Explicitly deferred (only if FOSS fails evaluation)
Closed SaaS CRMs, closed enrichment APIs, closed social schedulers, closed payroll (India-specific may need hybrid), closed ad platforms — document why FOSS failed + exit plan.

---

## 8. Open-Source Decision Rules

1. **Default = open source.** Check Section 7 first.
2. Prefer **self-hostable** (Nextcloud, n8n, Ollama, Keycloak, Odoo/ERPNext, BookStack/Outline).
3. License: MIT / Apache-2.0 / BSD preferred; AGPL only with isolation.
4. No secrets in Git or prompts.
5. Proprietary only with written FOSS-failure justification + data residency + exit plan.
6. Every adopted tool → Master Asset Registry (source, license, adaptation date).

---

## 9. Recommended Starter FOSS Stack (Nivy)

| Function | Primary FOSS pick |
|----------|-------------------|
| AI runtime | Ollama + Open WebUI + LiteLLM |
| Agents | LangGraph / CrewAI + Hermes/Goose |
| Automation | **n8n** |
| CRM/ERP | **Odoo Community** or **ERPNext** |
| Files / Office | **Nextcloud** + Collabora |
| Wiki / Knowledge | **BookStack** or **Outline** or **Docmost** |
| Calendar / booking | **Cal.com** (self-host) |
| Chat | **Mattermost** or **Rocket.Chat** |
| Support | **Chatwoot** |
| Marketing email | **Listmonk** + **Mautic** |
| Analytics | **Matomo** or **Plausible** + **Metabase** |
| HR | **OrangeHRM** or ERPNext HR |
| Projects | **Plane** or **OpenProject** |
| Identity | **Keycloak** |
| Scrape / research | Crawl4AI + Playwright + GPT Researcher |

---

## 10. Immediate Next Actions

1. Freeze Asset Registry schema.
2. Control plane minimum (approval + audit).
3. P0 agents: AI SDR + Lead Qualification + Concierge (FOSS stack only).
4. Wire Nextcloud + BookStack/Outline as knowledge/storage baseline.
5. n8n as central automation bus.

**Do not** scale to L7–L10 before P0 revenue spine is stable and audited.

---

**Bottom line:**  
Full company = **open-source first**. Sales, marketing, SEO, social, HR, calendar, storage, wiki, projects, chat, support, analytics, finance — sab ke liye FOSS options listed.  
Primary spine: **Ollama + n8n + Odoo/ERPNext + Nextcloud + BookStack/Outline + Keycloak + Chatwoot + Listmonk + Matomo**.  
Khud se banana nahi — FOSS reuse + adapt + govern.
