#!/bin/bash
# build_gallery.sh — AMY Electric Gallery Pipeline
# Processes raw images using photo_manifest.csv, generates SQL, uploads to R2
#
# Usage: ./build_gallery.sh [--upload] [--db] [--manifest-only]
#   --upload        Also upload to R2 after processing
#   --db            Also seed D1 database after processing
#   --manifest-only Just regenerate SQL from manifest (skip image processing)

set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SOURCE_DIR="/home/amram/Pictures/Photos-website"
PROCESSED_DIR="${SCRIPT_DIR}/processed"
SQL_DIR="${SCRIPT_DIR}/sql"
SQL_FILE="${SQL_DIR}/batch_insert.sql"
MANIFEST="${SCRIPT_DIR}/photo_manifest.csv"

R2_BUCKET="amyelectric-gallery"
R2_REMOTE="r2:amyelectric-gallery"
D1_DB="amyelectric_db"

# Image settings
MAX_WIDTH=1200
QUALITY=85
WEBP_QUALITY=80

# ─── Functions ───────────────────────────────────────────────────────────────

log() {
  echo -e "\033[1;36m[$(date '+%H:%M:%S')]\033[0m $*"
}

warn() {
  echo -e "\033[1;33m[$(date '+%H:%M:%S') WARNING]\033[0m $*"
}

error() {
  echo -e "\033[1;31m[$(date '+%H:%M:%S') ERROR]\033[0m $*" >&2
  exit 1
}

# Read manifest CSV into parallel arrays (bash 3 compatible)
declare -a MANIFEST_FILENAME=()
declare -a MANIFEST_FOLDER=()
declare -a MANIFEST_CATEGORY=()
declare -a MANIFEST_DESCRIPTION=()
declare -a MANIFEST_LOCATION=()
declare -a MANIFEST_DATE=()

load_manifest() {
  if [ ! -f "$MANIFEST" ]; then
    error "Manifest not found: $MANIFEST\nRun generate_manifest.py first."
  fi

  log "Loading manifest from ${MANIFEST}..."

  # Skip header, read CSV
  local i=0
  while IFS=, read -r filename folder category description location date; do
    MANIFEST_FILENAME[$i]="$filename"
    MANIFEST_FOLDER[$i]="$folder"
    MANIFEST_CATEGORY[$i]="$category"
    MANIFEST_DESCRIPTION[$i]="$description"
    MANIFEST_LOCATION[$i]="$location"
    MANIFEST_DATE[$i]="$date"
    i=$((i + 1))
  done < <(tail -n +2 "$MANIFEST")

  log "Loaded ${i} entries from manifest"
}

# Look up a file in the manifest
lookup_manifest() {
  local filename="$1"
  for i in "${!MANIFEST_FILENAME[@]}"; do
    if [ "${MANIFEST_FILENAME[$i]}" = "$filename" ]; then
      echo "${MANIFEST_CATEGORY[$i]}|${MANIFEST_DESCRIPTION[$i]}|${MANIFEST_LOCATION[$i]}|${MANIFEST_DATE[$i]}"
      return 0
    fi
  done
  return 1
}

# Get image dimensions
get_dimensions() {
  local file="$1"
  if command -v identify &>/dev/null; then
    identify -format "%w %h" "$file" 2>/dev/null || echo "0 0"
  elif command -v file &>/dev/null; then
    file "$file" | grep -oP '\d+x\d+' | head -1 | tr 'x' ' ' || echo "0 0"
  else
    echo "0 0"
  fi
}

