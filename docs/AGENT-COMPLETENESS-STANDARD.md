# Agent Completeness Standard v1.0

A registered agent is not considered executable merely because an ID, skill list, prompt ID and tool list exist.

## Required layers

Every agent must resolve as:

`Identity → Objective/Scope → Input Contract → Skill Definitions → Prompt Body → Knowledge Retrieval → Memory Policy → Model Policy → Tool Authorization → Workflow/State → Guardrails → Execution → Postcondition Verification → Output Contract → Audit/Observability → Evaluation → Lifecycle/Provenance`

## Required agent fields

- stable `id`, `name`, `version`, lifecycle `status`, owner and provenance
- objective, scope, non-goals and escalation conditions
- input schema: required/optional fields, types, tenant/company scope and ambiguity handling
- output schema: status, structured result, actions, changed records, evidence, warnings/errors and next action
- skills: each referenced skill must have an implementation definition with inputs, procedure, outputs, dependencies and acceptance criteria
- prompts: each referenced prompt must have an executable body, variables, model compatibility and output instructions
- knowledge: referenced packs, retrieval rules, freshness/conflict rules and access policy
- memory: read/write classes, retention and authorization
- model policy: approved model/provider, temperature/context constraints and fallback policy
- tools: exact authorized tools, least-privilege arguments and side-effect classification
- workflow/state: trigger, steps, state transitions, idempotency, retry and timeout policy
- guardrails: prohibited actions, data handling, hallucination/source rules and approval gates
- verification: explicit postconditions and authoritative-system checks
- audit/observability: run/correlation IDs, timings, tool calls, approvals, failures and evidence
- evaluation: deterministic tests, quality criteria, regression tests and evidence path
- provenance/license/modifications and compatibility information

## Activation gates

`declared` → `testing` → `active` only after all referenced capabilities resolve, executable prompt/skill bodies exist, validation passes, policy passes and evaluation evidence exists. Production/autonomous activation also requires integration health and observability evidence.

Missing or ambiguous required data is fail-closed. The runtime must never silently substitute an undeclared capability.

## Reuse rule

Before creating a new implementation, search `Raw-Repository` and approved external sources for reusable agents, skills, prompts, workflows, evaluators, connectors and playbooks. Reused material must retain provenance, license/terms and an adaptation record.

## Source baseline

This standard incorporates the reusable execution lifecycle from `Raw-Repository/Chats/ChatGPT/Multi Agent AIOS/02-agents/AGENT_EXECUTION_CONTRACT.md`: `Receive → Validate → Authorize → Plan → Execute → Verify → Commit/Report → Audit`.
