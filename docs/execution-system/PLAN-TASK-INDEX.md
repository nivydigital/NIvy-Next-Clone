# AIOS Plan / Task Index

Use this file to discover **what** work should be performed.

## Resolution algorithm

1. Read `WORK-STATUS.md`.
2. Locate the canonical implementation plan/tracker named by the current repository state.
3. Search for the requested stage, task ID, agent ID, skill ID, component name or deliverable.
4. Determine dependencies and completion gates.
5. Compare the planned work with the actual repository state.
6. Select the highest-priority **incomplete + unclaimed + actionable** task.
7. Use the task's required instruction sources and forms.

## Canonical plan references currently declared by the repository

The README/WORK-STATUS currently refer to:

- `docs/plans/AIOS-FINAL-IMPLEMENTATION-PLAN-v1.0-2026-09-06-SUN.md`
- `docs/plans/AIOS-ONE-PAGE-BUILD-MAP-v1.0-2026-09-06-SUN.md`
- `docs/plans/AIOS-AUTONOMOUS-EXECUTION-BOOTSTRAP.md`
- `docs/plans/AIOS-AUTONOMOUS-PROGRESS-LOCK.md`

At the time this execution system was created, the repository's `docs/` directory did not contain those declared plan files. Therefore they are **references requiring reconciliation**, not assumed available content. Search for moved/renamed equivalents before creating duplicates.

## Task selection criteria

Priority is determined by the canonical plan, then by dependency order. Do not create a personal ranking when the plan already defines order.

A task is actionable when:

- it is not already verified complete;
- all required dependencies are satisfied or explicitly allowed to be parallel;
- no active claim blocks it;
- required authority/instructions are available;
- no human approval is pending.

## Task identity

Prefer stable identifiers such as:

`STAGE → GATE → TASK → AGENT/SKILL → DELIVERABLE`

If no stable ID exists, derive a temporary descriptive task ID and record it in the execution form; do not pretend it is a canonical plan ID.

## Reconciliation rule

If the plan says a task is complete but repository evidence contradicts it, flag the mismatch and reconcile before proceeding. If the repository contains implementation that the plan does not mention, preserve it and record the discrepancy rather than deleting or duplicating it.
