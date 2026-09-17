# Nivy Owner Console

Company-owner UI for health, agent/workflow testing, leads, and approvals.

## Prerequisites

1. Backend running on `http://localhost:8000`
2. Node.js 18+ (for Vite)

```bash
# terminal 1 — API
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# terminal 2 — UI
cd frontend/owner-console
npm install
npm run dev
```

Open **http://localhost:5173**

## Pages

| Route | Purpose |
|-------|---------|
| `/` | Dashboard — health, counts, eval snapshot |
| `/test/agents` | Agent Test Lab — execute / LLM / presets |
| `/test/workflows` | Workflow Lab — dry-run default ON |
| `/leads` | Create / list / qualify leads |
| `/approvals` | Request / approve / gated email send |
| `/settings` | API base URL + dry-run default |

## Safety

- Workflow **dry-run** defaults to ON (Settings + Workflow Lab)
- Turning dry-run OFF asks for confirmation
- Email send requires `approval_id`

## Docs

- Plan: `docs/owner-console/IMPLEMENTATION-PLAN.md`
- Tracker: `docs/owner-console/PROGRESS-TRACKER.md`

## Smoke checklist (owner demo)

1. Dashboard shows backend **ok**
2. Agent Lab → load A034 preset → Execute (or A001 research)
3. Workflow Lab → lead-outreach → dry-run Run
4. Leads → create one lead → refresh list
5. Approvals → request → approve → (optional) email with approval_id
