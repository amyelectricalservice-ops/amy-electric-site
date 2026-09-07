#!/usr/bin/env bash
# scripts/run_audit.sh
# Run Lighthouse accessibility/SEO audit on all HTML pages of the AMY Electric site.
# Uses the Chrome DevTools MCP lighthouse_audit tool.

set -euo pipefail

# Directory of the site
SITE_DIR="/home/amram/WEBSITE"

# Output directory for reports
REPORT_DIR="${SITE_DIR}/audit-reports"
mkdir -p "$REPORT_DIR"

# Find all .html files (excluding the audit report itself)
mapfile -t pages < <(find "$SITE_DIR" -type f -name "*.html" ! -path "*audit-reports*" )

# Function to run lighthouse audit via MCP
run_audit() {
  local page_path="$1"
  local page_url="file://$page_path"
  local page_name=$(basename "$page_path" .html)
  echo "Auditing $page_name..."
  # Call the MCP tool
  agy_mcp_chrome-devtools-mcp_lighthouse_audit {
    "pageId": $(basename "$page_path"),
    "outputDirPath": "$REPORT_DIR/$page_name"
  }
}

for page in "${pages[@]}"; do
  run_audit "$page"
 done

echo "All audits completed. Reports are in $REPORT_DIR"
