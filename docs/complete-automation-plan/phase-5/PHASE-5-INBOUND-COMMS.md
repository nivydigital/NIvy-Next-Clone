# Phase 5 — Inbound + Comms workflows

**Status:** 🟢 Implemented (dry-run default)

## Workflows

| ID | Path | Agents |
|----|------|--------|
| inbound-email-triage | `workflows/inbound-email-triage/workflow.yaml` | A066, A052, A068 |
| response-qa | `workflows/response-qa/workflow.yaml` | A068, A071 |
| conversation-intel | `workflows/conversation-intel/workflow.yaml` | A067, A069, A070 |

## Orchestrator

`backend/app/runtime/workflows.py`
- Load `workflow.yaml` by id
- Stage types: agent, context_lookup (stub), gate (approval)
- **dry_run=True by default** — plans agent calls without LLM/side effects
- Audit events: workflow.started, stage.completed, workflow.completed/failed

## API (v0.9.0)

| Method | Path |
|--------|------|
| GET | `/api/v1/runtime/workflows` |
| GET | `/api/v1/runtime/workflows/{id}` |
| POST | `/api/v1/runtime/workflows/{id}/run` |

### Example dry-run

```http
POST /api/v1/runtime/workflows/inbound-email-triage/run
{
  "dry_run": true,
  "payload": {
    "inbound": {
      "message": {"from": "lead@example.com", "subject": "Pricing", "body": "..."},
      "mailbox": "inbox"
    }
  }
}
```

## Mapping to plan

| Plan item | Done |
|-----------|------|
| P5.1 Inbound triage | A066 + A052 + context + draft gate |
| P5.2 Response + QA | A068 + A071 + approval gate |
| P5.3 Conversation/meeting intel | A067 + A069 + A070 |

## Limits

- Live mode calls `execute_agent` (needs prompts/Ollama healthy)
- Context lookup is stub (uses payload.context)
- Gates do not yet integrate full approval store in dry_run skip path
