# AIOS Task Intake Form

Copy this form when a new user command needs to be resolved into repository work.

```yaml
TASK_ID: ""
USER_COMMAND: ""
REQUESTED_OUTCOME: ""
STAGE: ""
GATE: ""
AGENT_OR_SKILL: ""
TARGET_FILES: []

STATE_SOURCE: "WORK-STATUS.md"
INSTRUCTION_SOURCES: []
PLAN_SOURCES: []
GOVERNANCE_SOURCES: []
DEPENDENCIES: []

EXISTING_IMPLEMENTATION_FOUND: false
DUPLICATE_RISK: "low|medium|high"
CLAIM_STATUS: "unclaimed|claimed|in_progress|blocked|complete"

REQUIRED_DELIVERABLES: []
REQUIRED_TESTS: []
HUMAN_APPROVAL_REQUIRED: false
BLOCKER: ""
```

## Intake questions

- What exactly did the user ask to change or produce?
- Which existing plan/task does it map to?
- Which instructions govern the work?
- What already exists?
- What dependencies must be satisfied?
- What evidence will prove completion?
- Is human approval required?

## Resolution rule

Do not implement directly from this form. Resolve the authoritative instruction and plan sources first, then create the execution record.
