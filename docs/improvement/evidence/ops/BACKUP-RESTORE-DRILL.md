# Backup Restore Drill Evidence (P3 F3)

**Date:** 2026-09-17  
**Operator:** automated scaffold / ops  
**Environment:** local / CI-safe documentation (no live Postgres required for this evidence pack)

## Scope

| Asset | Method | Script |
|-------|--------|--------|
| Postgres | gzipped SQL dump | `scripts/backup_postgres.sh` |
| Postgres restore | gunzip + psql | `scripts/restore_postgres.sh` |

## Procedure (copy for live drill)

```bash
export NIVY_BACKUP_DIR=./.local-data/backups
mkdir -p "$NIVY_BACKUP_DIR"
./scripts/backup_postgres.sh
# Inspect: ls -la .local-data/backups/
./scripts/restore_postgres.sh .local-data/backups/postgres-LATEST.sql.gz
```

## Results (template — fill on live drill)

| Check | Result | Notes |
|-------|--------|-------|
| Backup script exit 0 | ☐ | |
| Artifact non-empty | ☐ | path: |
| Restore exit 0 | ☐ | |
| Spot-check table counts | ☐ | |
| Duration | ☐ | minutes: |

## Policy notes

- CI does **not** run live Postgres restore; this evidence file satisfies process documentation.
- Live drill must be recorded here before production activation (see `ops/checklists/PRODUCTION-ACTIVATION.md`).
- Retention: keep last N dumps per `ops/backup/BACKUP-RESTORE.md`.

## Sign-off

| Role | Name | Date |
|------|------|------|
| Ops |  |  |
| Engineering |  |  |
