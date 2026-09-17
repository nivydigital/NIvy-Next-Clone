#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="${NIVY_BACKUP_DIR:-$ROOT/.local-data/backups}"
mkdir -p "$BACKUP_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$BACKUP_DIR/postgres-$STAMP.sql.gz"
CONTAINER="${POSTGRES_CONTAINER:-nivy-postgres}"
USER="${POSTGRES_USER:-nivy}"
DB="${POSTGRES_DB:-nivy}"
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx "$CONTAINER"; then
  docker exec "$CONTAINER" pg_dump -U "$USER" "$DB" | gzip > "$OUT"
else
  echo "-- placeholder backup $STAMP (start postgres for real dump)" | gzip > "$OUT"
  echo "WARN: container $CONTAINER not running — wrote placeholder"
fi
ln -sfn "$(basename "$OUT")" "$BACKUP_DIR/postgres-LATEST.sql.gz"
echo "Backup written: $OUT"
