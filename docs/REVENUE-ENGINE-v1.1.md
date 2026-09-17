# Revenue Engine v1.1

## What changed

The Revenue Engine now uses a portable SQLite store instead of process memory. This keeps local/Docker portability while allowing state to survive API restarts. The database path is controlled by `NIVY_REVENUE_DB_PATH` and defaults to `data/revenue.db`.

The engine also provides:

- idempotent lead creation with `request_id`
- approval actor tracking for proposal approval
- append-only audit events for lead lifecycle changes
- deterministic qualification behavior and explicit approval boundaries
- no outbound CRM, email, or messaging side effect from the core engine

## API additions

- `POST /api/v1/revenue/leads` accepts `request_id` and `actor`.
- `GET /api/v1/revenue/leads/{lead_id}/audit` returns lifecycle audit events.
- `GET /api/v1/system` reports the Revenue persistence mode.

## Safety boundary

Proposal approval changes state only after an explicit human approval endpoint call. It does not send a proposal or write to an external CRM. External side effects remain behind the governed runtime approval mechanism.

## Production follow-up

The next persistence hardening step is to introduce a PostgreSQL adapter behind the same repository interface, then add migration/versioning and role-backed approval identity. SQLite remains the default portable implementation for local and CI use.
