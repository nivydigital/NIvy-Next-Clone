# Phase 6–7 Verification

## Phase 6 — Revenue Agent Factory

Implemented repository contract:
- `runtime/revenue-agent-factory.yaml`
- seeded revenue agents are declared in `agents/registry.yaml`
- activation is gated by registry binding, policy, evaluation evidence and integration health
- autonomous activation remains disabled by default

## Phase 7 — Revenue Workflows & State Machines

Implemented repository contract:
- `runtime/revenue-state-machine.yaml`
- canonical states: new → qualified → proposal → won/lost
- undefined transitions are rejected
- protected transitions require approval
- n8n is the workflow engine and Odoo is the system of record
- idempotency key is `lead_id:event`

## Automated checks

`backend/tests/test_revenue_state_machine.py` validates the contracts.

## Evidence limitation

These phases are **implemented but not VERIFIED** until the test suite runs successfully and live n8n/Odoo workflow execution is demonstrated in the user's environment. Repository declarations do not count as live integration evidence.
