# STD-01 — Skill Standard v2.0

Every skill is a **reusable, versioned, testable procedure** — not a one-line description.

## Mandatory fields

id, name, version, status, category, objective, non_goals, inputs, outputs, procedure (≥3 steps), preconditions, postconditions, quality_checks, failure_policy, evidence_policy, dependencies, permissions, acceptance_criteria, evaluation, provenance.

## Execution shape

```
RECEIVE → VALIDATE → PREPARE → EXECUTE → QUALITY_CHECK → VERIFY → RETURN → AUDIT
```

## Quality bar

1. Deterministic structure  
2. Fail-closed  
3. No fabricated evidence  
4. Least privilege tools  
5. Semver + provenance  
6. Testable acceptance criteria  
7. Owner + last_reviewed  

## Promotion

`declared` → `implementation` → `testing` → `active`
