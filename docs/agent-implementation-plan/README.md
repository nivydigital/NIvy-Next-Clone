# Agent Implementation Plan

**Status:** Canonical execution folder
**Purpose:** Complete and verify every canonical AIOS agent one-by-one before moving to the next agent.

## Governing rule

`DISCOVER → AUDIT → REUSE → ADAPT → INTEGRATE → IMPLEMENT ONLY WHAT IS MISSING → TEST → VERIFY → DOCUMENT → ACTIVATE`

This folder overrides any older agent-by-agent sequencing document. Platform phases may continue only where they do not conflict with this closure process. No agent is considered complete because it is merely registered.

## Required order

1. Freeze the canonical agent inventory from `agents/registry.yaml`.
2. For the current agent, search Raw-Repository and approved internet sources for ready-made agents, skills, prompts, workflows, tools/connectors and evaluators.
3. Audit all candidate sources, including license, provenance, freshness, dependencies, security and compatibility.
4. Reuse/adapt the strongest suitable source before writing new logic.
5. Build the complete agent specification using `docs/AGENT-COMPLETENESS-STANDARD.md` and `schemas/agent-spec.schema.yaml`.
6. Resolve every capability: skills, executable prompts, knowledge, memory, model, tools, workflow/state and policy.
7. Implement runtime behavior and integration adapters required by the agent.
8. Test the agent in isolation, then test its protected side effects and downstream handoffs.
9. Produce evidence and update the tracker.
10. Only after the current agent reaches **COMPLETE** may work begin on the next agent.

## Definition of complete

An agent is **COMPLETE** only when all mandatory contract fields are populated, every referenced capability resolves, executable prompt/skill bodies exist, reuse research is recorded, policy is enforced, deterministic tests pass, postconditions are verified, observability/audit evidence exists, provenance is recorded, and the required local/integration smoke test has evidence. If any gate is missing, status remains `BLOCKED`, `IN_PROGRESS`, or `TESTING`.

## Documents

- `MASTER-AGENT-IMPLEMENTATION-PLAN.md` — detailed implementation standard and sequencing.
- `AGENT-PROGRESS-TRACKER.md` — one-row-per-agent progress and evidence tracker.
- `AGENT-SPEC-CHECKLIST.md` — repeatable gate checklist for each agent.
- `REUSE-DISCOVERY-PROTOCOL.md` — mandatory Raw-Repository/internet reuse process.
- `COMPLETION-GATES.md` — objective pass/fail rules; prevents false completion.

## Canonical dependencies

- Agent standard: `docs/AGENT-COMPLETENESS-STANDARD.md`
- Agent schema: `schemas/agent-spec.schema.yaml`
- Agent registry: `agents/registry.yaml`
- Agent bindings: `knowledge/agent-bindings/AGENT-SKILL-BINDINGS.yaml`
- Executable prompts: `prompts/executable.yaml`
- Skill definitions: `skills/definitions.yaml`
- Skill execution contract: `skills/execution-contract.yaml`
- Runtime: `backend/app/runtime/`
- Reuse warehouse: `nivyindia/Raw-Repository`

## Resume rule

Always open `AGENT-PROGRESS-TRACKER.md` first. Work only on the first agent that is not COMPLETE. Never skip an incomplete earlier agent merely because a later agent is easier.
