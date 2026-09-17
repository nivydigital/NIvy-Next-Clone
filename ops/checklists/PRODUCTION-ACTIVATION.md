# Production Activation Checklist (Phase 10 / P3 F4 / STD-08)

Aligned with `docs/DEFINITION-OF-DONE.md` and Improvement Plan F4.

**Hard gate:** Revenue path (lead-outreach dry-run + SK034–SK050 tests) must be **testing-green** before any live side effects.

## A. Security

- [ ] `python3 scripts/check_no_secrets_in_git.py` → OK
- [ ] CI job `quality-gates` secret scan green on main
- [ ] `.env` not in Git; secrets in env/secret store
- [ ] Strong unique `POSTGRES_PASSWORD` and provider keys
- [ ] Protected tools require approval
- [ ] Audit redaction verified

## B. Data durability

- [ ] Postgres backup script succeeds
- [ ] Restore drill documented in `docs/improvement/evidence/ops/BACKUP-RESTORE-DRILL.md`
- [ ] Backup retention set

## C. Runtime / workflows (revenue path first)

- [ ] `pytest backend/app/test_lead_skills.py` green
- [ ] Lead-outreach dry-run E2E green (`skill_contracts: true`)
- [ ] Knowledge retrieval mock tests green (`NIVY_KNOWLEDGE_STORE=mock`)
- [ ] Live email only after approval process is live
- [ ] Knowledge packs ingested / freshness reviewed
- [ ] Inbound + marketing workflows remain `dry_run_default: true` until separately signed

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

**Activation without complete sign-off is out of policy.**
