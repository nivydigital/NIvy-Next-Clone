# Revenue Engine v1

The first production-oriented Revenue Engine boundary is now available under `/api/v1/revenue`.

## Current capabilities

- Lead intake with source attribution.
- Deterministic qualification score from 0-100.
- Status transitions: `new` -> `qualified` -> `proposal`.
- Explicit proposal approval gate before a proposal can be marked ready to send.
- Summary endpoint for operational dashboards.

## Protected side effects

This layer does **not** send email, write to a CRM, or publish external messages. Those actions must remain behind a separate human approval and integration boundary. The approval endpoint only records an internal approval state and changes the lead next action to `send_proposal`.

## Endpoints

- `POST /api/v1/revenue/leads`
- `GET /api/v1/revenue/leads`
- `POST /api/v1/revenue/leads/{lead_id}/qualify`
- `POST /api/v1/revenue/leads/{lead_id}/proposal/request`
- `POST /api/v1/revenue/leads/{lead_id}/proposal/approve`
- `GET /api/v1/revenue/summary`

## Current limitation

The engine uses an in-process store for deterministic v1 smoke testing. Before multi-worker production deployment, replace it with the existing PostgreSQL service and add idempotency keys, audit events, and role-based approval identity.
