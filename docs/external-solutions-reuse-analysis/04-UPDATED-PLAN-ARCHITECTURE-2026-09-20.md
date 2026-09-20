# Updated Plan & Architecture — Full Company FOSS Stack

**Source library:** https://github.com/nivyindia/Raw-Repository/tree/main/external-solutions/business-structure-planning-ai-library  
**Updated:** 2026-09-20  
**Core rule:** `DISCOVER → DECOMPOSE → REUSE → ADAPT → INTEGRATE → BUILD ONLY WHAT IS MISSING`  
**Software policy:** **100% open-source first.** Proprietary only if FOSS fails evaluation.

---

## Target Architecture

```
ONE NIVY WORKSPACE (role-aware UI)
        ↓
CONTROL PLANE (Identity · Policy · Router · Approval · Audit · Kill Switch)
        ↓
Agents (Intake · Specialist · Managers · Executives)
        ↓
n8n + MCP + Tools (scrape, enrich, CRM, calendar, RAG, voice, browser)
        ↓
Systems of Record + Knowledge + Storage + Memory
```

---

## COMPLETE FOSS SOFTWARE MAP — Micro Work → Major Company → Client Delivery

### 1. MICRO TASKS (L0–L1) — Daily atomic work

| Micro work | FOSS software |
|------------|---------------|
| Email classify / draft / follow-up | n8n + LLM (Ollama) + mail stack |
| Calendar schedule / remind | Cal.com, Nextcloud Calendar, Xandikos |
| Chat classify / route / task | Mattermost / Rocket.Chat + n8n |
| Voice transcribe / intent | Whisper + LiveKit / Pipecat |
| Document rename / OCR / extract | Nextcloud + Tesseract + agents |
| File dedupe / version / archive | Nextcloud, Seafile |
| Form submit → CRM | Formbricks + n8n |
| Notification / escalate | n8n + Mattermost |
| Data entry / clean / merge | n8n + PostgreSQL + agents |
| Contact enrich / dedupe | n8n + enrichment MCP / scrape |
| Task from email/message | n8n + Plane / OpenProject |
| Approval request / remind | n8n + Keycloak roles |
| Report collect / format | Metabase + n8n |
| Meeting transcript → tasks | Whisper + agents + n8n |
| Search multi-source | Onyx / RAGFlow + GPT Researcher |
| Knowledge capture / chunk | BookStack / Outline + LlamaIndex |
| Translate | LibreTranslate + agents |
| Template fill (proposal/invoice) | n8n + Odoo/ERPNext templates |
| Browser extract / fill | Playwright, Browser Use, Skyvern |
| Media resize / caption / transcribe | FFmpeg + Whisper + agents |

### 2. SALES & REVENUE (client acquisition)

| Work | FOSS |
|------|------|
| CRM / pipeline | **Odoo Community**, **ERPNext**, Twenty, EspoCRM, SuiteCRM, Dolibarr |
| Lead gen / research | GPT Researcher, Crawl4AI, Firecrawl, Hermes lead-gen, Apify skills |
| Enrichment | Open enrichment MCP + scrape |
| Outreach sequences | n8n + Listmonk + approval gates |
| Proposal / quote | Odoo/ERPNext + agent skills |
| Booking meetings | **Cal.com** |
| Sales skills | astDeniss, Autter agentic-sales-skills, Anthropic Sales plugin |

### 3. MARKETING / DIGITAL / SEO / SOCIAL

| Work | FOSS |
|------|------|
| Email campaigns | **Listmonk**, **Mautic** |
| Marketing automation | Mautic |
| Web analytics | **Matomo**, Plausible, Umami |
| Product analytics | PostHog |
| Blog / content CMS | Ghost, Strapi, Payload, Directus |
| SEO / content strategy | astDeniss SEO skills + Anthropic marketing plugins |
| Social scheduling / monitoring | n8n + Chatwoot + browser agents |
| Design | **Penpot** (Figma alt), Excalidraw |
| Public docs site | Docusaurus |

