# Deferred Testing Plan for All Agents

**Status:** Active policy override (user direction 2026-09-17)  
**Rule:** Full testing deferred until final phase. No agent marked COMPLETE until then.

## How (final phase)
Contract → unit happy-path → negative/policy → schema/golden → eval → integration → regression.

## Coverage inventory

### Prior ranges
A001–A094 as previously documented (strategy, lead, CS, finance, marketing, control start).

### Control + Evaluation start (A095–A099)
| ID | Name | Extra asserts |
|----|------|---------------|
| **A095** | **Risk Analyst** | **risks, severity, mitigations, residual_risk** |
| **A096** | **Executive Intelligence Analyst** | **summary, key_decisions, asks, risks_opportunities** |
| **A097** | **Resource Planning Analyst** | **allocations, gaps, reallocation_options** |
| **A098** | **Evaluation Analyst** | **scores, findings, pass_fail, recommendations** |
| **A099** | **Regression QA Agent** | **regressions, severity, pass_fail, recommended_fixes** |

### Higher IDs
A117–A127 existing — deferred.

### Not yet implemented
A100 Trace Auditor, A101 Runtime Quality Monitor, A102 Cost Observability, A103 Evidence Collector, A104–A108 learning agents.

## Chain tests
Control: A092→A093→A094→A095→A096→A097  
Eval: A098→A099→A100 (when built)

## Maintenance
Update on every new batch. Do not mark COMPLETE until final testing phase.
