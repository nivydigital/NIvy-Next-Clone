# Phase 3 — Skills

**Status:** 🟡 Partial complete (lead path + resolver + tests + API)

## Delivered

### P3.1 / P3.2 — Implementations
- `skills/implementations/SK034.yaml` … `SK050.yaml` (lead/sales path — full procedures)
- Generator: `scripts/generate_skill_implementations.py` for remaining SK001–SK033 stubs from `definitions.yaml`
- **Action:** run `python scripts/generate_skill_implementations.py` in repo root to fill SK001–SK033 if not yet present

### P3.3 — Runtime resolve (fail closed)
- `backend/app/runtime/skills.py`
  - `load_skill_implementation`
  - `resolve_agent_skills` — Agent → Skills → Tools; raises `RuntimeDenied` if skill file missing or skill tools not on agent
  - `skill_coverage_report`

### API (v0.8.0)
| Method | Path |
|--------|------|
| GET | `/api/v1/runtime/skills/coverage` |
| GET | `/api/v1/runtime/agents/{id}/skills/resolve` |

### P3.4 — Tests
- `backend/app/test_skills.py` — lead skills exist, load SK034, coverage structure, unknown agent fails

## Not fully closed
- SK001–SK033 may still be missing until generator is run once
- Skills are procedure specs — not yet invoked step-by-step inside every `run_a0XX` (agents still LLM-first)
- Full CI job wiring deferred with testing policy
