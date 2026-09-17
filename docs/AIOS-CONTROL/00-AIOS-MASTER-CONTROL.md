# AIOS MASTER CONTROL

**Common cross-repository execution standard.**

Read this file first whenever a ChatGPT/AI agent is asked to continue, implement, audit, test, or complete work in this repository.

## Mandatory scan

1. Read `00-AIOS-MASTER-CONTROL.md`.
2. Scan the entire `docs/AIOS-CONTROL/` folder.
3. Read the repository's canonical state/resume file.
4. Find the canonical implementation/master plan.
5. Find progress, task, timeline, milestone, dependency, and blocker records.
6. Inspect existing implementation before creating anything.
7. Resolve the user's command to the exact task.
8. Execute → test → record evidence → update status → commit.
9. Re-scan control files after the work.
10. Continue to the next actionable task unless blocked or human approval is required.

## Control files

| File | Purpose |
|---|---|
| `00-AIOS-MASTER-CONTROL.md` | Single entry point and rules |
| `01-AIOS-INSTRUCTION-INDEX.md` | Finds applicable instructions |
| `02-AIOS-PLAN-TASK-INDEX.md` | Finds plans/tasks/milestones |
| `03-AIOS-SEARCH-SCAN-PROTOCOL.md` | Defines repository-wide scan order |
| `04-AIOS-TASK-INTAKE.md` | Converts command into an actionable task |
| `05-AIOS-EXECUTION-RECORD.md` | Records implementation and evidence |
| `06-AIOS-TEST-VERIFICATION.md` | Records verification and tests |
| `07-AIOS-KNOWLEDGE-LOOP.md` | Captures verified reusable knowledge |
| `08-AIOS-RESUME-CONTINUITY.md` | Preserves exact resume state |
| `09-AIOS-REMINDER-SCHEDULE.md` | Tracks reminders, deadlines and automation |

## Authority

Repository evidence > canonical plans/state > control files > conversational memory.

Never invent a missing plan, task, status, test result, dependency, or completion percentage. If two sources conflict, record the conflict and resolve it using the repository's governance rules.

## Important terminology

“Learning/training” in this system means repository-based operational knowledge reuse. It does not mean changing or fine-tuning the ChatGPT model.

## Completion gate

A task is complete only when implementation, applicable verification, evidence, status update, commit, and resume continuity are all handled.
