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
2. **Unit / happy-path tests**
3. **Negative / policy tests**
4. **Output & schema tests**
5. **Evaluation suite**
6. **Integration / live proof**
7. **Regression**

(Details unchanged from prior version — same 7-step pyramid applies to all agents.)

---

## Agent coverage inventory (what must be tested)

### Strategy track
| ID range | Focus |
|----------|--------|
| A001–A002 | Market Research, ICP Strategist |
| A003–A033 | Strategy chain (extension implementations) |

### Lead & sales ops
| ID | Name | Extra asserts |
|----|------|---------------|
| A034–A038 | Discovery → Verification | provenance; no fabricated entities |
| A039 | Lead Scoring | scores, breakdown, priority_order |
| A041 | Account Research | signals, talking_points, sources |
| A043–A044 | Outreach plan + Email | draft-only default; compliance_checks |
| A049–A050 | Personalization + Follow-Up | do_not_use; timing_guidance |
| A052–A055 | Triage → Meeting Prep | classification; handoff; agenda |
| A060 | Proposal | sections, pricing_block; draft-only |

### Onboarding & communications
| ID | Name | Extra asserts |
|----|------|---------------|
| A065 | Onboarding Agent | steps, milestones, owners |
| A066–A071 | Comms suite | intent/route; objections; pass_fail/score |

### Customer success
| ID | Name | Extra asserts |
|----|------|---------------|
| A072 | Customer Onboarding Planner | tasks, timeline, checkpoints |
| A073 | Customer Health Analyst | health_score, risk_flags, expansion_signals |
| A074 | Support Triage | severity, category, playbook |
| **A075** | **Customer Success Planner** | **motions, timeline, owners, success_metrics** |
| **A076** | **Renewal Risk Analyst** | **risk_score, risk_drivers, save_plays, urgency** |
| **A077** | **Feedback & NPS Analyst** | **themes, nps_summary, promoter/detractor_actions** |

### Finance (started)
| ID | Name | Extra asserts |
|----|------|---------------|
| **A078** | **Billing Analyst** | **anomalies, dispute_candidates, process_recommendations** |
| **A079** | **Accounts Receivable Analyst** | **priority_accounts, aging_summary, collection_actions** |

### Higher IDs already on disk
| ID range | Notes |
|----------|--------|
| A117–A127 | Existing folders; full pyramid deferred |

### Not yet implemented
A080–A083 (AP, cashflow, pricing, revenue analytics), A084+ marketing, A092+ control/eval/learning — append rows when built.

---

## Suggested chain tests (final phase)

1. Lead: A034 → A036 → A039 → A041 → A043 → A044  
2. Comms: A066 → A068 → A071  
3. CS: A065 → A072 → A073 → A075 → A076  
4. Finance smoke: A078 → A079  
5. Live Ollama one-shot per agent or per chain  
6. Mark COMPLETE only after pyramid passes

---

## Maintenance rule

Update this file on every new agent batch with IDs, extra asserts, and chain notes. Do **not** mark agents COMPLETE until final testing phase.
