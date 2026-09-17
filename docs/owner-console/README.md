# Owner Console (UI)

**Created:** 2026-09-18  
**Audience:** Company owner only (single-operator)  
**Goal:** Make AIOS usable without curl — dashboard + test lab + approvals + leads

| Document | Purpose |
|----------|---------|
| [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md) | Full plan: scope, screens, APIs, phases, exit criteria |
| [PROGRESS-TRACKER.md](./PROGRESS-TRACKER.md) | Ordered backlog and status (update as work lands) |

**Related backend:** FastAPI `backend/app/main.py`  
**Related ops:** `ops/observability/dashboard-spec.yaml`, `ops/checklists/PRODUCTION-ACTIVATION.md`  
**Current frontend:** `frontend/index.html` (email-only stub — replace/extend)

**Rule:** Dry-run default ON. Live side effects only after approval flow works in UI.
