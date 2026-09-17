# Complete Automation Plan

**Purpose:** Single place to track everything still required to automate Nivy end-to-end — not only agents, but skills, prompts, tools, workflows, knowledge, orchestration, and gates.

**Created:** 2026-09-17  
**Status vocabulary:** 🟢 Complete · 🟡 In progress · ⚪ Not started · 🔴 Blocked

## Documents in this folder

| File | Role |
|------|------|
| [GAP-ANALYSIS.md](./GAP-ANALYSIS.md) | What exists vs what is missing for full automation |
| [MASTER-IMPLEMENTATION-PLAN.md](./MASTER-IMPLEMENTATION-PLAN.md) | Phased work plan with ordered workstreams |
| [PROGRESS-TRACKER.md](./PROGRESS-TRACKER.md) | Live checklist — update after every session |
| [DEPENDENCY-MAP.md](./DEPENDENCY-MAP.md) | How layers depend on each other |

## Related existing docs

- `docs/agent-implementation-plan/` — agent-only build + deferred testing
- `docs/AGENT-COMPLETENESS-STANDARD.md` — activation gates for agents
- `docs/DEFINITION-OF-DONE.md` — platform-level DoD
- `docs/AIOS-AUTOMATION-MAP.md` — target automation journeys
- `WORK-STATUS.md` — latest agent batch resume point

## Rule

Agents alone do **not** automate the business. Automation requires:

`Agent contract → Skill bodies → Prompt bodies → Tool implementations → Workflow orchestration → Knowledge/memory → Approvals → Persistence → Evaluation`

Update **PROGRESS-TRACKER.md** whenever a workstream moves.
