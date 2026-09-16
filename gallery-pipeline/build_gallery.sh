#!/bin/bash
# build_gallery.sh — AMY Electric Gallery Pipeline
# Processes raw images, generates SQL, and uploads to Cloudflare R2
#
# Usage: ./build_gallery.sh [--upload] [--db]
#   --upload  Also upload to R2 after processing
#   --db      Also seed D1 database after processing

set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RAW_DIR="${SCRIPT_DIR}/raw"
PROCESSED_DIR="${SCRIPT_DIR}/processed"
SQL_DIR="${SCRIPT_DIR}/sql"
SQL_FILE="${SQL_DIR}/batch_insert.sql"

R2_BUCKET="amyelectric-gallery"
R2_REMOTE="r2:amyelectric-gallery"
D1_DB="amyelectric_db"

# Image settings
MAX_WIDTH=1200
QUALITY=85
WEBP_QUALITY=80

# Categories (auto-detected from folder names or file patterns)
declare -A CATEGORIES=(
  ["ev-charger"]="EV Charger Installation"
  ["panel-upgrade"]="Panel Upgrade"
  ["commercial"]="Commercial Electrical"
  ["lighting"]="Lighting Installation"
  ["rewiring"]="Whole-Home Rewiring"
  ["repair"]="Electrical Repair"
  ["residential"]="Residential"
  ["emergency"]="Emergency Service"
)

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

# Detect category from filename
detect_category() {
  local filename="$1"
  local lower=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
  
  case "$lower" in
    *ev*|*charger*|*tesla*|*wall*connector*) echo "ev-charger" ;;
    *panel*|*breaker*|*subpanel*|*200a*) echo "panel-upgrade" ;;
    *commercial*|*bus*duct*|*switchgear*|*meter*) echo "commercial" ;;
    *light*|*recessed*|*ceiling*fan*) echo "lighting" ;;
    *rewir*|*knob*tube*|*aluminum*) echo "rewiring" ;;
    *repair*|*fix*|*outlet*|*switch*) echo "repair" ;;
    *emergency*|*urgent*) echo "emergency" ;;
    *) echo "residential" ;;
  esac
}

