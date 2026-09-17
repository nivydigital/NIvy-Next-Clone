# Deferred Testing Plan for All Agents

**Status:** Active policy override (user direction 2026-09-17)  
**Rule:** Full testing deferred until final phase. No agent marked COMPLETE until then.

## How (final phase)
Contract → unit happy-path → negative/policy → schema/golden → eval → integration → regression.

## Coverage inventory

### Prior ranges
A001–A033 strategy; A034–A060 lead/sales; A065–A077 CS/comms; A078–A083 finance — as previously documented.

### Marketing (A084–A089)
| ID | Name | Extra asserts |
|----|------|---------------|
| A084 | Marketing Strategist | pillars, channel_priorities, messaging_themes |
| **A085** | **Content Strategist** | **pillars, formats, calendar_outline, success_metrics** |
| **A086** | **SEO Strategist** | **keyword_themes, content_opportunities, technical_priorities** |
| **A087** | **Social Media Strategist** | **channel_mix, content_types, engagement_plays** |
| **A088** | **Paid Media Analyst** | **performance_summary, budget_recommendations, creative_recommendations** |
| **A089** | **Marketing Analytics** | **channel_summary, top_insights, recommended_experiments** |

### Higher IDs
A117–A127 existing — deferred.

### Not yet implemented
A090 Growth Experiment Planner, A091 Campaign QA Reviewer, A092+ control/eval/learning.

## Chain tests (final phase)
1. Lead: A034→A039→A041→A043→A044  
2. Comms: A066→A068→A071  
3. CS: A065→A072→A073→A075→A076  
4. Finance: A078→A079→A080→A081  
5. Marketing: A084→A085→A086/A087→A088→A089→A090  

## Maintenance
Update on every new batch. Do not mark COMPLETE until final testing phase.
