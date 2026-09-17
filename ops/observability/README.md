# Observability (Phase 10 / P10.3)

| Signal | Source |
|--------|--------|
| Audit events | `backend.app.runtime.audit` |
| Workflow transitions | lead-outreach orchestrator |
| Tool errors | tool.execution status=error |

See `dashboard-spec.yaml`. Use `backend.app.runtime.observability.audit_summary()` for MVP metrics.
