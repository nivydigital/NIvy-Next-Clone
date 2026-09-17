# Priority Backlog

**Last updated:** 2026-09-17

Legend: ⚪ not started · 🟡 in progress · 🟢 done · 🔴 blocked

## P0 — Foundation wiring

| ID | Item | Status | Notes |
|----|------|--------|-------|
| A1 | All 50 skills on main + validate green | 🟢 | generate_std01_skills + validate |
| A3 | Skill resolver runtime | 🟢 | `backend/app/runtime/skill_resolver.py` |
| B1 | Prompt body loader | 🟢 | `prompt_loader.py` + engine wire |

## P1 — Lead-path depth

| ID | Item | Status | Notes |
|----|------|--------|-------|
| A2 | Deepen SK034–SK050 | 🟢 | All SK034–SK050 at STD-01 v1.1 |
| A4 | Unit tests lead skills | 🟢 | `backend/app/test_lead_skills.py` |
| C2 | A034–A052 completeness | ⚪ | |
| C3 | Golden fixtures A034–A052 | ⚪ | |

## P2 — Workflow + prompts coverage

| ID | Item | Status | Notes |
|----|------|--------|-------|
| D1 | Lead-outreach uses skill contracts | ⚪ | Keep dry-run |
| B2 | Revenue agents non-generic prompts | ⚪ | |
| B3 | PR009+ bodies | ⚪ | |

## P3 — Expand + harden

| ID | Item | Status | Notes |
|----|------|--------|-------|
| E1–E3 | Knowledge depth + retrieval | 🟢 | KP packs expanded; `knowledge_store.py` mock default; `test_knowledge_retrieval.py` |
| F1–F3 | CI + secrets + backup evidence | 🟢 | `.github/workflows/quality-gates.yml`; evidence under `docs/improvement/evidence/ops/` |
| C5 | Later agent waves | 🟢 | `docs/improvement/AGENT-WAVES.md` (waves gated on revenue path) |
| D2–D3 | Inbound + marketing workflows | 🟢 | STD-05 parity v1.1; publish gated; cancel path |
| F4 | Production activation sign-off | 🟢 | Checklist requires revenue path testing-green |

## Completed (reference)

| Item | Date |
|------|------|
| Standards STD-01…08 | 2026-09-17 |
| Master Plan v2 | 2026-09-17 |
| Phase scaffolds | 2026-09-17 |
| P0 A1/A3/B1 | 2026-09-17 |
| P1 A2/A4 | 2026-09-17 |
| P3 E/F/D2–D3/C5/F4 | 2026-09-17 |
