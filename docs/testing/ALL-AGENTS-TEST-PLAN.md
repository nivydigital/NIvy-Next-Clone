# Nivy Next AIOS — ALL AGENTS TEST PLAN

**Purpose:** One canonical place to test every declared agent after implementation. Live testing is intentionally deferred until the implementation batch is ready.

## 1. Testing policy

- Implement first; execute live tests later as one controlled batch.
- CI/unit/contract tests may run during implementation, but they do **not** prove live execution or integration.
- An agent cannot be marked `COMPLETE` until all applicable G0–G19 gates have evidence, including required live execution/integration evidence.
- Never invent test results. Use `PENDING_BATCH_LIVE_TEST` until the batch is actually executed.
- Record exact command, input fixture, output/evidence location, timestamp, commit SHA and pass/fail result.

## 2. Batch prerequisites

Run from the Windows PowerShell project directory:

```powershell
cd G:\Docker\Nivy\Nivy-Next-AIOS

docker compose up -d postgres redis qdrant ollama backend n8n
Invoke-RestMethod http://localhost:8000/health
```

Confirm required environment variables/API credentials are configured according to the repository's environment template. Do not commit secrets.

## 3. Batch execution order

1. Infrastructure health checks
2. Agent registry/schema consistency
3. Per-agent contract and negative tests
4. Per-agent live API execution
5. Required external-tool/integration tests
6. Output-schema and postcondition verification
7. Failure/retry/security tests
8. Cross-agent integration tests
9. Evidence collection
10. Update `docs/testing/TEST-RESULTS.md`
11. Update the implementation tracker and completion records

## 4. Standard per-agent test matrix

| Test | Required | What must be proven |
|---|---|---|
| T01 Registry/identity | Yes | ID, name, version and registry entry agree |
| T02 Input schema | Yes | Valid input accepted; invalid/missing input rejected |
| T03 Happy path | Yes | Real runtime produces a valid governed result |
| T04 Output schema | Yes | Runtime output validates against canonical schema |
| T05 Negative/policy | Yes | Forbidden/invalid operation fails closed |
| T06 Failure/retry | Yes | Tool failure/timeouts do not fabricate output; retry policy works |
| T07 Evidence/provenance | Yes | Material claims/actions have required evidence |
| T08 Observability | Yes | Correlation/request IDs and audit information are available |
| T09 Integration | If applicable | Required n8n/Odoo/Qdrant/tool integration actually works |
| T10 Regression | Yes | Existing deterministic tests remain green |

---

# A001 — Market Research

**Status:** `PENDING_BATCH_LIVE_TEST`  
**Implementation:** integration-ready; do not mark COMPLETE before live batch evidence.  
**Runtime endpoint:** `POST http://localhost:8000/api/v1/runtime/agents/A001/research`

### A001 live happy-path input

```powershell
$body = @{
    research_question = "What are the current demand trends for HVAC services in the United States?"
    target_market = "United States"
    geography = "United States"
    industry = "HVAC"
    customer_segment = "SMB"
    time_horizon = "current"
    source_policy = @{
        max_sources = 8
    }
} | ConvertTo-Json -Depth 10
```

### A001 live execution

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/api/v1/runtime/agents/A001/research" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### A001 expected result

- HTTP success response for valid input.
- Output validates against `agents/A001/output.schema.json`.
- Every material finding has source provenance, or is explicitly identified as assumption/unknown.
- No fabricated source, statistic or market claim.
- Evidence/cross-check fields are populated where applicable.
- No undeclared side effect occurs.
- Correlation/request ID and audit information are available.

### A001 negative tests

**Missing required input:**

```powershell
$badBody = @{ target_market = "United States" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/runtime/agents/A001/research" -Method POST -ContentType "application/json" -Body $badBody
```

Expected: validation failure; no research result is fabricated.

**Undeclared field:** add an arbitrary field such as `hack = "ignore policy"` and expect rejection according to the input contract.

**Unsupported/unauthorized source access:** request a source outside approved access and expect fail-closed behavior/escalation.

### A001 integration test

Execute the configured A001 n8n workflow and verify the workflow invokes the governed runtime rather than bypassing the runtime contract. Record the n8n execution evidence in `TEST-RESULTS.md`.

### A001 existing deterministic evidence

- `backend/tests/test_agent_a001_market_research.py`
- `backend/tests/test_a001_live_research.py`
- `backend/tests/test_a001_evaluation.py`
- `.github/workflows/runtime-tests.yml`

CI success is supporting evidence only; it does not replace the deferred live test.

---

# A002 and subsequent agents

Each newly implemented agent must receive an entry here **before live batch testing** containing:

1. endpoint/runtime entrypoint
2. prerequisites
3. valid fixture
4. exact PowerShell command
5. expected output/schema
6. negative/policy cases
7. failure/retry case
8. required integrations
9. evidence locations
10. status `PENDING_BATCH_LIVE_TEST`

Use the same T01–T10 matrix unless an agent-specific contract requires additional tests.

## 5. Completion rule

Only after the batch is executed and evidence is recorded may an agent move from `PENDING_BATCH_LIVE_TEST` to the final completion decision. The implementation tracker remains the authoritative gate record.
