# Master Instructions

## ⚡ QUICK RESUME — READ THIS FIRST
- **Repository:** `nivyindia/Nivy-Next-AIOS`
- **URL:** https://github.com/nivyindia/Nivy-Next-AIOS
- **Branch:** `main`
- **Branch URL:** https://github.com/nivyindia/Nivy-Next-AIOS/tree/main
- **Start/Continue:** `Read docs/REPO-CONTROL/00-MASTER-INSTRUCTIONS.md and start/continue the work.`
- **Flow:** READ → DISCOVER → PLAN/TASK → EXECUTE → VERIFY → RECORD → COMMIT → RESUME
- **Current focus:** Reconcile canonical implementation-plan references with current repository state, then continue the highest-priority unblocked task.
- **Blocker:** Some previously referenced canonical plan paths are not currently under `docs/`; search moved/renamed equivalents before creating duplicates.

## START HERE — READ THIS FILE FIRST

This is the repository's universal work entry point. If the user says **“Read `docs/REPO-CONTROL/00-MASTER-INSTRUCTIONS.md` and start/continue the work”**, that is enough to begin.

### Required sequence
1. Read this file completely.
2. Read every file in `docs/REPO-CONTROL/`.
3. Follow `01-SOURCE-INDEX.md` and discover all related instructions, implementation plans, roadmaps, task lists, progress/status, timelines, dependencies, blockers, reminders/schedules, tests, workflows, README files, and existing trackers.
4. Use repository evidence as truth; never invent status or completion.
5. Select the highest-priority unblocked actionable task from `02-PLAN-TASK-TRACKER.md` and the indexed canonical sources.
6. Execute it when tools/permissions allow.
7. Verify it with appropriate tests, inspection, or other reproducible evidence.
8. Update tracking, progress/timeline, execution evidence, changelog/resume, and README as applicable.
9. Commit completed changes when write access is available.
10. Re-scan the control folder and continue if the user's command means continue.

## Three Mandatory Safeguards

### 1. Source Authority
When sources conflict, resolve them in this order:
1. Actual repository state and reproducible verification evidence.
2. Current canonical plan/task/status sources identified by `01-SOURCE-INDEX.md`.
3. `docs/REPO-CONTROL/` operational records.
4. Older plans, research, archived documents, and historical notes.
5. Conversation memory or assumptions.

Never treat an old plan, previous chat statement, or intended change as proof that the repository is currently in that state.

### 2. Duplicate/Reconciliation Gate
Before creating a new plan, tracker, instruction, status, or implementation file:
- Search for existing, renamed, moved, archived, or equivalent sources.
- If an equivalent exists, map it in `01-SOURCE-INDEX.md` and use the existing canonical source instead of creating a competing copy.
- If sources overlap or conflict, reconcile them explicitly and preserve historical files unless deletion is specifically required.
- A missing referenced path is not proof that the underlying document is missing; search for its equivalent first.

### 3. Human-Approval / Safety Gate
Stop the affected task as `BLOCKED` or `NEEDS APPROVAL` when it requires human approval, credentials, payment, destructive deletion, irreversible external action, or unavailable permissions.
- Do not bypass the gate.
- Continue with independent, non-blocked work when possible.
- Record exactly what is blocked, why, what evidence exists, and the next human action required.

## Rules
- The user should not need to provide a long command after identifying this file.
- Preserve old plans/files; map them rather than deleting them.
- Keep one canonical current status while retaining historical evidence.
- “Learning” means repository operational knowledge reuse, not model fine-tuning.
- Never mark work `DONE` from intention alone.

## Control Pack
- `00-MASTER-INSTRUCTIONS.md` — entry point and mandatory safeguards
- `01-SOURCE-INDEX.md` — discovery map
- `02-PLAN-TASK-TRACKER.md` — plan/task state
- `03-PROGRESS-TIMELINE.md` — progress, milestones, blockers, reminders
- `04-EXECUTION-VERIFICATION.md` — execution/tests/evidence/commits
- `05-CHANGELOG-RESUME.md` — cross-session handoff

## Definition of Done
Implementation → verification → evidence → tracking → README when relevant → commit → resume state.
