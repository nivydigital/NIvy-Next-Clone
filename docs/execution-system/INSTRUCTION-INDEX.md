# AIOS Instruction Index

Use this file to discover **how** a task must be performed.

## Search order

1. `WORK-STATUS.md` — current state and resume point.
2. `docs/execution-system/MASTER-EXECUTION-SYSTEM.md` — universal execution contract.
3. `AUTONOMOUS-START-CONTINUE.md` — autonomous start/continue command.
4. Existing governance, architecture, agent, skill, policy and schema documents discovered in the repository.
5. Task-specific instructions referenced by the applicable plan.
6. External sources only when the repository explicitly requires them.

## Instruction resolution rules

For every user command, identify:

| Question | Required result |
|---|---|
| What are we doing? | User intent / task |
| How must it be done? | Applicable instruction sources |
| What authority governs it? | Canonical policy/plan |
| What already exists? | Repository evidence |
| What must be produced? | Task deliverables |
| How is it verified? | Applicable tests/evidence |
| What must be remembered? | Knowledge-loop entry |

## Existing instruction sources

- `AUTONOMOUS-START-CONTINUE.md` — autonomous execution loop.
- `WORK-STATUS.md` — current-state authority.
- `README.md` — repository purpose and navigation.
- `docs/execution-system/MASTER-EXECUTION-SYSTEM.md` — this system's top-level execution contract.
- `docs/execution-system/SEARCH-PROTOCOL.md` — discovery procedure.
- `docs/execution-system/EXECUTION-FORM.md` — work record.
- `docs/execution-system/TESTING-FORM.md` — verification record.
- `docs/execution-system/KNOWLEDGE-LOOP.md` — reusable knowledge procedure.
- `docs/execution-system/RESUME-FORM.md` — cross-session continuation record.

## Missing-source rule

If a referenced instruction does not exist at the referenced path:

1. Search the repository for the title/key terms.
2. Check whether the source moved or was renamed.
3. Prefer the discovered canonical replacement.
4. Record the discrepancy in the work evidence.
5. Do not invent a replacement as if it were pre-existing authority.
6. Create a new canonical instruction only when the current task explicitly requires it and no authoritative equivalent exists.
