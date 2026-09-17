# Progress Tracker — Complete Automation

**Last updated:** 2026-09-17 (Phase 1 tools + Phase 2 prompts complete)
**Owner:** unassigned
Update checkboxes and dates after every meaningful session.

Legend: 🟢 done · 🟡 partial · ⚪ not started · 🔴 blocked

---

## Phase 0 — Inventory & wiring

| ID | Item | Status | Notes |
|----|------|--------|-------|
| P0.1 | Agent folder vs registry diff | ⚪ | |
| P0.2 | Skill/prompt/tool coverage matrix | ⚪ | |
| P0.3 | Runtime API registration for all a0XX | ⚪ | |
| P0.4 | Unified run path documented + coded | ⚪ | |

## Phase 1 — Tools

| ID | Item | Status | Notes |
|----|------|--------|-------|
| P1.1 | Tool registry schemas complete | 🟢 | TOOL-REGISTRY.yaml v2.0 with arg schemas + side_effects |
| P1.2 | Ollama generate hardened | 🟢 | timeouts, JSON format, mock mode |
| P1.3 | Email send + mock | 🟢 | EMAIL_MOCK default; approval-gated |
| P1.4 | Web fetch/crawl + mock | 🟢 | public-data mocks; live opt-in |
| P1.5 | Verification tool mock | 🟢 | tool.email.verify mock + Reacher path |
| P1.6 | Tool audit wrapper | 🟢 | run_id, redacted args, status events |

## Phase 2 — Prompts

| ID | Item | Status | Notes |
|----|------|--------|-------|
| P2.1 | prompts/bodies layout | 🟢 | prompts/bodies/ + README |
| P2.2 | PR001–PR008 executable bodies | 🟢 | executable.yaml v2.0 + bodies/*.md |
| P2.3 | Per-agent prompt mapping | 🟢 | agent-prompt-map.yaml |
| P2.4 | Variable ↔ schema alignment script | 🟢 | scripts/check_prompt_schema_alignment.py |

## Phase 3 — Skills

| ID | Item | Status | Notes |
|----|------|--------|-------|
| P3.1 | All SK* implementation files | ⚪ | registry/definitions only |
| P3.2 | Lead-pipeline skills prioritized | ⚪ | |
| P3.3 | Runtime Agent→Skill→Tool resolve | ⚪ | |
| P3.4 | Skill unit tests | ⚪ | |

## Phase 4 — Lead → Outreach workflow

| ID | Item | Status | Notes |
|----|------|--------|-------|
| P4.1 | workflow.yaml registered | ⚪ | |
| P4.2 | State machine | ⚪ | |
| P4.3 | Idempotency | ⚪ | |
| P4.4 | Dry-run mode | ⚪ | |
| P4.5 | E2E with mocks | ⚪ | |

## Phase 5 — Inbound / comms workflows

| ID | Item | Status |
|----|------|--------|
| P5.1 | Inbound triage workflow | ⚪ |
| P5.2 | Response + QA workflow | ⚪ |
| P5.3 | Conversation/meeting intel hooks | ⚪ |

## Phase 6 — Remaining agents

| ID | Item | Status | Notes |
|----|------|--------|-------|
| P6.1 | A100–A103 | 🟡 | scaffolds present |
| P6.2 | A104–A108 | 🟡 | scaffolds present |
| P6.3 | Status promotion rules applied | ⚪ | after skills/prompts |
