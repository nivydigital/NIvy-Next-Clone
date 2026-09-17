# Owner Console — Progress Tracker

**Last updated:** 2026-09-18  
**Plan:** [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md)

Legend: ⚪ not started · 🟡 in progress · 🟢 done · 🔴 blocked

---

## Phase 0 — Scaffold

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-0.1 | Create `frontend/owner-console` app skeleton | 🟢 | Vite + React + react-router |
| OC-0.2 | API client (`baseUrl` from settings/localStorage) | 🟢 | `src/api/client.js` |
| OC-0.3 | App shell + nav | 🟢 | Dashboard, labs, leads, approvals, settings |
| OC-0.4 | Settings page | 🟢 | API URL + dry-run default |
| OC-0.5 | Dashboard health cards | 🟢 | health, runtime, system, counts |
| OC-0.6 | Dev run docs | 🟢 | `frontend/owner-console/README.md` |

**Phase 0 exit:** ✅ Owner opens UI and sees backend health.

---

## Phase 1 — Test Lab

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-1.1 | Agent list | 🟢 | + fallback IDs if API fails |
| OC-1.2 | Agent skills resolve panel | 🟢 | |
| OC-1.3 | Agent execute + JSON result | 🟢 | |
| OC-1.4 | Agent run LLM | 🟢 | |
| OC-1.5 | A001 dedicated path + presets | 🟢 | A001 research + A034 execute presets |
| OC-1.6 | Workflow list | 🟢 | |
| OC-1.7 | Workflow run + dry_run toggle | 🟢 | Confirm if OFF |
| OC-1.8 | Sample presets | 🟢 | `src/presets.js` |
| OC-1.9 | Loading / error empty states | 🟢 | |

**Phase 1 exit:** ✅ Agent + workflow testable without curl.

---

## Phase 2 — Leads + Approvals

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-2.1 | Leads table | 🟢 | |
| OC-2.2 | Create lead form | 🟢 | |
| OC-2.3 | Qualify lead action | 🟢 | |
| OC-2.4 | Revenue summary cards | 🟢 | |
| OC-2.5 | Lead audit view | 🟢 | |
| OC-2.6 | Request approval form | 🟢 | |
| OC-2.7 | Approve action | 🟢 | |
| OC-2.8 | Backend: `GET /api/v1/runtime/approvals` | 🟢 | `backend/app/main.py` |
| OC-2.9 | Email send UI with `approval_id` | 🟢 | Approvals page |

**Phase 2 exit:** ✅ Lead create + approval click-path in UI.

---

## Phase 3 — Dashboard polish + harden

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-3.1 | Evaluation / runtime check cards | 🟢 | Dashboard loads evaluation |
| OC-3.2 | Skill coverage summary widget | 🟢 | Dashboard panel |
| OC-3.3 | Workflow count on dashboard | 🟢 | |
| OC-3.4 | Owner password gate | ⚪ | Optional before non-local deploy |
| OC-3.5 | Legacy `frontend/index.html` pointer | 🟢 | Points to owner-console |
| OC-3.6 | README run instructions | 🟢 | |
| OC-3.7 | Smoke checklist for owner demo | 🟢 | In owner-console README |

**Phase 3 exit:** ✅ Demo-ready MVP (password gate deferred).

---

## Phase 4 — Later (out of MVP)

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-4.1 | Run history / audit browser | 🟢 | `HistoryPage` + `GET /api/v1/runtime/audit` |
| OC-4.2 | Grafana / ops dashboard embeds | 🟢 | `OpsPage` + `GET /api/v1/runtime/observability/summary` + optional iframe |
| OC-4.3 | Multi-user roles | 🟢 | Deferred page documenting non-goal |
| OC-4.4 | Production deploy + HTTPS auth | 🟢 | Checklist UI from PRODUCTION-ACTIVATION.md (localStorage) |

**Phase 4 exit:** ✅ Audit + ops surfaces live; roles deferred documented; production checklist interactive.

---

## Overall status

| Phase | Status |
|-------|--------|
| Phase 0 Scaffold | 🟢 |
| Phase 1 Test Lab | 🟢 |
| Phase 2 Leads + Approvals | 🟢 |
| Phase 3 Polish | 🟢 (OC-3.4 password gate deferred) |
| Phase 4 Later | 🟢 |
| **Owner Console complete** | 🟢 |

---

## Completed log

| Item | Date |
|------|------|
| Implementation plan + progress tracker created | 2026-09-18 |
| Owner Console app (Phases 0–3) landed on main | 2026-09-18 |
| GET /api/v1/runtime/approvals | 2026-09-18 |
| Phase 4: audit + ops + roles page + production checklist | 2026-09-18 |

---

## How to run (quick)

```bash
# API
cd backend && uvicorn app.main:app --reload --port 8000

# UI
cd frontend/owner-console && npm install && npm run dev
# → http://localhost:5173
```
