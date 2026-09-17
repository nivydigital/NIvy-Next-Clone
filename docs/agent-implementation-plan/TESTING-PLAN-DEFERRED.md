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
2. **Unit / happy-path tests**
3. **Negative / policy tests**
4. **Output & schema tests**
5. **Evaluation suite**
6. **Integration / live proof**
7. **Regression**

---

## Agent-specific deferred tests — A117–A127 (pushed 2026-09-17)

Full G16–G20 deferred until final testing phase.

For each of A117–A127:
1. Contract/registry: skill/prompt/knowledge IDs resolve; input/output schemas validate.
2. Unit happy-path: valid required inputs → schema-compliant JSON with confidence in {high,medium,low}.
3. Negative: missing required inputs → agent-specific Error; non-JSON model output → fail closed.
4. Policy: only tool.ollama.generate; side_effects false; no activation/publish/deploy/cross-tenant writes.
5. Golden cases: minimum 3 representative scenarios per agent.
6. Integration: runtime entrypoint callable with local Ollama when credentials available.

Do not mark COMPLETE until final testing phase.
