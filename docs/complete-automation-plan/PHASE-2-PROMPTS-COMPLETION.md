# Phase 2 — Prompts — Completion Record

**Status:** Implemented (2026-09-17)

## Delivered

| ID | Task | Artifact |
|----|------|----------|
| P2.1 | `prompts/bodies/` structure | `prompts/bodies/README.md` + PR001–PR008.md |
| P2.2 | Executable bodies PR001–PR008 | `prompts/executable.yaml` v2.0 + body files |
| P2.3 | Agent → primary prompt map | `prompts/agent-prompt-map.yaml` |
| P2.4 | Variable ↔ schema alignment | `scripts/check_prompt_schema_alignment.py` |

## Run alignment check

```bash
python3 scripts/check_prompt_schema_alignment.py
```

## Notes

- PR009–PR011 retained for A003–A005 strategy agents.
- Registry prompt status flipped to `implementation` for PR001–PR008.
- Runtime should prepend `common.system` and append `common.output` when loading bodies.
