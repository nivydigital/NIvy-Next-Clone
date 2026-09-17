# Deferred Testing Plan for All Agents

**Status:** Active policy override (user direction 2026-09-17)  
**Rule:** Full automated testing, evaluation suites, live integration evidence and G16/G17 gates are **deferred** until the final testing phase for the entire agent set.

## Policy

- Implementation of agents continues without requiring passing unit/integration/evaluation tests for each agent.
- Every agent still receives:
  - Complete `agent.yaml` specification
  - Input / output JSON schemas
  - Runtime adapter (`backend/app/runtime/a0XX.py`)
  - Registry / binding updates as needed
- **No agent is marked COMPLETE or ACTIVE** until the final testing phase is executed.
- The final testing phase will apply the full G0–G20 gates, the AGENT-BUILD-MASTER-PROMPT testing pyramid, and live evidence requirements.

---

## How testing will be performed (final phase)

For **every** agent the final testing phase will execute the same pyramid:

1. **Contract / registry tests**
   - Agent ID exists in `agents/registry.yaml` and/or `implementation-registry.yaml`
   - Skill / prompt / knowledge IDs resolve
   - `input.schema.json` and `output.schema.json` validate as JSON Schema
   - Runtime module importable; entrypoint name matches convention

2. **Unit / happy-path tests**
   - Valid required inputs → status success|partial
   - Output validates against output schema
   - `confidence` ∈ {high, medium, low}
   - Required array/object fields present and correctly typed
   - `assumptions` and `derived_from` are non-empty lists when model returns success

3. **Negative / policy tests**
   - Missing required inputs → agent-specific Error (fail closed)
   - Non-JSON model output → agent-specific Error
   - Invalid confidence value → Error
   - Only allowed tools (default `tool.ollama.generate`); no unexpected side effects
   - Agents with `external_actions: prohibited_by_default` must not call send/deploy APIs in default path

4. **Output & schema tests**
   - Round-trip: output dict validates against output.schema.json
   - Golden fixtures (min 3 per agent) for representative scenarios

5. **Evaluation suite**
   - Quality rubric: evidence-backed, no fabricated claims, uncertainty explicit
   - Downstream next_action points to a real next agent or human step

6. **Integration / live proof**
   - Runtime entrypoint callable with local Ollama (or configured LLM) when credentials available
   - Optional: chain 2–3 agents (e.g. A034→A036→A039) with fixture data

7. **Regression**
   - Re-run prior golden cases after any runtime/engine change

---

## Agent coverage inventory (what must be tested)

### Strategy track (extension implementations)
| ID range | Focus | Notes for final test |
|----------|--------|----------------------|
| A001–A002 | Market Research, ICP Strategist | Registry + early completion records exist; full G16–G20 still deferred |
| A003–A033 | Strategy chain (positioning, messaging, offer, GTM, campaign, enablement, etc.) | Implemented as sequential strategy layer; verify against agent.yaml contracts even if not all IDs appear in canonical registry |

### Lead & sales ops (registry-aligned)
| ID | Name | What to test (beyond pyramid) |
|----|------|-------------------------------|
| A034 | Lead Discovery | Multi-source style fields; provenance; no fabricated company lists |
| A035 | Contact Discovery | Contact fields; role/title consistency with ICP |
| A036 | Lead Enrichment | Enrichment completeness; freshness/confidence |
| A037 | Data Quality | Dedup/cleanup flags; quality scores |
| A038 | Verification | Verification status; fail-closed on unverifiable claims |
| A039 | Lead Scoring | Scores + breakdown + priority_order; strategy linkage |
| A041 | Account Research | Signals + talking_points + sources |
| A043 | Outreach Strategy (ops) | channel_mix, sequence_outline, messaging_angles |
| A044 | Email Outreach | drafts only by default; compliance_checks present |
| A049 | Personalization | hooks + do_not_use boundaries |
| A050 | Follow-Up | trigger_reason + timing_guidance; draft-only default |
| A052 | Reply Triage | classification + recommended_action + urgency |
| A054 | Qualification | status_per_lead + criteria_met + handoff_recommendation |
| A055 | Meeting Prep | agenda, talking_points, risks, questions |
| A060 | Proposal Agent | sections, value_summary, pricing_block; draft-only default |

### Onboarding & communications (registry-aligned)
| ID | Name | What to test (beyond pyramid) |
|----|------|-------------------------------|
| A065 | Onboarding Agent | steps, milestones, owners, success_criteria |
| A066 | Inbound Communication Triage | intent, urgency, route_to, summary |
| A067 | Conversation Intelligence | objections, commitments, sentiment, next_best_actions |
| A068 | Response Drafting | draft + tone + compliance_checks |
| A069 | Meeting Intelligence | decisions, action_items, risks, follow_ups |
| A070 | Communication Knowledge Extractor | faqs, objection_handlers, playbook_snippets, tags |
| A071 | Communication Quality Reviewer | pass_fail, issues, suggested_edits, score |

### Customer success (registry-aligned)
| ID | Name | What to test (beyond pyramid) |
|----|------|-------------------------------|
| A072 | Customer Onboarding Planner | tasks, timeline, owners, checkpoints |
| A073 | Customer Health Analyst | health_score, risk_flags, expansion_signals, recommended_actions |
| A074 | Support Triage | severity, category, route_to, playbook |

### Already present higher IDs
| ID range | Focus | Notes |
|----------|--------|-------|
| A117–A127 | (existing folders) | Contract/registry + golden cases as listed in prior section; still deferred to final phase |

### Not yet implemented (will be added when built)
A075–A077 (CS planner, renewal risk, NPS), A078+ finance, A084+ marketing, A092+ control/eval/learning — add a row to this file in the same format when each batch is implemented.

---

## Suggested final-phase execution order

1. Registry + schema contract suite for all agents with folders under `agents/`
2. Unit/negative tests per runtime module under `backend/app/runtime/`
3. Golden fixtures directory e.g. `tests/fixtures/agents/A0XX/`
4. Optional chain tests: Lead pipeline A034→A039→A041→A043→A044
5. Optional chain tests: Comms A066→A068→A071
6. Optional chain tests: CS A065→A072→A073→A074
7. Live Ollama smoke (one call per agent or per chain)
8. Update AGENT-PROGRESS-TRACKER and only then mark COMPLETE

---

## Maintenance rule

Whenever a new agent batch is implemented, **update this file** with:
- Agent IDs and names
- Any agent-specific fields or policy quirks to assert
- Suggested chain tests if the batch closes a pipeline segment

Do **not** mark any agent COMPLETE until this plan is executed in full.
