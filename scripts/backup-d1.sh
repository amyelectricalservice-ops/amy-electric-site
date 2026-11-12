#!/usr/bin/env bash
# AMY Electric — D1 backup (AE-048).
#
# Exports every D1 database the site depends on to a dated folder OUTSIDE the
# repo (default ~/amy-backups), gzips it, and prunes copies older than the
# retention window. Backups contain lead PII: keep the folder private, never
# commit it, and never upload it to a public bucket.
#
# Usage:
#   bash scripts/backup-d1.sh                 # remote databases
#   bash scripts/backup-d1.sh --local         # local dev state
#   KEEP_DAYS=60 bash scripts/backup-d1.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${BACKUP_DIR:-$HOME/amy-backups}"
KEEP_DAYS="${KEEP_DAYS:-30}"
STAMP="$(date -u +%Y-%m-%d)"
TARGET="$OUT_DIR/$STAMP"
MODE="--remote"

if [[ "${1:-}" == "--local" ]]; then
  MODE="--local"
  TARGET="$OUT_DIR/local-$STAMP"
fi

mkdir -p "$TARGET"
chmod 700 "$OUT_DIR" "$TARGET"

DB_LIST=(
  "amy-electric-crm"
  "amy-electric-confirmed-db"
)

echo "Backing up to $TARGET ($MODE)"
for db in "${DB_LIST[@]}"; do
  file="$TARGET/$db.sql"
  echo "  → $db"
  if ! npx wrangler d1 export "$db" "$MODE" --output "$file" --no-data 2>/dev/null; then
    # Older wrangler versions need the flag order without --no-data support.
    npx wrangler d1 export "$db" "$MODE" --output "$file"
  fi
  gzip -f "$file"
done

# Manifest (no PII): sizes + checksums so a restore can be verified.
( cd "$TARGET" && shasum -a 256 ./*.sql.gz > SHA256SUMS.txt && ls -lh ./*.sql.gz >> SHA256SUMS.txt )

# Prune old dated folders.
find "$OUT_DIR" -maxdepth 1 -type d -name '20*-*-*' -mtime "+$KEEP_DAYS" -print -exec rm -rf {} + 2>/dev/null || true

echo "Done. Files:"
ls -lh "$TARGET"
echo
echo "Restore:  gunzip -c $TARGET/amy-electric-crm.sql.gz | npx wrangler d1 execute amy-electric-crm --remote --file=/dev/stdin"
