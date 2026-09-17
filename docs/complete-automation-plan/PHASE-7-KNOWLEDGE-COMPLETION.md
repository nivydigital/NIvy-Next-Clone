# Phase 7 — Knowledge, Memory, RAG

**Status:** Implemented (2026-09-17)

| ID | Artifact |
|----|----------|
| P7.1 | `knowledge/packs/KP001.md`–`KP008.md` |
| P7.2 | `knowledge/agent-bindings/AGENT-KNOWLEDGE-BINDINGS.yaml` |
| P7.3 | `backend/app/runtime/knowledge/ingest.py` |
| P7.4 | `memory/policy.yaml` |

```bash
PYTHONPATH=. KNOWLEDGE_MOCK=1 pytest backend/tests/test_phase7_knowledge.py -q
```
