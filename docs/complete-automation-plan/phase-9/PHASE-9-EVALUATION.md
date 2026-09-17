# Phase 9 — Evaluation (lift deferred testing)

**Status:** 🟡 Harness complete; live LLM/agent COMPLETE marks still gated

## Delivered

| ID | Task | Artifact |
|----|------|----------|
| P9.1 | Golden fixtures from schemas | `scripts/generate_golden_fixtures.py` → `evaluation/fixtures/golden/` |
| P9.2 | Offline pyramid tests | `backend/app/test_evaluation.py` |
| P9.3 | Chain definitions | `evaluation/chains.yaml` |
| P9.4 | CI regression job | `.github/workflows/evaluation-regression.yml` |
| P9.5 | Mark COMPLETE | **Not done globally** — only after live suites pass |

## How to run locally

```bash
python scripts/generate_golden_fixtures.py
PYTHONPATH=. pytest backend/app/test_evaluation.py backend/app/test_skills.py -q
```

## Pyramid (per TESTING-PLAN-DEFERRED)

1. Contract / schema presence — offline ✅
2. Golden fixtures — generated ✅
3. Workflow dry-run chains — offline ✅
4. Live agent happy-path — requires Ollama / mocks (not auto-marked COMPLETE)
5. Policy negative tests — deferred per agent batch
6. Full regression — CI job runs offline slice on every PR

## Policy

Agents remain **implementation** (not COMPLETE) until explicit live evaluation evidence is recorded. This phase **lifts the harness**; it does not auto-promote production readiness.
