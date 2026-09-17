# Executable Revenue Pipeline

Canonical runtime path:

`lead intake → discovery → enrichment/verification → scoring → qualification → personalization → approval → outreach → reply triage → follow-up → proposal approval → Odoo CRM update → outcome`

## Runtime controls

1. Read-only intelligence agents may execute without approval when their capabilities are declared.
2. Email, CRM mutation and other external side effects are protected tools and require an approval token unless an explicit future policy grants autonomous authority.
3. Unknown agents/tools are denied by default.
4. Credentials are environment variables/secrets, never registry values.
5. Every runtime call gets a run ID and audit event.
6. Production autonomy requires evaluation and health gates; this repository does not claim that credentials or external accounts are configured.

## Integrations

- Ollama: `OLLAMA_URL`, `OLLAMA_MODEL`
- n8n: `N8N_URL`, `N8N_EMAIL_WEBHOOK`
- Odoo: `ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_PASSWORD`
- PostgreSQL/Redis/Qdrant/MinIO remain the infrastructure services defined by `docker-compose.yml`.

## n8n contract

The runtime calls these webhook contracts; workflows can be imported/adapted from the reusable Raw-Repository catalog:

- `/webhook/nivy/lead-discovery`
- `/webhook/nivy/lead-scoring`
- `/webhook/nivy/outreach-prepare`
- `/webhook/nivy/personalize`
- `/webhook/nivy/qualification`
- `/webhook/nivy/send-email`

No provider-specific credential is committed to the repository.