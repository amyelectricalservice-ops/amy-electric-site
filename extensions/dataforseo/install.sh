#!/bin/bash
set -e

# DataForSEO MCP Server Install Script
# Requires: Node.js/npm and DataForSEO API credentials

echo "Installing DataForSEO MCP server..."

# Check for Node.js
if ! command -v npx &> /dev/null; then
    echo "ERROR: Node.js/npx is required"
    exit 1
fi

# Install the MCP server package
npm install -g dataforseo-mcp-server 2>&1 || {
    echo "Global install failed, trying local..."
    cd "$(dirname "$0")/../../"
    npm init -y 2>/dev/null
    npm install dataforseo-mcp-server 2>&1
}

# Check for credentials
if [ -z "$DATAFORSEO_LOGIN" ] || [ -z "$DATAFORSEO_PASSWORD" ]; then
    echo ""
    echo "To complete setup, add to your ~/.config/opencode/opencode.json:"
    echo '  "mcp": {'
    echo '    "dataforseo": {'
    echo '      "type": "local",'
    echo '      "command": "npx",'
    echo '      "args": ["dataforseo-mcp-server"],'
    echo '      "env": {'
    echo '        "DATAFORSEO_LOGIN": "your_api_login",'
    echo '        "DATAFORSEO_PASSWORD": "your_api_password"'
    echo '      },'
    echo '      "enabled": true'
    echo '    }'
    echo '  }'
    echo ""
    echo "Get API keys at: https://app.dataforseo.com/api-access"
fi

echo "DataForSEO MCP server installed successfully."
echo "Available tools: serp, keywords, volume, difficulty, intent, backlinks, competitors, onpage, ai-scrape, and 79+ more."
