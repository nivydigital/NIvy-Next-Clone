# AIOS Search Protocol

This protocol defines how an agent finds the right information before implementing work.

## A. Start with state

Read:

1. `WORK-STATUS.md`
2. `README.md`
3. `AUTONOMOUS-START-CONTINUE.md`

Record the current task, next task, blockers and declared canonical references.

## B. Resolve the user's command

Extract:

- requested action;
- stage/gate/task/agent/skill IDs, if present;
- target component/file;
- requested outcome;
- constraints such as `do next`, `implement`, `test`, `fix`, or `reconcile`.

## C. Search the repository

Search in this order:

```text
exact task ID / exact file name
→ stage / gate name
→ agent / skill / component name
→ distinctive requirement phrase
→ related architecture/governance terms
→ broader semantic search
```

Inspect actual files after search results. Search results are discovery aids, not authority by themselves.

## D. Resolve authority

When multiple documents disagree:

1. explicit current governance/policy;
2. canonical implementation plan;
3. current verified repository implementation;
4. current work status;
5. supporting design/research documents;
6. raw/research material;
7. conversational memory.

If authority is ambiguous, stop the affected action and record the ambiguity rather than silently choosing.

## E. Find existing work before creating

Before creating any file, agent, skill, schema, workflow or service:

- search exact names;
- search aliases and IDs;
- inspect neighboring directories;
- inspect references/imports;
- inspect recent relevant commits when necessary.

Reuse or extend existing canonical work when appropriate.

## F. External research

Use external sources only when:

- the repository requires current external facts;
- implementation depends on an external API/specification;
- a required dependency must be verified;
- repository instructions explicitly request research.

Record external-source provenance in the execution evidence.

## G. Stop conditions

Do not proceed with substantive implementation when:

- the task identity cannot be resolved;
- a required authority source is missing and cannot be reconciled;
- destructive action is not authorized;
- required human approval is pending;
- the requested outcome conflicts with a higher-priority repository rule.

Record the blocker and use the resume form.