### 4. CLIENT DELIVERY / PROJECTS / SERVICES

| Work | FOSS |
|------|------|
| Project / task management | **Plane**, OpenProject, Taiga, Leantime, Redmine, Huly |
| Time tracking | OpenProject, ERPNext, Leantime |
| Client portal | Odoo/ERPNext portal, Chatwoot, Nextcloud share |
| SOPs / runbooks | BookStack / Outline + agents |
| Delivery handoff | n8n workflows (won deal → project → invoice) |
| QA / checklist | n8n + wiki |

### 5. CUSTOMER SUCCESS / SUPPORT

| Work | FOSS |
|------|------|
| Live chat / omnichannel | **Chatwoot** |
| Helpdesk / tickets | **Zammad**, FreeSCOUT, osTicket |
| Knowledge for support | BookStack + RAG (AnythingLLM / RAGFlow) |
| SLA / escalation | n8n + Zammad |
| Feedback / NPS | Formbricks |

### 6. FINANCE / BILLING / ACCOUNTING

| Work | FOSS |
|------|------|
| Full accounting | **Odoo Accounting**, **ERPNext Accounting** |
| Invoicing | Odoo, ERPNext, Invoice Ninja, Akaunting, Crater |
| Usage billing / metering | **Lago** (Stripe Billing alt) |
| Expenses / books (light) | Akaunting, Firefly III |
| Bank reconcile / collections | n8n + agents + ERP |
| Multi-currency / tax | Odoo / ERPNext localization |

### 7. INVENTORY / PROCUREMENT / MANUFACTURING / POS

| Work | FOSS |
|------|------|
| Inventory / warehouse | **Odoo**, **ERPNext**, Dolibarr |
| Purchase / RFQ / PO | Odoo, ERPNext, Dolibarr |
| Manufacturing / BOM / MRP | Odoo MRP, ERPNext Manufacturing |
| Point of Sale | Odoo POS, ERPNext POS, Dolibarr |
| Asset management | Snipe-IT |

### 8. HR / EMPLOYEES / LEARNING

| Work | FOSS |
|------|------|
| HRIS core | **OrangeHRM**, IceHrm, Odoo HR, ERPNext HR, Open HRMS |
| Attendance / payroll | TimeTrex Community, ERPNext Payroll |
| Appraisals / ESS | Sentrifugo, OrangeHRM |
| Recruitment pipeline | n8n + agents + CRM |
| Onboarding / offboarding | n8n + wiki checklists |
| LMS / training | Moodle, Open edX, Frappe LMS |
| Password / secrets for staff | **Vaultwarden**, Passbolt |

### 9. KNOWLEDGE / STORAGE / DOCS / WIKI

| Work | FOSS |
|------|------|
| File sync / Drive alt | **Nextcloud** |
| Object storage | **MinIO** |
| Office collaborative edit | Collabora Online, OnlyOffice |
| Internal wiki | **BookStack**, **Outline**, Docmost, Wiki.js |
| Encrypted collab docs | CryptPad |
| Notes / whiteboard | AFFiNE, HedgeDoc, Excalidraw |
| Personal knowledge | TriliumNext |

### 10. CALENDAR / COMMUNICATION / MEETINGS

| Work | FOSS |
|------|------|
| Booking / scheduling | **Cal.com** |
| Team calendar | Nextcloud Calendar |
| Team chat | **Mattermost**, Rocket.Chat, Zulip, Element |
| Video meetings | **Jitsi** |
| Email server | Mailcow, docker-mailserver, Postal |

### 11. IDENTITY / SECURITY / IT OPS

| Work | FOSS |
|------|------|
| SSO / IAM | **Keycloak**, ZITADEL, Authentik |
| Password manager | Vaultwarden, Passbolt |
| VPN | WireGuard, Headscale |
| Remote desktop | RustDesk |
| Monitoring | Prometheus + Grafana, Uptime Kuma |
| Logs / SIEM light | Grafana Loki |
| Backup | Restic, BorgBackup |
| Git hosting | Gitea, Forgejo |
| App hosting platform | Coolify, CapRover |

