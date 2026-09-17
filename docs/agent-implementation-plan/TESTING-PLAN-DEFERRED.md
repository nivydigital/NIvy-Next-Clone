# Deferred Testing Plan for All Agents

**Status:** Active policy override (user direction 2026-09-17)  
**Rule:** Full testing deferred until final phase. No agent marked COMPLETE until then.

## How (final phase)
Contract → unit happy-path → negative/policy → schema/golden → eval → integration → regression (same pyramid for every agent).

## Coverage inventory

### Strategy / Lead / Sales / Comms / CS
A001–A033 strategy track; A034–A060 lead/sales; A065–A071 comms; A072–A077 CS — as previously documented.

### Finance (complete through A083)
| ID | Name | Extra asserts |
|----|------|---------------|
| A078 | Billing Analyst | anomalies, dispute_candidates |
| A079 | AR Analyst | priority_accounts, aging_summary, collection_actions |
| **A080** | **AP Analyst** | **due_summary, payment_priorities, risk_flags** |
| **A081** | **Cashflow Analyst** | **projection, shortfall_flags, surplus_opportunities** |
| **A082** | **Pricing Analyst** | **performance_summary, recommended_changes, experiments** |
| **A083** | **Revenue Analytics** | **trend_summary, cohort_insights, drivers** |

### Marketing (started)
| ID | Name | Extra asserts |
|----|------|---------------|
| **A084** | **Marketing Strategist** | **pillars, channel_priorities, messaging_themes, success_metrics** |

### Higher IDs
A117–A127 existing folders — deferred.

### Not yet implemented
A085 Content Strategist, A086 SEO, A087 Social, A088 Paid Media, A089 Marketing Analytics, A090 Growth Experiment Planner, A091 Campaign QA, then A092+ control/eval/learning.

## Chain tests (final phase)
1. Lead: A034→A039→A041→A043→A044  
2. Comms: A066→A068→A071  
3. CS: A065→A072→A073→A075→A076  
4. Finance: A078→A079→A080→A081 (+ A082/A083)  
5. Marketing smoke: A084→A085 (when built)  

## Maintenance
Update this file on every new batch. Do not mark COMPLETE until final testing phase.