# Process a single image using Pillow
process_image() {
  local src="$1"
  local category="$2"
  local counter="$3"
  local basename=$(basename "$src")
  local name="${basename%.*}"
  local ext="${basename##*.}"

  # Force-lowercase extension
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

  # Sanitize name
  name=$(echo "$name" | sed 's/[^a-zA-Z0-9._-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')

  # Add category prefix and sequential number
  local new_name="${category}-${name}-$(printf '%02d' $counter).${ext}"
  local new_name_lower=$(echo "$new_name" | tr '[:upper:]' '[:lower:]')

  mkdir -p "${PROCESSED_DIR}/${category}"

  if python3 "${SCRIPT_DIR}/process_image.py" "$src" "${PROCESSED_DIR}/${category}" "${new_name_lower}" 2>/dev/null; then
    echo "${new_name_lower}"
  else
    cp "$src" "${PROCESSED_DIR}/${category}/${new_name_lower}"
    echo "${new_name_lower}"
  fi
}

# Escape single quotes for SQL
sql_escape() {
  echo "$1" | sed "s/'/''/g"
}

# Upload to R2
upload_to_r2() {
  local category="$1"
  log "Uploading ${category} to R2..."

  if ! command -v rclone &>/dev/null; then
    warn "rclone not installed. Skipping R2 upload."
    return 1
  fi

  rclone copy "${PROCESSED_DIR}/${category}" "${R2_REMOTE}/${category}" \
    --progress --transfers 4 --checkers 8

  log "Uploaded ${category} to R2"
}

# Seed D1 database
seed_database() {
  log "Seeding D1 database..."

  if ! command -v npx &>/dev/null; then
    warn "npx not installed. Skipping D1 seed."
    return 1
  fi

  if [ ! -f "$SQL_FILE" ]; then
    warn "No SQL file found at ${SQL_FILE}"
    return 1
  fi

  npx wrangler d1 execute "$D1_DB" --remote --file="$SQL_FILE"
  log "Database seeded successfully"
}

# ─── Main ────────────────────────────────────────────────────────────────────

main() {
  local upload=false
  local db=false
  local manifest_only=false

  while [[ $# -gt 0 ]]; do
    case $1 in
      --upload) upload=true; shift ;;
      --db) db=true; shift ;;
      --manifest-only) manifest_only=true; shift ;;
      *) error "Unknown option: $1" ;;
    esac
  done

  log "AMY Electric Gallery Pipeline"
  log "============================="

  # Load the manifest
  load_manifest

  mkdir -p "$PROCESSED_DIR" "$SQL_DIR"

  # Start SQL file
  cat >"$SQL_FILE" <<'EOF'
-- AMY Electric Gallery — Batch Insert
-- Generated by build_gallery.sh from photo_manifest.csv
-- Run: npx wrangler d1 execute amyelectric_db --remote --file=batch_insert.sql

BEGIN TRANSACTION;

EOF

  local total=0
  local processed=0
  declare -A by_category

  if [ "$manifest_only" = false ]; then
    log "Processing images from source..."
  fi

  # Process each manifest entry
  for i in "${!MANIFEST_FILENAME[@]}"; do
    local fname="${MANIFEST_FILENAME[$i]}"
    local folder="${MANIFEST_FOLDER[$i]}"
    local category="${MANIFEST_CATEGORY[$i]}"
    local description="${MANIFEST_DESCRIPTION[$i]}"
    local location="${MANIFEST_LOCATION[$i]}"
    local date="${MANIFEST_DATE[$i]}"

    total=$((total + 1))

    # Find source file
    local src="${SOURCE_DIR}/${folder}/${fname}"
    if [ ! -f "$src" ]; then
      warn "Source not found: ${src} — skipping"
      continue
    fi

    by_category[$category]=$(( ${by_category[$category]:-0} + 1 ))

    if [ "$manifest_only" = false ]; then
      local new_name
      new_name=$(process_image "$src" "$category" "${by_category[$category]}")

      # Get dimensions
      local dims
      dims=$(get_dimensions "${PROCESSED_DIR}/${category}/${new_name}")
      local width=$(echo "$dims" | awk '{print $1}')
      local height=$(echo "$dims" | awk '{print $2}')

      # Write SQL with description and location
      local safe_desc
      safe_desc=$(sql_escape "$description")
      local safe_loc
      safe_loc=$(sql_escape "$location")
      local safe_name
      safe_name=$(sql_escape "$new_name")

      cat >>"$SQL_FILE" <<SQLEOF
