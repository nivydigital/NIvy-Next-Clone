# Agent Completion Gates v1.0

An agent advances only when the current gate passes.

| Gate | Required evidence | Fail condition |
|---|---|---|
| G0 Inventory | canonical ID/order | duplicate or ambiguous registry |
| G1 Discovery | Raw-Repository + relevant external search record | reuse gate skipped |
| G2 Audit | candidate/license/security/compatibility review | unknown provenance or unacceptable risk |
| G3 Specification | complete agent contract | any mandatory field missing |
| G4 Capability closure | all skills/prompts/knowledge/memory/model/tools/policy/workflow resolve | unresolved reference |
| G5 Implementation | runnable implementation paths | placeholder-only behavior |
| G6 Unit/negative tests | passing deterministic tests | core/negative test failure |
| G7 Integration | connected service evidence where required | mocked-only proof for required integration |
| G8 Postcondition | authoritative system confirms result | result inferred only from model output |
| G9 Observability/audit | trace, tool, approval, failure evidence | material execution untraceable |
| G10 Evaluation | task-specific acceptance evidence | threshold not met/unproven |
| G11 Release | provenance, limitations, rollback, commit | incomplete release record |

## Status rules

- `DISCOVERY`: source investigation in progress.
- `AUDIT`: candidate and existing implementation audit in progress.
- `SPECIFICATION`: contract being completed.
- `IMPLEMENTATION`: coding/configuration/integration in progress.
- `TESTING`: tests or runtime verification in progress.
- `BLOCKED`: dependency or evidence prevents progress.
- `COMPLETE`: all required gates G0–G11 pass.
- `ACTIVE`: COMPLETE plus approved runtime activation evidence.
- `PAUSED`: intentionally stopped after a valid state.
- `DEPRECATED`: retired with replacement/rollback information.

**Critical rule:** a green generic CI run does not by itself make every agent COMPLETE. Agent-specific evidence is required.
