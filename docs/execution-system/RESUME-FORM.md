# AIOS Resume Form

Use this record when work ends, pauses, or is blocked.

```yaml
SESSION_ID: ""
DATE: ""
LAST_COMPLETED_TASK: ""
CURRENT_TASK: ""
CURRENT_STATUS: "complete|in_progress|blocked"

CANONICAL_STATE_FILE: "WORK-STATUS.md"
PLAN_SOURCE: ""
INSTRUCTION_SOURCES: []

CLAIMED_TASKS: []
COMPLETED_TASKS: []
VERIFIED_EVIDENCE: []
COMMITS: []

BLOCKER: ""
HUMAN_INPUT_REQUIRED: false

NEXT_HIGHEST_PRIORITY_TASK: ""
NEXT_ACTION: ""
RELEASED_CLAIMS: []
```

## Resume rule

A new session must be able to continue from this record plus the repository itself. Do not depend on private conversational memory.

## Required final checks

- current status written;
- completed work evidenced;
- commit recorded;
- claims released unless intentionally still active;
- blockers explicit;
- next task identified from canonical plan/state;
- any missing canonical reference recorded.

## Relationship to WORK-STATUS.md

`WORK-STATUS.md` remains the repository's single resume point. This form defines the structure of the information that should be captured; it does not replace `WORK-STATUS.md`.
