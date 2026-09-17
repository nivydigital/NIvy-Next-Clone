# Phase 6 — Remaining agents & promotion

**Status:** 🟢 Complete (A100–A108 scaffolds + promotion rules)

## Agents A100–A108

| ID | Name | Runtime |
|----|------|---------|
| A100 | Trace Auditor | `run_a100_trace_auditor` |
| A101 | Runtime Quality Monitor | `run_a101_runtime_quality` |
| A102 | Cost Observability Analyst | `run_a102_cost_observability` |
| A103 | Evidence Collector | `run_a103_evidence_collector` |
| A104 | Feedback Analyst | `run_a104_feedback_analyst` |
| A105 | Prompt Improvement Agent | `run_a105_prompt_improvement` |
| A106 | Skill Improvement Agent | `run_a106_skill_improvement` |
| A107 | Experiment Manager | `run_a107_experiment_manager` |
| A108 | Regression Guard | `run_a108_regression_guard` |

Each has: `agents/A1xx/{agent.yaml,input.schema.json,output.schema.json}` + `backend/app/runtime/a1xx.py`.

## Promotion rules (P6.3)

`declared` → `implementation` when **all** true:

1. Agent folder + `agent.yaml`
2. `input.schema.json` + `output.schema.json`
3. Runtime module with `async def run_a1xx_*`
4. `agent.yaml` runtime.adapter + entrypoint

**Not** promoted to production without deferred evaluation suite.

Script: `python scripts/promote_agents.py`

## Execute via unified API

```http
POST /api/v1/runtime/agents/A100/execute
{"payload": {"trace_bundle": {}, "policy_baseline": {}}}
```

(Discovery lists structured entrypoints when modules are present.)
