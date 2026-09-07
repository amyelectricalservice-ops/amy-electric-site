#!/usr/bin/env bash
set -euo pipefail

# Ensure Lighthouse is installed
if ! command -v lighthouse >/dev/null 2>&1; then
  echo "Installing Lighthouse..."
  npm install -g lighthouse > /dev/null 2>&1
fi

# Start local server (if not already running)
./scripts/serve.sh &
SERVER_PID=$!
# Give the server a moment to start
sleep 2

OUT_DIR="accessibility-audit"
mkdir -p "$OUT_DIR"

# Find all HTML files tracked by git (or fallback to find)
if command -v git >/dev/null 2>&1; then
  pages=$(git ls-files "*.html")
else
  pages=$(find . -type f -name "*.html")
fi

# Run Lighthouse audit for each page
for page in $pages; do
  # Strip leading ./ if present
  clean_page=${page#./}
  url="http://localhost:8000/${clean_page}"
  echo "Auditing $url ..."
  # Use page basename for output files
  base=$(basename "$clean_page" .html)
  npx lighthouse "$url" \
    --output=json --output=html \
    --quiet \
    --chrome-flags="--headless" \
    --output-path="${OUT_DIR}/${base}"
  # Lighthouse appends .report.json and .report.html automatically
done

# Stop the server
kill $SERVER_PID || true
rm -f .server_pid

echo "All audits completed. Results are in $OUT_DIR/"
