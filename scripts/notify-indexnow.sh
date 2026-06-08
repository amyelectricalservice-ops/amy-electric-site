#!/bin/bash
# Notify Bing/IndexNow after a deployment
# Run: bash scripts/notify-indexnow.sh

KEY="16076f14-4d06-4581-b281-38a7a89804ca"
SITE="https://amyelectric.com"

# Submit home page to IndexNow API
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "amyelectric.com",
    "key": "'"$KEY"'",
    "keyLocation": "'"$SITE/$KEY.txt"'",
    "urlList": [
      "'"$SITE"'",
      "'"$SITE/ev-charger-installation"'",
      "'"$SITE/panel-upgrade"'",
      "'"$SITE/electrical-repair"'",
      "'"$SITE/commercial-electrical"'",
      "'"$SITE/lighting-installation"'",
      "'"$SITE/tesla-charger-installation"'",
      "'"$SITE/whole-home-rewiring"'",
      "'"$SITE/surge-protection"'",
      "'"$SITE/outlet-switch-installation"'",
      "'"$SITE/ceiling-fan-installation"'",
      "'"$SITE/smoke-co-detector-installation"'",
      "'"$SITE/generator-transfer-switch"'",
      "'"$SITE/dedicated-circuits"'",
      "'"$SITE/smart-home-electrical"'",
      "'"$SITE/electrical-safety-inspections"'",
      "'"$SITE/blog"'"
    ]
  }'

echo "IndexNow notification sent. Check response above."