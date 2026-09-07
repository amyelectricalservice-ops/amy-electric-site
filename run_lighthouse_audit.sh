#!/usr/bin/env bash
# run_lighthouse_audit.sh – audit all HTML pages with the globally installed lighthouse binary
# Requires a local HTTP server serving the site on http://localhost:8000
# The script will:
#   1. Ensure the audit/lighthouse output directory exists
#   2. Find all .html files under the project root
#   3. For each file, build the URL and run lighthouse, saving JSON output
#   4. Continue on errors

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/audit/lighthouse"
mkdir -p "$OUTPUT_DIR"

BASE_URL="http://localhost:8000"

# Find all HTML files relative to the project root
find "$PROJECT_ROOT" -type f -name "*.html" -printf "%P\n" | while read -r relPath; do
  url="$BASE_URL/$relPath"
  name=$(basename "$relPath" .html)
  outFile="$OUTPUT_DIR/${name}.json"
  echo "🔎 Auditing $url → $outFile"
  LIGHTHOUSE_BIN="$HOME/.npm-global/bin/lighthouse"
"$LIGHTHOUSE_BIN" "$url" --output=json --output-path="$outFile" --quiet --chrome-flags="--headless" || echo "⚠️ Lighthouse failed for $url; skipping"
done

echo "✅ All Lighthouse reports saved in $OUTPUT_DIR"
