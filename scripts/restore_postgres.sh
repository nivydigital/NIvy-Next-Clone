#!/usr/bin/env bash
set -euo pipefail
FILE="${1:-}"
if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  echo "Usage: $0 <backup.sql.gz>" >&2
  exit 1
fi
CONTAINER="${POSTGRES_CONTAINER:-nivy-postgres}"
USER="${POSTGRES_USER:-nivy}"
DB="${POSTGRES_DB:-nivy}"
if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -qx "$CONTAINER"; then
  echo "ERROR: container $CONTAINER not running" >&2
  exit 1
fi
gunzip -c "$FILE" | docker exec -i "$CONTAINER" psql -U "$USER" -d "$DB"
echo "Restore completed from $FILE"
