# Phase 8 — Marketing workflows

**Status:** 🟢 Implemented (dry-run default)

## Workflows

| ID | Path | Agents |
|----|------|--------|
| content-calendar | `workflows/content-calendar/workflow.yaml` | A085, A084, A091 |
| seo-audit | `workflows/seo-audit/workflow.yaml` | A086, A085, A089 |
| social-content-pipeline | `workflows/social-content-pipeline/workflow.yaml` | A087, A085, A091 |

## Plan mapping

| Plan item | Workflow |
|-----------|----------|
| P8.1 Content calendar | content-calendar |
| P8.2 SEO audit | seo-audit |
| P8.3 Social pipeline | social-content-pipeline |

## Run (dry-run)

```http
POST /api/v1/runtime/workflows/content-calendar/run
{
  "dry_run": true,
  "payload": {
    "input": {
      "marketing_strategy": {"goals": ["demand gen"], "audience": "SMB"},
      "content_constraints": {"cadence": "weekly"}
    }
  }
}
```

Same pattern for `seo-audit` and `social-content-pipeline`.

## Policy

- No auto-publish (approval gates)
- Public-data / evidence-backed agent policies apply
- Side effects none until separate publish path is authorized
