# STD-02 — Agent System Standard v2.0

An agent is a governed runtime unit: objective + skills + prompts + knowledge + tools + policy + evaluation.

## Layers (must resolve)

Agent YAML → I/O schemas → Skills (STD-01) → Prompts → Knowledge → Tools → Runtime → Policy → Evaluation

## Status ladder

| Status | Production traffic |
|--------|--------------------|
| declared | No |
| implementation | Dry-run only |
| testing | Shadow / pilot |
| active | Yes (after checklist) |

## Completeness checklist

agent.yaml, schemas, skill implementations, prompt bodies, knowledge packs, runtime, approval policy, audit, golden fixture, owner.

**Honest gap:** many agents remain *scaffold/implementation*, not *active*.
