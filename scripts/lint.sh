#!/usr/bin/env bash
# Static lint for the site's own code. Report-only, no formatting, no rewrites.
#
#   bash scripts/lint.sh          # lint everything
#   bash scripts/lint.sh --fix    # let ruff apply its safe autofixes
#
# Scope: scripts/*.py (75 files), worker.js, js/src/*.js + js/*.js, scripts/*.mjs.
# Requires ruff (pipx/pip install ruff) and node. Exits non-zero on findings.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

FIX=""
[ "${1:-}" = "--fix" ] && FIX="--fix"
status=0

echo "── python: ruff ────────────────────────────────────────────"
if command -v ruff >/dev/null 2>&1; then
  ruff check scripts/ $FIX || status=1
else
  echo "SKIP: ruff not installed (pip install ruff)"
fi

echo "── python: syntax (SyntaxWarning promoted to error) ────────"
while IFS= read -r f; do
  python3 -W error::SyntaxWarning -c "import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)" "$f" \
    || { echo "FAIL: $f"; status=1; }
done < <(find scripts -name '*.py' -print)
echo "checked $(find scripts -name '*.py' | wc -l) python files"

echo "── javascript: node --check ────────────────────────────────"
js_count=0
for f in worker.js js/*.js js/src/*.js scripts/*.mjs; do
  [ -f "$f" ] || continue
  node --check "$f" || { echo "FAIL: $f"; status=1; }
  js_count=$((js_count + 1))
done
echo "checked $js_count javascript files"

echo "────────────────────────────────────────────────────────────"
[ $status -eq 0 ] && echo "LINT OK" || echo "LINT FAILED"
exit $status
