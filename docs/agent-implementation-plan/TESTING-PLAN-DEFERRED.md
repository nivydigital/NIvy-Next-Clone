# Deferred Testing Plan for All Agents

**Status:** Phase 9 evaluation **harness active** (2026-09-17)  
**Rule:** Full live agent COMPLETE marks still require explicit suite evidence. Offline pyramid runs in CI.

## How

Contract → unit happy-path → negative/policy → schema/golden → eval → integration → regression.

### Phase 9 harness

| Step | Command / path |
|------|----------------|
| Generate fixtures | `python scripts/generate_golden_fixtures.py` |
| Offline tests | `pytest backend/app/test_evaluation.py backend/app/test_skills.py` |
| Chains | `evaluation/chains.yaml` |
| CI | `.github/workflows/evaluation-regression.yml` |
| Docs | `docs/complete-automation-plan/phase-9/PHASE-9-EVALUATION.md` |

## Coverage inventory

### Strategy / lead / CS / finance / marketing / control
A001–A099 as previously scaffolded — offline schema + dry-run workflow coverage via Phase 9.

### Evaluation / learning (A100–A108)
Runtime modules + schemas present; offline module presence tests in `test_evaluation.py`.

## Chain tests

| Chain | Mode |
|-------|------|
| lead-path | dry_schema |
| inbound-comms, response-qa, conversation-intel | workflow_dry_run |
| marketing-* | workflow_dry_run |
| control-eval, learning-agents | schema_presence |

## Maintenance

Update fixtures after schema changes. Do not mark agents COMPLETE until live evaluation evidence is stored.
