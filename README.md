# Nivy-Next-AIOS

## 🚀 START / CONTINUE WORK

> **Repository:** `nivyindia/Nivy-Next-AIOS` | **Branch:** `main`
>
> Start with `WORK-STATUS.md`, then `docs/execution-system/MASTER-EXECUTION-SYSTEM.md`, then the canonical implementation plan and progress tracker.

## Canonical implementation state

- **Plan:** `docs/plans/AIOS-FINAL-IMPLEMENTATION-PLAN-v3.1.md`
- **Progress:** `docs/plans/AIOS-PROGRESS-TRACKER.md`
- **Source map:** `docs/plans/AIOS-SOURCE-MAP.md`
- **Conflict register:** `docs/plans/AIOS-CONFLICT-REGISTER.md`
- **Metadata contract:** `schemas/governance/metadata-contract.yaml`
- **Skills:** `skills/registry.yaml`
- **Prompts:** `prompts/registry.yaml`
- **Knowledge packs:** `knowledge/packs/registry.yaml`
- **Memory:** `memory/registry.yaml`
- **Reusable assets:** `research/reusable-assets/registry.yaml`
- **Agents:** `agents/registry.yaml`
- **Agent factory:** `agents/_template/agent.yaml`
- **Capability bindings:** `knowledge/agent-bindings/AGENT-SKILL-BINDINGS.yaml`

## Phase 0–3 status

Phase 0, Phase 1, Phase 2 and Phase 3 are recorded as **VERIFIED at the repository-contract level**. This does **not** mean every agent is executable or production-ready. Runtime execution still requires implementation, credentials where applicable, policy/approval checks, tests and evidence.

## AIOS execution system

`docs/execution-system/MASTER-EXECUTION-SYSTEM.md` is the operational entry point for discovery, plan/task resolution, implementation, verification, evidence and resume state.

Execution loop:

```text
CHECK → READ STATE → RESOLVE PLAN → INSPECT → CLAIM → IMPLEMENT
→ VERIFY → RECORD EVIDENCE → STATUS → COMMIT → RECHECK → CONTINUE
```

## Runtime

The repository includes Docker and Windows V1 installation/testing infrastructure. The next implementation gate after the completed contract foundation is **Phase 4 — Policy, Approval, Safety & Trust**.
