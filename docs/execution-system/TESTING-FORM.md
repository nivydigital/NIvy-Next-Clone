# AIOS Testing Form

Use this form after implementation and before declaring a task complete.

```yaml
TASK_ID: ""
TEST_RUN_ID: ""
TESTED_AT: ""

STATIC_CHECKS:
  run: []
  result: "pass|fail|not_applicable"

UNIT_TESTS:
  run: []
  result: "pass|fail|not_applicable"

INTEGRATION_TESTS:
  run: []
  result: "pass|fail|not_applicable"

RUNTIME_HEALTH:
  run: []
  result: "pass|fail|not_applicable"

AGENT_OR_WORKFLOW_SMOKE:
  run: []
  result: "pass|fail|not_applicable"

REGRESSION_CHECKS:
  run: []
  result: "pass|fail|not_applicable"

SECURITY_CONFIG_CHECKS:
  run: []
  result: "pass|fail|not_applicable"

EVIDENCE: []
FAILURES: []
SKIPPED_WITH_REASON: []
OVERALL: "pass|fail|blocked"
```

## Verification principles

- Test the smallest relevant layer first, then broader layers when applicable.
- Never report an unrun test as passed.
- Distinguish infrastructure health from business/agent correctness.
- Preserve failing evidence; do not hide failures to obtain a green status.
- Record exact commands, endpoints, workflow IDs, logs or artifacts where available.
- If a test is not applicable, record why.

## Minimum gate

A task may be marked complete only when all required tests for its task class pass or an explicit human-approved exception is recorded.
