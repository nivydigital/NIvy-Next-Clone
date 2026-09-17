# Prompt bodies (Phase 2)

Executable prompt bodies for registered prompt IDs.

Layout:
- `PR00X.md` — human-readable body with variables + output instructions
- Parent `prompts/executable.yaml` remains the machine-readable index
- `prompts/agent-prompt-map.yaml` maps agents → primary prompt

Convention:
1. Bodies reference variables declared in `prompts/registry.yaml`
2. Bodies always require JSON-only responses when used by runtime agents
3. Common system/output preamble is applied by the runtime (`common.system` / `common.output`)