INSERT INTO gallery_images (filename, category, title, description, location, width, height, shoot_date, created_at)
VALUES ('${safe_name}', '${category}', '${safe_desc}', '${safe_desc}', '${safe_loc}', ${width:-0}, ${height:-0}, '${date}', datetime('now'));
SQLEOF

      processed=$((processed + 1))

      if [ $((processed % 100)) -eq 0 ]; then
        log "  Processed ${processed}/${total}..."
      fi
    else
      # Manifest-only: use processed files that already exist
      local existing="${PROCESSED_DIR}/${category}/"
      local existing_count
      existing_count=$(ls "${existing}" 2>/dev/null | grep -c "${fname%.*}" || true)

      if [ "$existing_count" -gt 0 ]; then
        local dims
        dims=$(get_dimensions "$(ls ${existing}*${fname%.*}* 2>/dev/null | head -1)")
        local width=$(echo "$dims" | awk '{print $1}')
        local height=$(echo "$dims" | awk '{print $2}')

        local safe_desc
        safe_desc=$(sql_escape "$description")
        local safe_loc
        safe_loc=$(sql_escape "$location")

        # Find the actual processed filename
        local proc_file
        proc_file=$(ls "${existing}"*"${fname%.*}"* 2>/dev/null | head -1 | xargs basename)

        cat >>"$SQL_FILE" <<SQLEOF
INSERT INTO gallery_images (filename, category, title, description, location, width, height, shoot_date, created_at)
VALUES ('${proc_file}', '${category}', '${safe_desc}', '${safe_desc}', '${safe_loc}', ${width:-0}, ${height:-0}, '${date}', datetime('now'));
SQLEOF

        processed=$((processed + 1))
      else
        warn "No processed file for ${fname} — processing now"
        local new_name
        new_name=$(process_image "$src" "$category" "${by_category[$category]}")

        local dims
        dims=$(get_dimensions "${PROCESSED_DIR}/${category}/${new_name}")
        local width=$(echo "$dims" | awk '{print $1}')
        local height=$(echo "$dims" | awk '{print $2}')

        local safe_desc
        safe_desc=$(sql_escape "$description")
        local safe_loc
        safe_loc=$(sql_escape "$location")
        local safe_name
        safe_name=$(sql_escape "$new_name")

        cat >>"$SQL_FILE" <<SQLEOF
INSERT INTO gallery_images (filename, category, title, description, location, width, height, shoot_date, created_at)
VALUES ('${safe_name}', '${category}', '${safe_desc}', '${safe_desc}', '${safe_loc}', ${width:-0}, ${height:-0}, '${date}', datetime('now'));
SQLEOF

        processed=$((processed + 1))
      fi
    fi
  done

  echo "" >>"$SQL_FILE"
  echo "COMMIT;" >>"$SQL_FILE"

  log "============================="
  log "Manifest entries: ${total}"
  log "SQL rows generated: ${processed}"
  log ""
  log "By category:"
  for cat in $(echo "${!by_category[@]}" | tr ' ' '\n' | sort); do
    log "  ${cat}: ${by_category[$cat]}"
  done
  log ""
  log "Output: ${PROCESSED_DIR}"
  log "SQL: ${SQL_FILE}"

  if [ "$manifest_only" = true ]; then
    log ""
    log "(manifest-only mode — no images were processed)"
  fi

  if $upload; then
    log ""
    log "Uploading to R2..."
    for cat in "${!by_category[@]}"; do
      upload_to_r2 "$cat"
    done
  fi

  if $db; then
    log ""
    seed_database
  fi

  log ""
  log "Done!"
}

main "$@"
