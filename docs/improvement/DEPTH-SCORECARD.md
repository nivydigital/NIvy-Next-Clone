# Depth Scorecard

**Purpose:** Score capabilities so “file exists” is not confused with “production ready.”

**Last updated:** 2026-09-17

## Scoring (0–5)

| Score | Meaning |
|-------|---------|
| 0 | Missing |
| 1 | ID declared only |
| 2 | Scaffold (yaml/schema without real procedure) |
| 3 | Implementation (procedure/runtime, mock OK) |
| 4 | Testing (automated tests + fixtures) |
| 5 | Active (evidence + checklist + owner) |

## Target minimums

| Area | Now (approx) | After P0–P1 | Production |
|------|----------------|-------------|------------|
| Lead-path skills | 2–3 | 4 | 4–5 |
| Other skills | 1–3 | 3 | 3–4 |
| Core prompts PR001–8 | 3 | 4 | 4–5 |
| Other prompts | 1–2 | 3 | 3–4 |
| Lead-outreach workflow | 3 | 4 | 4–5 |
| Tools (mock) | 3–4 | 4 | 4 |
| Tools (live) | 2 | 2–3 | 4–5 |
| Knowledge packs | 2–3 | 3 | 4 |
| Agents A034–A052 | 2–3 | 4 | 4–5 |
| Other agents | 1–3 | 2–3 | per wave |

## Rule

Do not raise registry status above score 3 without tests (score ≥ 4).
