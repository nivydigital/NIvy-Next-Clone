# Owner Console — Progress Tracker

**Last updated:** 2026-09-18  
**Plan:** [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md)

Legend: ⚪ not started · 🟡 in progress · 🟢 done · 🔴 blocked

---

## Phase 0 — Scaffold

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-0.1 | Create `frontend/owner-console` app skeleton | ⚪ | Vite+React (or agreed stack) |
| OC-0.2 | API client (`baseUrl` from settings/localStorage) | ⚪ | Default `http://localhost:8000` |
| OC-0.3 | App shell + nav (Dashboard, Test, Leads, Approvals, Settings) | ⚪ | |
| OC-0.4 | Settings page (API URL, dry-run default) | ⚪ | |
| OC-0.5 | Dashboard health cards (`/health`, `/runtime/health`, `/system`) | ⚪ | |
| OC-0.6 | Dev run docs (how to start backend + UI) | ⚪ | |

**Phase 0 exit:** Owner opens UI and sees backend health.

---

## Phase 1 — Test Lab

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-1.1 | Agent list from `GET /api/v1/runtime/agents` | ⚪ | |
| OC-1.2 | Agent skills resolve panel | ⚪ | Optional but useful |
| OC-1.3 | Agent execute (`POST .../execute`) + JSON result | ⚪ | |
| OC-1.4 | Agent run LLM (`POST .../run`) | ⚪ | |
| OC-1.5 | Dedicated A001–A005 forms (or deep-link presets) | ⚪ | Can start with A001 only |
| OC-1.6 | Workflow list from `GET .../workflows` | ⚪ | |
| OC-1.7 | Workflow run with dry_run toggle (default ON) | ⚪ | Confirm if OFF |
| OC-1.8 | Sample presets (A001, A034, lead-outreach) | ⚪ | localStorage |
| OC-1.9 | Loading / error empty states for Test Lab | ⚪ | |

**Phase 1 exit:** Agent + workflow testable without curl.

---

## Phase 2 — Leads + Approvals

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-2.1 | Leads table (`GET .../revenue/leads`) | ⚪ | |
| OC-2.2 | Create lead form | ⚪ | |
| OC-2.3 | Qualify lead action | ⚪ | |
| OC-2.4 | Revenue summary cards | ⚪ | |
| OC-2.5 | Lead audit view (optional) | ⚪ | |
| OC-2.6 | Request approval form | ⚪ | |
| OC-2.7 | Approve action | ⚪ | |
| OC-2.8 | Backend: `GET /api/v1/runtime/approvals` if missing | ⚪ | Only if needed |
| OC-2.9 | Email send UI with `approval_id` | ⚪ | Keep gated |

**Phase 2 exit:** Lead create + approval click-path works.

---

## Phase 3 — Dashboard polish + harden

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-3.1 | Evaluation / runtime check cards | ⚪ | `GET /api/v1/evaluation/runtime` |
| OC-3.2 | Skill coverage summary widget | ⚪ | |
| OC-3.3 | Workflow count / list shortcut on dashboard | ⚪ | |
| OC-3.4 | Owner password gate (env-based) | ⚪ | Before non-local use |
| OC-3.5 | Replace or redirect legacy `frontend/index.html` | ⚪ | Link to console |
| OC-3.6 | README link from repo root or docs index | ⚪ | |
| OC-3.7 | Smoke checklist for owner demo | ⚪ | 5-step path |

**Phase 3 exit:** Demo-ready MVP.

---

## Phase 4 — Later (out of MVP)

| ID | Item | Status | Notes |
|----|------|--------|-------|
| OC-4.1 | Run history / audit browser | ⚪ | |
| OC-4.2 | Grafana / ops dashboard embeds | ⚪ | See `ops/observability/` |
| OC-4.3 | Multi-user roles | ⚪ | |
| OC-4.4 | Production deploy + HTTPS auth | ⚪ | After activation checklist |

---

## Overall status

| Phase | Status |
|-------|--------|
| Phase 0 Scaffold | ⚪ |
| Phase 1 Test Lab | ⚪ |
| Phase 2 Leads + Approvals | ⚪ |
| Phase 3 Polish | ⚪ |
| Phase 4 Later | ⚪ |
| **MVP complete** | ⚪ |

---

## Completed log

| Item | Date |
|------|------|
| Implementation plan + progress tracker created | 2026-09-18 |

---

## How to update this file

1. When work starts → set 🟡 and note branch/PR
2. When merged and manually verified → 🟢
3. If blocked on backend → 🔴 + note gap
4. Bump **Last updated** date
