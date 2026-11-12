#!/usr/bin/env bash
# AMY Electric — production security smoke test (AE-048).
#
# Read-only checks against a deployed host. Verifies the headers and the
# guard rails around the lead endpoints. It does NOT submit a lead.
#
# Usage:
#   bash scripts/security-check.sh                       # workers.dev host
#   bash scripts/security-check.sh https://amyelectric.com
#
# Exit code is non-zero if any check fails, so it can gate a release.
set -uo pipefail

BASE="${1:-https://amy-electric-site.a-m-y-electricalservice.workers.dev}"
fail=0

note() { printf '  %-44s %s\n' "$1" "$2"; }
ok()   { note "$1" "PASS"; }
bad()  { note "$1" "FAIL"; fail=$((fail+1)); }

echo "Security smoke test: $BASE"
echo

headers="$(curl -sSI -m 20 "$BASE/" | tr -d '\r')"

check_header() {
  local name="$1" pattern="$2"
  if echo "$headers" | grep -qiE "^${name}: .*${pattern}"; then ok "$name"; else bad "$name (missing/incorrect)"; fi
}

check_header "strict-transport-security" "max-age=[0-9]+"
check_header "x-content-type-options" "nosniff"
check_header "x-frame-options" "(SAMEORIGIN|DENY)"
check_header "referrer-policy" "."
check_header "content-security-policy" "."

echo
# Admin API must reject anonymous requests.
code="$(curl -s -o /dev/null -w '%{http_code}' -m 15 "$BASE/api/admin/leads")"
[[ "$code" == "401" ]] && ok "admin API rejects anonymous (401)" || bad "admin API returned $code (expected 401)"

code="$(curl -s -o /dev/null -w '%{http_code}' -m 15 "$BASE/admin")"
[[ "$code" == "401" ]] && ok "admin page rejects anonymous (401)" || bad "admin page returned $code (expected 401)"

# Uploads must reject non-allowed types before storage.
tmp="$(mktemp)"
printf 'not a real file' > "$tmp"
resp="$(curl -s -m 20 -X POST "$BASE/api/lead-files" -F "upload_token=securitycheck1234567890" -F "file=@$tmp;filename=evil.jpg;type=image/jpeg")"
rm -f "$tmp"
if echo "$resp" | grep -q '"success":false'; then ok "upload rejects a disguised file"; else bad "upload accepted a disguised file"; fi

# Contact endpoint must reject a non-POST.
code="$(curl -s -o /dev/null -w '%{http_code}' -m 15 "$BASE/api/contact")"
[[ "$code" == "405" || "$code" == "400" ]] && ok "contact endpoint rejects GET ($code)" || bad "contact GET returned $code"

# robots/sitemap sanity.
code="$(curl -s -o /dev/null -w '%{http_code}' -m 15 "$BASE/sitemap.xml")"
[[ "$code" == "200" ]] && ok "sitemap.xml reachable" || bad "sitemap.xml returned $code"

echo
if [[ "$fail" -gt 0 ]]; then
  echo "FAILED: $fail check(s)"
  exit 1
fi
echo "All security checks passed."