# Generate display title from filename
generate_title() {
  local filename="$1"
  # Remove extension, numbers, common prefixes
  local title=$(echo "$filename" | sed 's/\.[^.]*$//' | sed 's/^gallery-//' | sed 's/^[0-9]*-//' | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
  echo "$title"
}

# Process a single image
process_image() {
  local src="$1"
  local category="$2"
  local counter="$3"
  local basename=$(basename "$src")
  local name="${basename%.*}"
  local ext="${basename##*.}"
  
  # Force-lowercase extension
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  
  # Replace spaces and punctuation with hyphens
  name=$(echo "$name" | sed 's/[^a-zA-Z0-9._-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
  
  # Add category prefix and sequential number
  local new_name="${category}-${name}-$(printf '%02d' $counter).${ext}"
  local new_name_lower=$(echo "$new_name" | tr '[:upper:]' '[:lower:]')
  
  # Create output directory
  mkdir -p "${PROCESSED_DIR}/${category}"
  
  # Process with ImageMagick (if available) or just copy
  if command -v convert &> /dev/null; then
    # Resize to max width, maintain aspect ratio
    convert "$src" -resize "${MAX_WIDTH}>" -quality "$QUALITY" "${PROCESSED_DIR}/${category}/${new_name_lower}"
    
    # Also create WebP version
    convert "$src" -resize "${MAX_WIDTH}>" -quality "$WEBP_QUALITY" "${PROCESSED_DIR}/${category}/${new_name_lower%.*}.webp"
  else
    # No ImageMagick — just copy with renamed file
    cp "$src" "${PROCESSED_DIR}/${category}/${new_name_lower}"
  fi
  
  echo "${new_name_lower}"
}

# Generate SQL insert statement
generate_sql() {
  local filename="$1"
  local category="$2"
  local title="$3"
  local width="$4"
  local height="$5"
  
  # Escape single quotes for SQL
  local safe_title=$(echo "$title" | sed "s/'/''/g")
  local safe_filename=$(echo "$filename" | sed "s/'/''/g")
  
  cat <<EOF
INSERT INTO gallery_images (filename, category, title, width, height, created_at)
VALUES ('${safe_filename}', '${category}', '${safe_title}', ${width:-0}, ${height:-0}, datetime('now'));
EOF
}

# Get image dimensions (requires ImageMagick or file command)
get_dimensions() {
  local file="$1"
  if command -v identify &> /dev/null; then
    identify -format "%w %h" "$file" 2>/dev/null || echo "0 0"
  elif command -v file &> /dev/null; then
    file "$file" | grep -oP '\d+x\d+' | head -1 | tr 'x' ' ' || echo "0 0"
  else
    echo "0 0"
  fi
}

# Upload to R2
upload_to_r2() {
  local category="$1"
  log "Uploading ${category} to R2..."
  
  if ! command -v rclone &> /dev/null; then
    warn "rclone not installed. Skipping R2 upload."
    return 1
  fi
  
  rclone copy "${PROCESSED_DIR}/${category}" "${R2_REMOTE}/${category}" \
    --progress \
    --transfers 4 \
    --checkers 8
  
  log "Uploaded ${category} to R2"
}

# Seed D1 database
seed_database() {
  log "Seeding D1 database..."
  
  if ! command -v npx &> /dev/null; then
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
  
  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      --upload) upload=true; shift ;;
      --db) db=true; shift ;;
      *) error "Unknown option: $1" ;;
    esac
  done
  
  log "AMY Electric Gallery Pipeline"
  log "============================="
  
  # Check for raw images
  if [ ! -d "$RAW_DIR" ] || [ -z "$(ls -A "$RAW_DIR" 2>/dev/null)" ]; then
    warn "No raw images found in ${RAW_DIR}"
    log "Place your images in ${RAW_DIR} and run again."
    exit 0
  fi
  
  # Create output directories
  mkdir -p "$PROCESSED_DIR" "$SQL_DIR"
  
  # Initialize SQL file
  cat > "$SQL_FILE" <<'EOF'
-- AMY Electric Gallery — Batch Insert
-- Generated by build_gallery.sh
-- Run: npx wrangler d1 execute amyelectric_db --remote --file=batch_insert.sql

BEGIN TRANSACTION;

EOF
  
  # Counters
  local total=0
  local by_category=()
  
  # Process each raw image
  log "Processing images from ${RAW_DIR}..."
  
  for src in "$RAW_DIR"/*.{jpg,jpeg,png,gif,webp,JPG,JPEG,PNG,GIF,WEBP} 2>/dev/null; do
    [ -f "$src" ] || continue
    
    total=$((total + 1))
    local basename=$(basename "$src")
    local category=$(detect_category "$basename")
    local title=$(generate_title "$basename")
    local dims=$(get_dimensions "$src")
    local width=$(echo "$dims" | awk '{print $1}')
    local height=$(echo "$dims" | awk '{print $2}')
    
    # Count per category
    by_category[$category]=$(( ${by_category[$category]:-0} + 1 ))
    
    # Process image
    local new_name=$(process_image "$src" "$category" "${by_category[$category]}")
    
    # Generate SQL
    generate_sql "$new_name" "$category" "$title" "$width" "$height" >> "$SQL_FILE"
    
    log "  [${category}] ${basename} → ${new_name}"
  done
  
  # Finalize SQL
  echo "" >> "$SQL_FILE"
  echo "COMMIT;" >> "$SQL_FILE"
  
  log "============================="
  log "Processed ${total} images"
  log ""
  log "By category:"
  for cat in "${!by_category[@]}"; do
    log "  ${cat}: ${by_category[$cat]}"
  done
  log ""
  log "Output: ${PROCESSED_DIR}"
  log "SQL: ${SQL_FILE}"
  
  # Upload to R2 if requested
  if $upload; then
    log ""
    log "Uploading to R2..."
    for cat in "${!by_category[@]}"; do
      upload_to_r2 "$cat"
    done
  fi
  
  # Seed database if requested
  if $db; then
    log ""
    seed_database
  fi
  
  log ""
  log "Done! 🎉"
}

main "$@"
