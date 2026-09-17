# NIVY NEXT AIOS — MASTER AGENT IMPLEMENTATION PLAN

**Version:** 1.0
**Status:** Canonical agent-by-agent execution plan
**Scope:** All canonical agents currently declared in `agents/registry.yaml`
**Primary rule:** finish and verify one agent before starting the next.

## 1. Objective

Transform the current agent registry from declarations/bindings into a set of genuinely executable, governed, testable and observable agents. The target is not merely a large number of YAML records. Each agent must be capable of performing its assigned business work within explicit boundaries and must prove that it can do so.

## 2. Non-negotiable engineering principles

1. **One agent at a time.** The next agent does not start until the current agent passes all required completion gates.
2. **Reuse before build.** Search Raw-Repository first and search approved internet/open-source sources before implementing anything new.
3. **No weak imitation.** Do not copy an attractive-looking agent blindly. Audit its actual implementation, dependencies, license, security, quality and integration fit.
4. **Adapt to canonical AIOS.** Reused components must fit the canonical Odoo/PostgreSQL/Qdrant/MinIO/n8n/runtime architecture and governance model unless an explicit exception is approved.
5. **Fail closed.** Missing or ambiguous capabilities, permissions, schemas, prompts, tools or policies block execution.
6. **Evidence over declarations.** A file existing in GitHub is not proof that an agent works.
7. **Least privilege.** An agent receives only the tools, data, memory and side-effect permissions necessary for its job.
8. **Protected side effects require approval.** Sending external communications, changing CRM/business records, financial actions or other protected effects must pass runtime policy.
9. **Authoritative systems are explicit.** Every read/write must identify its source of truth and postcondition check.
10. **Reusable capabilities are first-class.** When a missing behavior is useful to multiple agents, implement it as a governed skill/tool/workflow rather than duplicating agent-specific code.
11. **No autonomous activation by default.** Autonomous operation requires separate policy, evaluation, integration-health and observability evidence.
12. **Never mark VERIFIED without runtime evidence.** Local unit tests and live integration tests are distinct evidence classes.

## 3. Canonical agent lifecycle

`DISCOVER → AUDIT → REUSE → ADAPT → SPECIFY → BIND → IMPLEMENT → UNIT TEST → INTEGRATION TEST → POSTCONDITION VERIFY → OBSERVE/AUDIT → EVALUATE → DOCUMENT → ACTIVATE`

If a stage fails, repair the current agent and repeat the failed stage. Do not move to the next agent.

## 4. Gate 0 — Canonical inventory freeze

Before agent-by-agent work begins:

- Parse `agents/registry.yaml` and produce the authoritative ordered agent list.
- Detect duplicate IDs, missing IDs, duplicate names and unexpected gaps.
- Cross-check `knowledge/agent-bindings/AGENT-SKILL-BINDINGS.yaml`.
- Cross-check legacy `agents/agent-registry.yaml` and classify it as canonical, reference or legacy; no ambiguous duplicate source may control runtime.
- Record the exact inventory and baseline count in the tracker.

**Exit evidence:** inventory report + conflict register + tracker baseline.

## 5. Gate 1 — Existing-solution discovery (mandatory for every agent)

For the current agent, search in this order:

### 5.1 Internal reuse
- `nivyindia/Raw-Repository`
- existing AIOS skills/prompts/knowledge packs/workflows/tools/evaluators
- existing agent implementations and execution contracts
- prior Company OS / SOP / playbook material

### 5.2 External reuse
Search approved public sources for:
- ready-made agents
- agent frameworks/templates
- system/task prompts
- skills/tool definitions
- n8n workflows
- MCP/connectors/APIs
- open-source repositories
- evaluation suites
- SOPs/playbooks/templates
- commercial products only when they materially reduce missing implementation and fit policy/cost constraints

### 5.3 Candidate audit
For each serious candidate record:
- source URL/repository
- exact asset
- license/terms
- maintenance/freshness
- implementation evidence
- dependencies
- security/privacy risks
- data requirements
- model/provider requirements
- integration requirements
- quality/evaluation evidence
- compatibility with AIOS
- modifications required
- reuse/adaptation decision

**Rule:** discovery is not complete merely because search results were found. The candidate must be inspected enough to determine whether it is actually reusable.

**Exit evidence:** reuse research record and explicit `reuse/adapt/build-missing` decision.

## 6. Gate 2 — Complete agent specification

Create or update the agent specification so it contains all of the following:

### Identity
- stable ID, name, version, lifecycle, owner, provenance

### Purpose and boundary
- objective
- business outcome
- scope
- non-goals
- escalation conditions
- success/failure criteria

### Input contract
- required/optional inputs
- types/schema
- source and freshness requirements
- tenant/company scope
- ambiguity handling
- validation rules
- missing-data behavior

### Capability contract
- skills with implementation definitions
- executable prompt IDs and bodies
- knowledge packs and retrieval rules
- memory read/write classes and retention
- model/provider policy and fallback
- exact tools and allowed operations
- tool argument constraints

### Workflow contract
- trigger
- ordered steps
- decision points
- state machine/transitions
- delegation/handoffs
- idempotency
- retry/backoff
- timeout/cancellation
- failure/dead-letter behavior

### Governance
- permissions
- side-effect classification
- approval requirements
- sensitive-data rules
- contact/consent rules
- prompt-injection/tool-abuse defenses
- data egress restrictions
- secrets policy