### 12. ANALYTICS / BI / REPORTING

| Work | FOSS |
|------|------|
| Business dashboards | **Metabase**, Apache Superset |
| Web analytics | Matomo, Plausible, Umami |
| Product analytics | PostHog |
| Infra metrics | Grafana |

### 13. LEGAL / COMPLIANCE / GOVERNANCE (light)

| Work | FOSS |
|------|------|
| Contract templates / clause extract | Agents + wiki + n8n |
| Policy / evidence store | BookStack + Nextcloud + audit logs |
| GRC light | security-atlas patterns (from library registry) |
| Consent / forms | Formbricks |

### 14. E-COMMERCE / WEBSITE (if needed)

| Work | FOSS |
|------|------|
| Storefront | Odoo eCommerce, ERPNext, Saleor, Medusa |
| Website builder | Odoo Website, Ghost |
| CMS | Strapi, Payload, Directus |

### 15. DESIGN / CREATIVE / MEDIA

| Work | FOSS |
|------|------|
| UI design | **Penpot** |
| Whiteboard | Excalidraw |
| Image gen workflows | ComfyUI |
| Video / audio process | FFmpeg, Whisper, Coqui TTS |
| OpenVoice | Voice cloning research |

### 16. AI / AGENTS / AUTOMATION CORE

| Work | FOSS |
|------|------|
| LLM runtime | **Ollama**, llama.cpp, vLLM |
| AI UI | Open WebUI, AnythingLLM |
| Gateway | LiteLLM |
| Orchestration | LangGraph, CrewAI, AutoGen |
| Digital workers | Hermes, Goose, OpenClaw, Agent Zero, OpenHands |
| Memory | Mem0, Zep, Graphiti, Letta |
| RAG | LlamaIndex, Haystack, RAGFlow, Onyx |
| Automation bus | **n8n** |
| Browser agents | Browser Use, Skyvern, Playwright |

---

## Recommended Nivy Starter Stack (priority install)

| Layer | Pick |
|-------|------|
| AI | Ollama + Open WebUI + LiteLLM + LangGraph/CrewAI |
| Automation | **n8n** |
| Business core | **Odoo Community** *or* **ERPNext** |
| Files | **Nextcloud** + Collabora |
| Wiki | **BookStack** or **Outline** |
| Chat | **Mattermost** or **Rocket.Chat** |
| Support | **Chatwoot** |
| Booking | **Cal.com** |
| Marketing email | **Listmonk** + **Mautic** |
| Analytics | **Matomo** + **Metabase** |
| Identity | **Keycloak** |
| Passwords | **Vaultwarden** |
| Projects | **Plane** or OpenProject |
| HR | OrangeHRM or ERPNext HR |
| Monitoring | Uptime Kuma + Grafana |
| Object storage | MinIO |
| Scrape/research | Crawl4AI + Playwright + GPT Researcher |

---

## Decision Rules

1. Always check this list before adding software.
2. Prefer self-hosted FOSS.
3. One system of record per business object.
4. External messages + payments = human approval.
5. License: MIT/Apache/BSD preferred; AGPL with isolation.
6. Register every adopted tool in Asset Registry.

---

## Delivery Order

1. Foundation (registry + control plane)  
2. P0 revenue agents (SDR, Qualify, Concierge) on FOSS stack  
3. Nextcloud + wiki + n8n  
4. Odoo or ERPNext as system of record  
5. Chatwoot + Cal.com + Listmonk  
6. HR + projects + analytics  
7. Inventory/POS/manufacturing only if business needs them  

**Bottom line:** Micro task se leke client delivery, inventory, POS, manufacturing, procurement, billing, LMS, design, IT, backup — sab ke liye FOSS options mapped. Proprietary tabhi jab is list se kaam na chale.
