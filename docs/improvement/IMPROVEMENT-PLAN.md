# Nivy AIOS — Improvement Plan

**Version:** 1.0  
**Date:** 2026-09-17  
**Standards baseline:** `docs/standards/` STD-01 … STD-08  
**Planning baseline:** `docs/complete-automation-plan/MASTER-IMPLEMENTATION-PLAN-v2.md`

---

## 1. Purpose

Prior phases established **structure** (registries, schemas, mocks, state machines, ops checklists).  
They did **not** fully deliver an **international-grade operating system**.

This plan closes the gap between scaffolds and production-grade capabilities.

**Principle:** Prefer fewer **active** capabilities that meet standards over many empty IDs.

---

## 2. Current-state summary (honest)

### 2.1 What is usable today

- **Tools:** Registry + runtime with mocks, side-effect flags, audit redaction
- **Prompts:** PR001–PR008 bodies + executable.yaml + agent map
- **Workflows:** Lead-outreach state machine with idempotency + dry-run
- **Knowledge:** KP001–KP008 packs + mock ingest pipeline
- **Ops:** Secrets policy, backup scripts, production checklist, dashboard spec
- **Standards:** STD-01…08 published
- **Agents:** Many schemas + Python runtimes (coverage uneven)

### 2.2 What is thin or incomplete

| Area | Gap |
|------|-----|
| **Skills** | Generic templates; not domain-deep; not unit-tested end-to-end |
| **Prompts** | Only 8 core bodies; generic fallbacks; runtime load path incomplete; no evaluation evidence |
| **Agents** | Scaffold ≠ complete; few golden fixtures; almost none truly `active` |
| **Workflows** | Mock step artifacts, not full skill+prompt execution |
| **Knowledge** | Bootstrap-length pack text; live stores not certified |
| **Memory** | Policy only; no full memory service |
| **Evaluation** | Deferred tests not systematically executed |
| **Live integrations** | Email/CRM/web not production-certified |

### 2.3 Folders — keep and deepen (do not delete)

`agents/`, `skills/`, `prompts/`, `tools/`, `workflows/`, `knowledge/`, `memory/`, `ops/`, `backend/app/runtime/`, `docs/standards/`, `docs/complete-automation-plan/`

---

## 3. Improvement goals

1. **Standardization** — Meet STD-01…08 for each capability type.
2. **Depth** — Role-specific procedures and prompts, not one template for all.
3. **Integration** — Runtime: validate → execute → audit (fail-closed).
4. **Evidence** — Tests and fixtures before status promotion.
5. **Governed production** — Side effects only after dry-run + signed checklist.

---

## 4. Work packages

### WP-A — Skills system (highest leverage)

| ID | Task | Exit criteria |
|----|------|----------------|
| A1 | All 50 SK*.yaml on main; validate script green | `validate_skills_std01.py` → OK |
| A2 | Deepen lead-path skills SK034–SK050 | Non-generic execute_core; owner set |
| A3 | Runtime skill resolver | Fail-closed integration test |
| A4 | Unit tests SK034–SK050 | CI green |
| A5 | Promote lead-path skills to `testing` | Evidence folder present |

### WP-B — Prompts

| ID | Task | Exit criteria |
|----|------|----------------|
| B1 | Runtime loads bodies from prompts/ | Shared loader + test |
| B2 | Revenue-path agents non-generic primary prompt | Map review |
| B3 | PR009+ full bodies under bodies/ | Files + registry + executable |
| B4 | Variables aligned to input schemas | Alignment script green |
| B5 | Golden JSON shape fixtures for PR001–PR008 | evidence/prompts/ |

### WP-C — Agents (depth, not only coverage)

| ID | Task | Exit criteria |
|----|------|----------------|
| C1 | Refresh AGENT-COMPLETENESS-MATRIX.yaml | Script output committed |
| C2 | Fix A034–A052 completeness first | Matrix: runtime + skills_resolved |
| C3 | Golden fixtures A034–A052 | Fixtures + pytest |
| C4 | Enforce status ladder | No `active` without STD-02 checklist |
| C5 | Later agent waves | After revenue path |

### WP-D — Workflows

| ID | Task | Exit criteria |
|----|------|----------------|
| D1 | Lead-outreach calls skill contracts (dry-run) | Tests pass |
| D2 | Inbound/comms workflow STD-05 parity | yaml + runtime + tests |
| D3 | Marketing workflows, publish gated | Dry-run default |

### WP-E — Knowledge, memory, RAG

| ID | Task | Exit criteria |
|----|------|----------------|
| E1 | Expand KP packs with reviewable sections | Freshness + review note |
| E2 | Live store path behind env flags | Mock default in CI |
| E3 | Retrieval used by research/outreach agents | Integration test |

### WP-F — Quality, security, ops

| ID | Task | Exit criteria |
|----|------|----------------|
| F1 | CI: skill validate, prompt align, contract tests | Documented or Action |
| F2 | Secret scanner in CI | check_no_secrets_in_git.py |
| F3 | Backup restore drill evidence | evidence/ops/ |
| F4 | Production activation only when revenue path testing-green | STD-08 |

---

## 5. Priority order

```text
P0  A1 → A3 → B1        Skills on main + resolver + prompt loader
P1  A2 → A4 → C2 → C3   Lead-path depth + tests + fixtures
P2  D1 → B2 → B3        Workflow wiring + prompt coverage
P3  E* → F* → C5        Knowledge, CI, later agents
```

Do **not** chase “all 127 agents active” before P0–P1 complete.

---

## 6. Program definition of done

1. Lead revenue path dry-run uses **real skill + prompt contracts**.
2. SK001–SK050 pass STD-01 validation; lead-path skills have domain depth + unit tests.
3. Prompt loader is the single path for agent LLM calls.
4. Completeness matrix regeneratable on demand.
5. No capability marked `active` without evidence.
6. Secrets, backup, activation checklist mandatory for production.

---

## 7. Out of scope

- Full production autonomy for all agents without evidence
- Bulk-loading untrusted documents into RAG
- Live email/CRM without dry-run proof and approval process
- Full monorepo rewrite

---

## 8. Tracking

| Artifact | Location |
|----------|----------|
| Backlog | `docs/improvement/PRIORITY-BACKLOG.md` |
| Scorecard | `docs/improvement/DEPTH-SCORECARD.md` |
| Evidence | `docs/improvement/evidence/` |
| Standards | `docs/standards/` |

---

## 9. First actions

1. Ensure all STD-01 skills committed (A1).
2. Implement skill resolver (A3).
3. Implement prompt body loader (B1).
4. Deepen SK034, SK036, SK039, SK044, SK049 (start of A2).
5. Pytest for resolver + loader + three skills.

---

*End of Improvement Plan v1.0*