### Output contract
- structured result schema
- status
- actions taken
- records changed
- evidence
- warnings/errors
- confidence/quality indicators where applicable
- next action/handoff

### Verification
- explicit postconditions
- authoritative-system verification
- duplicate/idempotency verification
- side-effect verification
- evidence location

### Observability
- run/task/correlation IDs
- timings
- model usage/cost where available
- tool calls
- approvals
- retries/errors
- output/evaluation metrics
- audit events

### Evaluation
- deterministic unit cases
- golden cases
- negative cases
- policy tests
- tool-call tests
- integration tests
- regression tests
- acceptance thresholds

### Lifecycle/provenance
- source
- license/terms
- adaptations
- dependencies
- compatibility
- changelog
- deprecation/rollback plan

**Exit:** the specification passes the agent completeness checklist.

## 7. Gate 3 — Capability closure

Resolve every referenced ID before implementation can pass:

`Agent → Skill → Prompt/Knowledge → Memory → Model → Tool → Workflow → Policy`

The validator must fail if:
- a referenced ID does not exist;
- a prompt has no executable body;
- a skill has no executable implementation contract;
- a knowledge pack is missing or has no access/freshness policy;
- a tool is undeclared or unauthorized;
- a protected tool lacks an approval path;
- workflow transitions are undefined;
- required input/output schema is absent;
- provenance/evaluation metadata is absent.

## 8. Gate 4 — Implementation

Implementation may include:
- agent-specific orchestration
- reusable skill additions
- prompt additions/adaptations
- knowledge-pack additions
- memory policy additions
- tool adapters
- n8n workflow integration
- Odoo/PostgreSQL/Qdrant/MinIO integration
- state-machine logic
- error/retry handling
- evidence/audit recording

**Preference:** modify reusable shared components only when the behavior is genuinely reusable; otherwise keep agent-specific logic isolated.

## 9. Gate 5 — Testing pyramid

Every agent must have:

1. **Schema/registry tests** — all IDs and contracts resolve.
2. **Unit tests** — core decisions and transformations.
3. **Negative tests** — invalid input, missing data, unauthorized tool, policy denial, malformed output.
4. **Prompt/skill tests** — expected behavior against representative cases.
5. **Tool tests** — exact arguments, authorization and failure behavior.
6. **Workflow tests** — state transitions, retries, idempotency and handoffs.
7. **Integration tests** — actual connected services where available.
8. **Postcondition tests** — authoritative system confirms the intended result.
9. **Regression tests** — prior golden cases remain passing.

Tests must be deterministic where possible and must not require production credentials.

## 10. Gate 6 — Runtime proof

At minimum, demonstrate:

`input → agent resolution → prompt/skill resolution → authorized tool use → result → verification → audit`

For side-effect agents additionally demonstrate:

`request → approval required → approval → side effect → authoritative confirmation → audit`

Live infrastructure evidence should use the user's local Docker environment when the relevant service exists. Do not convert planned or mocked execution into VERIFIED status.

## 11. Gate 7 — Quality acceptance

Each agent receives a task-specific evaluation suite. Generic pass conditions:

- 100% capability/registry resolution
- 100% policy tests pass
- 100% required schema validation pass
- 100% critical negative/security tests pass
- no unresolved critical defects
- all required postconditions verified
- acceptable quality threshold defined for the task and recorded
- no unexplained regression
- provenance/license complete
- observability/audit evidence present

Quality thresholds may be stricter than these baseline gates; never weaker.

## 12. Gate 8 — Completion classification

Use only these states:

- `DISCOVERY`
- `AUDIT`
- `SPECIFICATION`
- `IMPLEMENTATION`
- `TESTING`
- `BLOCKED`
- `COMPLETE`
- `ACTIVE`
- `PAUSED`
- `DEPRECATED`

`COMPLETE` means repository + automated test + required integration/postcondition evidence are present. `ACTIVE` additionally means policy-approved deployment/runtime activation exists.

## 13. Per-agent execution record

For each agent, preserve:

- discovery sources
- reuse decision
- final spec path
- capability closure report
- implementation paths
- tests
- test run evidence
- integration evidence
- verification evidence
- evaluation score/report
- audit/observability evidence
- commit SHA
- known limitations
- rollback/deprecation information

## 14. Shared-component rule

If Agent N reveals that a shared capability is incomplete, stop Agent N, fix the shared capability, regression-test all impacted earlier agents, then resume Agent N. Do not continue forward with a known broken shared layer.

## 15. Agent ordering

Order is taken from the canonical `agents/registry.yaml`, with revenue-first priority preserved where the registry is intentionally sequenced. The tracker is authoritative for the next agent. No later agent may be started while an earlier agent is incomplete unless the tracker explicitly records a dependency-blocking exception.

## 16. Closure pass after all agents

After the final agent:

- run the full registry/capability validator;
- run all agent tests;
- run cross-agent handoff tests;
- run revenue end-to-end tests;
- run policy/security regression suite;
- verify duplicate/legacy registry reconciliation;
- verify documentation/navigation;
- run local Docker integration suite;
- record final evidence and release readiness.

## 17. Definition of done for the whole agent program

The agent program is complete only when every canonical agent has an individual completion record and the cross-agent system passes end-to-end validation. A high agent count, successful YAML parsing, or passing generic runtime health checks alone is never sufficient.
