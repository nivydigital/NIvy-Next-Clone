# Backup & Restore Drill (Phase 10 / P10.2)

## Scope

| Asset | Backup method |
|-------|---------------|
| Postgres | `scripts/backup_postgres.sh` → gzipped SQL |
| Knowledge / Qdrant | future object/snapshot jobs |

## Drill

```bash
export NIVY_BACKUP_DIR=./.local-data/backups
./scripts/backup_postgres.sh
./scripts/restore_postgres.sh .local-data/backups/postgres-LATEST.sql.gz
```

Record evidence under `docs/complete-automation-plan/evidence/phase10-backup/`.
