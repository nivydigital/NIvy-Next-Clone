# Deferred Testing Plan for All Agents

**Status:** Active policy override (user direction 2026-09-17)
**Rule:** Full automated testing, evaluation suites, live integration evidence and G16/G17 gates are **deferred** until the final testing phase for the entire agent set.

## Policy

- Implementation of agents continues without requiring passing unit/integration/evaluation tests for each agent.
- Every agent still receives:
  - Complete `agent.yaml` specification
  - Input / output JSON schemas
  - Runtime adapter (`backend/app/runtime/a0XX.py`)
  - Minimal contract check (schema presence) if useful
  - Registry / binding updates
- **No agent is marked COMPLETE or ACTIVE** until the final testing phase is executed.
- The final testing phase will apply the full G0–G20 gates, the AGENT-BUILD-MASTER-PROMPT testing pyramid, and live evidence requirements.

## How testing will be performed (later)

For **every** agent (A001 onward) the final testing phase will execute:

1. **Contract / registry tests**
   - All referenced skill, prompt, knowledge, tool IDs resolve.
   - Input and output schemas validate.
   - Agent appears correctly in `agents/registry.yaml` and `implementation-registry.yaml`.

2. **Unit / happy-path tests**
   - Deterministic cases with controlled LLM mocks or local Ollama.
   - Valid input produces schema-compliant output.
   - Required fields and confidence values are present.

3. **Negative / policy tests**
   - Missing required inputs → fail closed.
   - Invalid / malformed input → rejected.
   - Missing provenance / evidence → rejected.
   - Unauthorized tool or side-effect → denied.
   - Prompt-injection style payloads → blocked or sanitized.

4. **Output & schema tests**
   - Strict JSON schema validation.
   - Required fields, types, confidence enum, evidence arrays.

5. **Evaluation suite**
   - Golden / representative cases (minimum 3–5 per agent).
   - Metrics: schema pass rate, evidence coverage, confidence calibration, policy compliance.
   - Acceptance threshold recorded (default 100% critical gates).

6. **Integration / live proof (where applicable)**
   - Runtime endpoint callable.
   - n8n workflow (if present) can trigger the agent.
   - Local Ollama + any declared research adapters produce real runs.
   - Audit / correlation IDs emitted.

7. **Regression**
   - Full suite re-run after any shared runtime, engine, or skill change.

## Evidence location (final phase)

- Test files: `backend/tests/test_a0XX_*.py`
- Evaluation results: recorded in each agent’s completion record and in `docs/agent-implementation-plan/AGENT-PROGRESS-TRACKER.md`
- CI: `.github/workflows/runtime-tests.yml` (and any agent-specific workflows)
- Live evidence: screenshots / logs / n8n execution IDs stored under `docs/verification/` or agent completion records

## Current agent implementation order (continuing)

A001 → A002 → A003 → A004 → A005 → **A006 (next)** → …

Testing remains deferred for all of the above until the explicit final testing phase is started.

## Change log

| Date       | Change                                      | By          |
|------------|---------------------------------------------|-------------|
| 2026-09-17 | Created deferred testing policy             | User + Grok |
