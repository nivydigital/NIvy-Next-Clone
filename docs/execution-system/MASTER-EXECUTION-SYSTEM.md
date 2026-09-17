# Nivy Next AIOS — ChatGPT AIOS Execution System

**Status:** Canonical operational entry point  
**Purpose:** Make a fresh ChatGPT/AI agent able to discover the right instructions, locate the right implementation plan/task, execute it, verify it, record evidence, and resume later without relying on hidden conversation memory.

## 1. What this system does

A user may give only a high-level command such as `do the next task`, `implement stage G`, or `continue AIOS`. The agent must resolve that command against repository evidence before acting.

The system connects five layers:

1. **State** — current work, claims, blockers and resume position.
2. **Instructions** — rules governing how the work must be performed.
3. **Plans/tasks** — what work is required and in what order.
4. **Execution forms** — a repeatable record for implementation, verification and evidence.
5. **Knowledge loop** — verified lessons become reusable operational knowledge; this is not model retraining.

## 2. Canonical start command

> **START / CONTINUE Nivy AIOS using the ChatGPT AIOS Execution System. Read `WORK-STATUS.md`, then this master system, the Instruction Index, Plan/Task Index, canonical implementation plan/tracker and relevant governance/architecture documents. Resolve the user's command to the highest-priority actionable task. Inspect the repository before changing anything. Claim the task, execute only the required work, verify it, record evidence, update status, commit the work, release the claim, re-check the canonical state, and continue to the next actionable task unless blocked or human approval is required. Never invent a missing instruction, plan, status, test result, completion percentage, or dependency. Treat verified repository evidence as authoritative over memory.**

## 3. Mandatory resolution order

`WORK-STATUS → MASTER SYSTEM → INSTRUCTION INDEX → PLAN/TASK INDEX → CANONICAL PLAN/TRACKER → RELEVANT GOVERNANCE/ARCHITECTURE → REPOSITORY INSPECTION → EXECUTION FORM → TESTING FORM → KNOWLEDGE LOOP → RESUME FORM`

If a referenced canonical file is missing or stale, record that as a repository-state issue and search the repository for its replacement. Do not silently recreate a conflicting canonical authority.

## 4. Execution lifecycle

```text
INTAKE
  ↓
RESOLVE INSTRUCTIONS
  ↓
RESOLVE PLAN / TASK
  ↓
INSPECT CURRENT STATE
  ↓
CLAIM + IN_PROGRESS
  ↓
IMPLEMENT
  ↓
VERIFY
  ↓
RECORD EVIDENCE
  ↓
UPDATE STATUS
  ↓
COMMIT
  ↓
RELEASE CLAIM
  ↓
KNOWLEDGE EXTRACTION
  ↓
RECHECK
  ↓
CONTINUE / BLOCK
```

## 5. Authority rules

- Repository evidence beats conversational memory.
- Canonical plans beat ad-hoc task lists.
- Existing implementation beats duplicate recreation.
- Verified tests beat assumptions.
- Draft knowledge never becomes authoritative merely because it exists.
- Human approval requirements must never be bypassed.
- Destructive changes require explicit authorization from the governing rules.
- A failed or skipped test must be recorded honestly.
- “Trained” means only actual model training/fine-tuning. Normal document learning is **operational knowledge acquisition**, not model training.

## 6. Definition of done

A task is not complete until all applicable items are true:

- Correct instruction source identified.
- Correct plan/task identified.
- Existing state inspected.
- Work claimed before substantive implementation.
- Implementation completed or a documented blocker recorded.
- Applicable tests/checks executed.
- Evidence captured.
- Status updated.
- Commit created.
- Claim released.
- Reconciliation performed.
- Reusable knowledge extracted when justified.

## 7. Related forms

- `INSTRUCTION-INDEX.md`
- `PLAN-TASK-INDEX.md`
- `SEARCH-PROTOCOL.md`
- `TASK-INTAKE-FORM.md`
- `EXECUTION-FORM.md`
- `TESTING-FORM.md`
- `KNOWLEDGE-LOOP.md`
- `RESUME-FORM.md`
