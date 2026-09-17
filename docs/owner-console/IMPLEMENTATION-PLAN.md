# Owner Console — Implementation Plan

**Version:** 1.0  
**Date:** 2026-09-18  
**Status:** Planned  
**Owner role:** Company owner (single user) only

---

## 1. Purpose

Backend APIs and agents exist, but day-to-day use via curl is too hard for the company owner.

This plan delivers a **simple Owner Console**:

1. See system health and key counts (dashboard)
2. Test agents and workflows from the browser (test lab)
3. Manage leads and approvals without CLI
4. Keep dry-run as the default path until production checklist is signed

**Principle:** Thin UI over existing FastAPI — do not rebuild orchestration in the frontend.

---

## 2. Problem statement

| Today | Pain |
|-------|------|
| `curl` + JSON payloads | High friction for testing |
| `frontend/index.html` | Email form only; no agents/workflows/leads |
| Many agents/workflows | Hard to discover what is runnable |
| Approvals | Easy to miss without a queue screen |

---

## 3. Goals and non-goals

### Goals (MVP)

- Owner can open one app and understand “is the system up?”
- Owner can run **one agent** with a form and see the result
- Owner can run **one workflow** with dry-run toggle and see stage outcome
- Owner can list/create leads and see revenue summary
- Owner can see pending approvals and approve/reject
- Config: API base URL + dry-run default stored in browser (or simple settings)

### Non-goals (MVP)

- Multi-user / RBAC / SSO
- Customer-facing portal
- Full observability stack (Grafana) — cards/tables are enough
- Building new agent logic in the UI
- Auto live-send without approval
- Mobile-native apps

---

## 4. Users and access

| User | Access |
|------|--------|
| Company owner | Full console |
| Others | Out of scope for MVP |

**Auth MVP options (pick one in Phase 0):**

1. **Local gate:** shared password in env (`OWNER_CONSOLE_PASSWORD`) checked by a tiny backend middleware or static page gate
2. **Network trust:** localhost-only bind (dev) — document as temporary only

Prefer (1) before any non-local deploy.

---

## 5. Information architecture (screens)

```text
Owner Console
├── /                 Dashboard (health + counts + recent activity)
├── /test/agents      Agent Test Lab
├── /test/workflows   Workflow Test Lab
├── /leads            Leads list + create + qualify
├── /approvals        Pending approvals queue
└── /settings         API base URL, dry-run default, links to docs
```

### 5.1 Dashboard

**Data sources (existing APIs):**

| Widget | API |
|--------|-----|
| Backend health | `GET /health`, `GET /api/v1/runtime/health` |
| System info | `GET /api/v1/system` |
| Agent count / discovery | `GET /api/v1/runtime/agents` |
| Skill coverage snapshot | `GET /api/v1/runtime/skills/coverage` |
| Workflow list count | `GET /api/v1/runtime/workflows` |
| Revenue summary | `GET /api/v1/revenue/summary` |
| Evaluation snapshot | `GET /api/v1/evaluation/runtime` |

**UI:** status cards (ok / degraded), lead counts by status, links into Test Lab and Approvals.

### 5.2 Agent Test Lab

1. Load agents from `GET /api/v1/runtime/agents`
2. Select agent id (e.g. A034, A001)
3. Optional: show skills via `GET /api/v1/runtime/agents/{id}/skills/resolve`
4. JSON payload editor (or simple fields for A001–A005 where dedicated routes exist)
5. Actions:
   - **Execute** → `POST /api/v1/runtime/agents/{id}/execute`
   - **Run (LLM)** → `POST /api/v1/runtime/agents/{id}/run`
   - Dedicated: A001 research, A002 ICP, … where available
6. Result panel: status, pretty JSON, errors, copy button

**Presets:** 2–3 saved sample payloads for A001, A034, A044 (localStorage).

### 5.3 Workflow Test Lab

1. Load `GET /api/v1/runtime/workflows`
2. Select workflow (lead-outreach, inbound-email-triage, …)
3. Toggle **dry_run** (default true)
4. Optional `stop_after_stage`
5. Payload JSON editor
6. **Run** → `POST /api/v1/runtime/workflows/{id}/run`
7. Result: stage outcomes, errors, next steps

**Safety:** UI must show a clear banner when dry_run is off.

### 5.4 Leads

| Action | API |
|--------|-----|
| List | `GET /api/v1/revenue/leads` |
| Create | `POST /api/v1/revenue/leads` |
| Qualify | `POST /api/v1/revenue/leads/{id}/qualify` |
| Summary | `GET /api/v1/revenue/summary` |
| Audit | `GET /api/v1/revenue/leads/{id}/audit` |

Table + create form + qualify score control.

### 5.5 Approvals

| Action | API |
|--------|-----|
| Request | `POST /api/v1/runtime/approvals` |
| Approve | `POST /api/v1/runtime/approvals/{id}/approve` |
| Email send (after approval) | `POST /api/v1/email/send` with `approval_id` |

MVP: form to request approval + list/approve if backend exposes list; if list is missing, Phase 1 backend adds `GET /api/v1/runtime/approvals` (in-memory is fine).

### 5.6 Settings

