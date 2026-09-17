# WORK STATUS — SINGLE RESUME POINT

- Last updated: 2026-09-17
- Phase 8: 🟢 marketing workflows
- **Phase 9: 🟡** evaluation harness (fixtures, chains, CI); agents not auto-COMPLETE

## Phase 9
```bash
python scripts/generate_golden_fixtures.py
PYTHONPATH=. pytest backend/app/test_evaluation.py -q
```
CI: `.github/workflows/evaluation-regression.yml`

## Next
Phase 7 knowledge/RAG, Phase 10 hardening, or live evaluation runs against Ollama.
