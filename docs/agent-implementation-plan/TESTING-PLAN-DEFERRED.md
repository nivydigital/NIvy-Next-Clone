# Deferred Testing Plan for All Agents

**Status:** Active policy override (user direction 2026-09-17)  
**Rule:** Full testing deferred until final phase. No agent marked COMPLETE until then.

## How (final phase)
Contract → unit happy-path → negative/policy → schema/golden → eval → integration → regression.

## Coverage inventory

### Prior ranges
A001–A033 strategy; A034–A060 lead/sales; A065–A077 CS/comms; A078–A083 finance; A084–A089 marketing — as previously documented.

### Marketing close + Control start (A090–A094)
| ID | Name | Extra asserts |
|----|------|---------------|
| **A090** | **Growth Experiment Planner** | **hypotheses, variants, success_metrics, run_plan** |
| **A091** | **Campaign QA Reviewer** | **pass_fail, issues, suggested_fixes, score** |
| **A092** | **KPI Intelligence Analyst** | **variance_summary, drivers, recommended_actions** |
| **A093** | **Planning Analyst** | **priorities, workstreams, owners, checkpoints** |
| **A094** | **Anomaly Detection Analyst** | **anomalies, severity, investigation_paths** |

### Higher IDs
A117–A127 existing — deferred.

### Not yet implemented
A095 Risk Analyst, A096 Executive Intelligence, A097 Resource Planning, A098–A103 evaluation, A104–A108 learning.

## Chain tests (final phase)
1. Lead: A034→A039→A041→A043→A044  
2. Comms: A066→A068→A071  
3. CS: A065→A072→A073→A075→A076  
4. Finance: A078→A079→A080→A081  
5. Marketing: A084→A085→A089→A090→A091  
6. Control: A092→A093→A094  

## Maintenance
Update on every new batch. Do not mark COMPLETE until final testing phase.
