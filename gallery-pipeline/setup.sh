#!/bin/bash
# setup.sh — AMY Electric Gallery Pipeline Setup
# Installs dependencies and configures the pipeline

set -euo pipefail

echo "AMY Electric Gallery Pipeline Setup"
echo "==================================="
echo ""

# Check for required tools
echo "Checking dependencies..."

check_tool() {
  local tool="$1"
  local install_cmd="$2"
  
  if command -v "$tool" &> /dev/null; then
    echo "  ✓ $tool installed"
    return 0
  else
    echo "  ✗ $tool not found"
    echo "    Install: $install_cmd"
    return 1
  fi
}

missing=0

check_tool "rclone" "curl https://rclone.org/install.sh | sudo bash" || missing=$((missing + 1))
check_tool "npx" "npm install -g npx" || missing=$((missing + 1))
check_tool "convert" "sudo apt install imagemagick" || missing=$((missing + 1))
check_tool "jq" "sudo apt install jq" || missing=$((missing + 1))

echo ""

if [ $missing -gt 0 ]; then
  echo "⚠  $missing tools missing. Install them before proceeding."
  echo ""
fi

# Create directories
echo "Creating directories..."
mkdir -p raw processed sql
echo "  ✓ raw/ — Place your unprocessed images here"
echo "  ✓ processed/ — Output directory"
echo "  ✓ sql/ — Generated SQL files"
echo ""

# Create rclone config if it doesn't exist
RCLONE_CONF="$HOME/.config/rclone/rclone.conf"
if [ ! -f "$RCLONE_CONF" ]; then
  echo "Creating rclone config..."
  mkdir -p "$(dirname "$RCLONE_CONF")"
  cat > "$RCLONE_CONF" <<'EOF'
[amyelectric]
type = s3
provider = Cloudflare
access_key_id = YOUR_R2_ACCESS_KEY_ID
secret_access_key = YOUR_R2_SECRET_ACCESS_KEY
endpoint = https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
acl = public-read
bucket_policy = true
EOF
  echo "  ✓ Created ${RCLONE_CONF}"
  echo "  ⚠  Edit with your R2 credentials!"
else
  echo "  ✓ rclone config exists"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Place raw images in: $(pwd)/raw/"
echo "  2. Edit rclone config: ${RCLONE_CONF}"
echo "  3. Create D1 database: npx wrangler d1 create amyelectric_db"
echo "  4. Run schema: npx wrangler d1 execute amyelectric_db --remote --file=schema.sql"
echo "  5. Run pipeline: ./build_gallery.sh --upload --db"
