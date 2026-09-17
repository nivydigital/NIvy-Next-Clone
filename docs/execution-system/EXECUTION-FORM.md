# AIOS Execution Form

Use one completed record for each meaningful implementation task.

```yaml
TASK_ID: ""
TITLE: ""
STARTED_AT: ""
COMPLETED_AT: ""

INSTRUCTION_SOURCES: []
PLAN_SOURCES: []
REPOSITORY_STATE_INSPECTED: []

CLAIM: ""
STATUS: "IN_PROGRESS"

IMPLEMENTATION:
  files_created: []
  files_updated: []
  files_deleted: []
  other_changes: []

VERIFICATION:
  tests_run: []
  tests_passed: []
  tests_failed: []
  tests_skipped: []
  manual_checks: []

EVIDENCE:
  commits: []
  logs: []
  artifacts: []
  relevant_file_paths: []

KNOWLEDGE_EXTRACTED: []
BLOCKER: ""
NEXT_TASK: ""
CLAIM_RELEASED: false
```

## Required narrative

### What was required?

### What was already present?

### What changed?

### How was it verified?

### What evidence proves the result?

### What remains?

## Completion rule

Do not mark `COMPLETE` merely because files were created. Completion requires the applicable implementation and verification evidence, plus status/commit/release actions.
