# Nivy Next AIOS — Definition of Done

A phase is **not complete** merely because its files exist or the container starts.

## Required gates for every phase

1. **Implementation** — required code/configuration is committed.
2. **Integration** — it connects to the real Nivy services where applicable.
3. **Validation** — inputs and outputs have explicit schemas.
4. **Error handling** — expected failures have deterministic behavior.
5. **Persistence** — state is durable when the phase requires state.
6. **Security** — secrets are externalized and permissions are enforced.
7. **Observability** — logs/status/audit data exist where appropriate.
8. **Tests** — unit/integration/e2e tests required by the phase pass.
9. **Documentation** — setup, configuration and operating behavior are documented.
10. **Acceptance test** — the phase's exit condition in `IMPLEMENTATION-PLAN.md` passes.

## Release gates

Before declaring the whole platform complete:

- All critical phases are green.
- No known critical security issue remains.
- No required secret is stored in Git.
- Docker Compose starts cleanly with documented configuration.
- Database migration and backup/restore have been tested.
- Agent/tool permissions and external side effects are audited.
- Regression suite passes.
- At least one complete lead/outreach lifecycle passes in a controlled test environment.
- At least one document/RAG lifecycle passes.
- At least one content/social lifecycle passes where provider credentials are available.
- Failure/retry/restart behavior has been tested.

## Status vocabulary

- 🟢 Complete: implementation + tests + acceptance verified.
- 🟡 In progress: active implementation.
- 🔴 Blocked: cannot proceed without a documented dependency.
- ⚪ Not started.

## Important rule

Provider credentials are dependencies, not reasons to fake success. If Gmail, Outlook, Apify, a publishing API, or another external service is unavailable, record the phase as blocked at the external-integration subtask while completing all provider-independent code and tests.
