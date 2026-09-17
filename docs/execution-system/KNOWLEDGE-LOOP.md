# AIOS Knowledge Loop

## Purpose

Turn verified implementation experience into reusable operational knowledge so future agents can work with less repeated discovery.

This is **not model training**. Repository documents can change the agent's available instructions/context, but they do not permanently retrain the underlying ChatGPT model.

## Loop

```text
WORK → VERIFY → EXTRACT LESSON → CHECK PROVENANCE → DRAFT KNOWLEDGE
→ HUMAN/CANONICAL APPROVAL WHEN REQUIRED → PUBLISH TO AUTHORITATIVE LOCATION
→ INDEX → REUSE → REVIEW
```

## What may become reusable knowledge

- verified implementation patterns;
- stable architecture decisions;
- tested setup/run procedures;
- reusable agent/skill contracts;
- recurring failure modes and verified fixes;
- dependency/version constraints;
- validated governance rules;
- test procedures that reliably prove a gate.

## What must not become authoritative automatically

- guesses;
- one-off observations without evidence;
- failed experiments presented as working patterns;
- secrets or credentials;
- user-sensitive data;
- stale external information;
- conversational assumptions;
- an implementation merely because it compiled.

## Knowledge record

```yaml
KNOWLEDGE_ID: ""
SOURCE_TASK_ID: ""
SOURCE_COMMIT: ""
STATEMENT: ""
EVIDENCE: []
SCOPE: ""
CONFIDENCE: "verified|provisional|deprecated"
APPROVAL_REQUIRED: false
APPROVAL_STATUS: "not_required|pending|approved|rejected"
CANONICAL_LOCATION: ""
LAST_VERIFIED: ""
REVIEW_TRIGGER: ""
```

## Improvement rule

If the same discovery or failure happens repeatedly, update the relevant instruction/index/form instead of relying on the agent to remember the conversation.

If new knowledge conflicts with an existing authoritative rule, do not silently overwrite it. Reconcile the conflict and record the decision.
