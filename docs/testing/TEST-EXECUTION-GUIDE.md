# Nivy Next AIOS — Test Execution Guide

## Purpose

Use this guide when the implementation batch is ready for live validation. Do not run live agent tests merely to move an implementation forward; the project policy is to test the agents together after implementation.

## 1. Prepare environment

PowerShell:

```powershell
cd G:\Docker\Nivy\Nivy-Next-AIOS

docker compose up -d postgres redis qdrant ollama backend n8n
```

Health check:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

If health fails, stop the batch and fix infrastructure first.

## 2. Run deterministic/contract tests

Run the repository's normal test suite first. For the current A001 implementation, the relevant tests are:

```powershell
python -m pytest backend/tests/test_agent_a001_market_research.py backend/tests/test_a001_evaluation.py backend/tests/test_a001_live_research.py -q
```

These tests establish implementation-level evidence. They are not a substitute for live tool/API/integration testing.

## 3. Execute live agents

Use `ALL-AGENTS-TEST-PLAN.md` as the canonical per-agent runbook. Execute agents in registry/implementation order and record each result immediately.

For each agent capture:

- date/time
- commit SHA
- agent ID/version
- environment
- exact fixture/input
- exact command
- HTTP/status result where applicable
- output validation result
- integration evidence
- failures/retries
- log/audit/correlation identifiers
- final PASS/FAIL/BLOCKED

## 4. Negative testing

Every applicable agent must be tested with:

- missing required input
- malformed input
- undeclared field/tool
- unauthorized operation/source
- dependency/tool failure
- timeout/retry condition
- prompt-injection or instruction-conflict fixture where the agent consumes untrusted text

Expected behavior is governed rejection/escalation/fail-closed behavior, not a plausible fabricated answer.

## 5. Evidence standard

A test is PASS only when the required observable evidence exists. A response that merely looks correct is insufficient for integration, provenance, side-effect, or audit gates.

Store durable test evidence in the repository only when it contains no secrets or sensitive customer data. Redact credentials, tokens, private personal data and confidential payloads.

## 6. Batch completion

After all agents are tested:

1. update `docs/testing/TEST-RESULTS.md`;
2. update each agent's completion record;
3. update `docs/agent-implementation-plan/AGENT-PROGRESS-TRACKER.md`;
4. verify G12/G16/G17/G19/G20 evidence for each applicable agent;
5. only then mark the agent `COMPLETE` and unlock the next agent according to the sequencing rule.
