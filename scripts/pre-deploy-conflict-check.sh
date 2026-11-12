#!/usr/bin/env bash
# pre-deploy-conflict-check.sh — exit non-zero if merge markers found
if git grep -lE '^(<{7}|>{7}|={7}$)' -- . ':!*.lock'; then
  echo "❌ Merge conflict markers found in tracked files. Resolve before deploying."
  exit 1
fi
echo "✅ No conflict markers. Safe to deploy."
