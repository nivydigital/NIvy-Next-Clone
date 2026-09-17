# Nivy Next AIOS — Autonomous Start / Continue Command

> **Canonical execution system:** `docs/execution-system/MASTER-EXECUTION-SYSTEM.md`

**START / CONTINUE Nivy AIOS using the ChatGPT AIOS Execution System.** Read `WORK-STATUS.md`, the master execution system, instruction index, plan/task index, canonical implementation plan/tracker and relevant governance/architecture documents. Resolve the user's command to the highest-priority actionable task. Inspect the current repository state before acting. Claim the task, mark it `IN_PROGRESS`, execute the required work, verify it, record evidence and status, commit the work, release the claim, re-check the repository state, and continue to the next actionable task unless blocked or human approval is required.

## Canonical loop

`CHECK → READ CANONICAL STATE → RESOLVE INSTRUCTIONS → RESOLVE PLAN/TASK → INSPECT → CLAIM → IN_PROGRESS → WORK → VERIFY → RECORD EVIDENCE → UPDATE STATUS → COMMIT → RELEASE CLAIM → KNOWLEDGE LOOP → RECHECK → CONTINUE`

## ChatGPT AIOS Execution System

- `docs/execution-system/MASTER-EXECUTION-SYSTEM.md` — top-level execution contract
- `docs/execution-system/INSTRUCTION-INDEX.md` — find the right instructions
- `docs/execution-system/PLAN-TASK-INDEX.md` — find the right plan/task
- `docs/execution-system/SEARCH-PROTOCOL.md` — repository discovery procedure
- `docs/execution-system/TASK-INTAKE-FORM.md` — resolve a user command into a task
- `docs/execution-system/EXECUTION-FORM.md` — record implementation/evidence
- `docs/execution-system/TESTING-FORM.md` — record verification
- `docs/execution-system/KNOWLEDGE-LOOP.md` — turn verified lessons into reusable operational knowledge
- `docs/execution-system/RESUME-FORM.md` — preserve cross-session continuation state

## Important distinction

The knowledge loop does **not** retrain ChatGPT. It makes verified repository knowledge, instructions and procedures available to future execution sessions. Actual model training/fine-tuning is a separate process and must never be implied by ordinary document updates.

## Repository reconciliation

The README/WORK-STATUS currently declare additional canonical plan paths under `docs/plans/`. If those paths are absent, search for moved/renamed equivalents before creating duplicates and record the discrepancy in the work evidence.
