# Production Activation Checklist (Phase 10 / P10.4)

Aligned with `docs/DEFINITION-OF-DONE.md`.

## A. Security

- [ ] `python3 scripts/check_no_secrets_in_git.py` → OK
- [ ] `.env` not in Git; secrets in env/secret store
- [ ] Strong unique `POSTGRES_PASSWORD` and provider keys
- [ ] Protected tools require approval
- [ ] Audit redaction verified

## B. Data durability

- [ ] Postgres backup script succeeds
- [ ] Restore drill documented
- [ ] Backup retention set

## C. Runtime / workflows

- [ ] Lead-outreach dry-run E2E green
- [ ] Live email only after approval process is live
- [ ] Knowledge packs ingested

## D. Observability

- [ ] Audit events flowing
- [ ] Dashboard panels reviewed
- [ ] Alerts on tool errors / failed workflows

## E. Definition of Done

- [ ] Implementation, integration, schemas, errors, persistence, security, observability, tests, docs, acceptance

## Sign-off

| Role | Name | Date |
|------|------|------|
| Engineering |  |  |
| Ops / Security |  |  |
| Product owner |  |  |