- API base URL (default `http://localhost:8000`)
- Dry-run default (boolean)
- Link to `ops/checklists/PRODUCTION-ACTIVATION.md`
- Link to `docs/owner-console/`

---

## 6. Technical approach

### 6.1 Stack recommendation

| Layer | Choice | Why |
|-------|--------|-----|
| App | **Vite + React** (or Next.js if preferred) under `frontend/owner-console/` | Fast SPA, clear separation from stub `index.html` |
| Styling | Simple CSS or Tailwind | Speed |
| Data | `fetch` to FastAPI | No new BFF required for MVP |
| State | React state + localStorage for settings/presets | Enough for single owner |

**Alternative (faster spike):** single enhanced HTML/JS page — acceptable for Phase 1 spike only; Phase 2 should be a real app structure.

### 6.2 Repo layout (target)

```text
frontend/
  index.html                 # keep or redirect to owner-console
  owner-console/
    package.json
    index.html
    src/
      main.tsx
      api/client.ts          # base URL + helpers
      pages/
        Dashboard.tsx
        AgentLab.tsx
        WorkflowLab.tsx
        Leads.tsx
        Approvals.tsx
        Settings.tsx
      components/
        StatusCard.tsx
        JsonViewer.tsx
        DryRunBanner.tsx
```

### 6.3 Backend gaps (small, allowed)

Only if UI is blocked:

| Gap | Suggested API |
|-----|----------------|
| Approvals list | `GET /api/v1/runtime/approvals` |
| CORS | Ensure owner-console origin allowed (already `allow_origins=["*"]` in main) |
| Run history | Optional later: append-only audit query |

Do **not** block MVP on full audit search.

### 6.4 Safety rules in UI

1. Dry-run default **true** for workflows
2. Confirm dialog if dry-run turned **off**
3. Email send always shows approval_id requirement
4. No “send to production” copy until checklist sign-off exists

---

## 7. Phased delivery

### Phase 0 — Scaffold (0.5–1 day)

- Create `frontend/owner-console` app skeleton
- API client with configurable base URL
- Shell layout + nav + Settings page
- Health check on Dashboard

**Exit:** Owner opens UI, sees health ok/fail against running backend.

### Phase 1 — Test Lab (1–2 days)

- Agent list + execute/run + JSON result
- Workflow list + dry-run + run + result
- 3 sample presets (A001, A034, lead-outreach)

**Exit:** Owner can test an agent and a workflow without curl.

### Phase 2 — Leads + Approvals (1–2 days)

- Leads table/create/qualify + summary cards
- Approvals request + approve (+ list if API added)
- Wire email send path with approval_id from UI

**Exit:** Owner can create a lead and complete an approval click-path.

### Phase 3 — Dashboard polish + harden (1 day)

- Evaluation/runtime cards
- Skill coverage summary
- Empty/error states, loading, toast errors
- Basic owner password gate (if not done in Phase 0)
- README run instructions

**Exit:** Demo-ready for owner daily use.

### Phase 4 — Optional later

- Run history / audit browser
- Grafana embeds from `ops/observability/dashboard-spec.yaml`
- Multi-user roles
- Production deploy (auth required)

---

## 8. API map (canonical)

| Area | Methods |
|------|---------|
| Health | `GET /health`, `GET /api/v1/runtime/health`, `GET /api/v1/system` |
| Agents | `GET/POST .../runtime/agents`, `.../execute`, `.../run`, dedicated A001–A005 |
| Skills | `GET .../skills/coverage`, `GET .../agents/{id}/skills/resolve` |
| Workflows | `GET .../workflows`, `GET .../workflows/{id}`, `POST .../workflows/{id}/run` |
| Revenue | `GET/POST .../revenue/leads`, qualify, summary, audit |
| Approvals / email | `POST .../approvals`, approve, `POST .../email/send` |
| Eval | `GET /api/v1/evaluation/runtime` |

---

## 9. Definition of done (Owner Console MVP)

1. All Phase 0–3 exit criteria met
2. Documented start commands in this folder’s README or main README link
3. Dry-run default enforced in Workflow Lab
4. No secrets committed; API URL local by default
5. Progress tracker updated to 🟢 for MVP items
6. Owner can complete: health check → agent test → workflow dry-run → lead create → approval path

---

## 10. Risks

| Risk | Mitigation |
|------|------------|
| Backend not running | Dashboard shows clear offline state |
| LLM/Ollama down | Show tool/agent error text; still allow list endpoints |
| Payload complexity | Presets + raw JSON editor |
| Accidental live send | Dry-run default + confirm + approval required |
| Scope creep | Stick to owner-only MVP screens |

---

## 11. Tracking

| Artifact | Path |
|----------|------|
| This plan | `docs/owner-console/IMPLEMENTATION-PLAN.md` |
| Progress | `docs/owner-console/PROGRESS-TRACKER.md` |
| Code target | `frontend/owner-console/` |

---

## 12. First actions

1. Scaffold `frontend/owner-console` (Phase 0)
2. Wire health + agents list
3. Agent execute form + result viewer
4. Workflow dry-run runner
5. Update PROGRESS-TRACKER as each item ships

---

*End of Owner Console Implementation Plan v1.0*
