#!/usr/bin/env python3
"""Audit the committed Worker routing against the live Cloudflare zone.

`amy-electric-site` is the only Worker that serves amyelectric.com, and it is
reached through the single `amyelectric.com/*` zone route declared in
`wrangler.jsonc`. An `amy-electric-seo` edge wrapper used to own that route
table, and because it had been deployed out-of-band nothing in git said it
existed — which is exactly how git and Cloudflare drifted apart before. This
script asserts they agree:

    wrangler.jsonc   the site Worker -- must own exactly its declared routes

and that no other Worker owns a route on the zone beyond the intentional
second-worker routes in `EXPECTED_OTHER_WORKERS` (lead-automation, declared in
its own repo). It exits non-zero on a real
mismatch so CI fails when git and Cloudflare disagree. Pass --warn-only to
report a mismatch without failing: the workflow uses that on pushes and pull
requests, where the deploy that follows reconciles the zone from git anyway, and
reserves the hard failure for the weekly scheduled run, which is the one that
catches drift nobody meant to introduce.

A missing API permission is reported as a warning instead of a failure, matching
the deploy pipeline's stance that a run red for reasons the repo cannot fix
trains people to ignore red.

Usage:
    CLOUDFLARE_API_TOKEN=... python3 scripts/audit-cloudflare-routes.py [--warn-only]
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

ZONE = "amyelectric.com"
API = "https://api.cloudflare.com/client/v4"
CONFIG = "wrangler.jsonc"

# Other Workers with intentional routes on this zone, declared in their own
# repos. Route ownership was a single-Worker invariant for years; it is now a
# two-Worker table, and drift in EITHER direction should fail the audit:
#   - an unexpected extra route on one of these Workers, or
#   - one of these Workers disappearing / losing its routes.
# Update this table in the same commit that changes the other repo's routes.
EXPECTED_OTHER_WORKERS = {
    # lead capture worker (repo: amyelectricalservice-ops/amyelectric-marketing-agent)
    "amyelectric-lead-automation": {"amyelectric.com/api/leads"},
}


class PermissionGap(Exception):
    """The token cannot read zone Worker routes; not the repo's fault."""


def api_get(path):
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    if not token:
        raise PermissionGap("CLOUDFLARE_API_TOKEN is not set")
    req = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + token})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:300]
        if exc.code in (401, 403):
            raise PermissionGap("HTTP %s from %s: %s" % (exc.code, path, body))
        sys.exit("Cloudflare API %s failed: HTTP %s %s" % (path, exc.code, body))
    if not data.get("success"):
        sys.exit("Cloudflare API %s failed: %s" % (path, data.get("errors")))
    return data["result"]


def declared(config_path):
    """Return (worker name, declared route patterns) from a wrangler jsonc file.

    Regex rather than a real jsonc parse: we only need the top-level `name` and
    the objects carrying a `pattern`, and a comment in these files never looks
    like either.
    """
    try:
        src = open(config_path, encoding="utf-8").read()
    except OSError as exc:
        sys.exit("cannot read %s: %s" % (config_path, exc))
    name = re.search(r'"name"\s*:\s*"([^"]+)"', src)
    return (name.group(1) if name else None,
            set(re.findall(r'"pattern"\s*:\s*"([^"]+)"', src)))


def main(argv):
    warn_only = "--warn-only" in argv
    name, declared_routes = declared(CONFIG)

    try:
        zone_id = api_get("/zones?name=" + ZONE)[0]["id"]
        routes = api_get("/zones/%s/workers/routes" % zone_id)
    except PermissionGap as gap:
        print("::warning title=Cloudflare route audit skipped::%s" % gap)
        print("Audit skipped: the token cannot read zone Worker routes.")
        print("Grant Zone > Workers Routes > Read to audit drift.")
        return 0

    live = {}
    for route in routes:
        live.setdefault(route.get("script") or "(unattached)", set()).add(route["pattern"])

    problems = []
    actual = live.get(name, set())
    if actual != declared_routes:
        problems.append(
            "%s: %d declared, %d live -- only in git: %s; only in Cloudflare: %s"
            % (name, len(declared_routes), len(actual),
               sorted(declared_routes - actual), sorted(actual - declared_routes)))
    for script, patterns in sorted(live.items()):
        if script == name:
            continue
        expected = EXPECTED_OTHER_WORKERS.get(script)
        if expected is None:
            problems.append("unexpected Worker %s owns %s" % (script, sorted(patterns)))
        elif patterns != expected:
            problems.append(
                "Worker %s owns %s, expected exactly %s (see EXPECTED_OTHER_WORKERS)"
                % (script, sorted(patterns), sorted(expected)))
    for script, expected in sorted(EXPECTED_OTHER_WORKERS.items()):
        if script not in live:
            problems.append(
                "expected Worker %s (see EXPECTED_OTHER_WORKERS) owns no route on the zone"
                % script)

    print("Declared in git:")
    print("  %s (%d):" % (name, len(declared_routes)))
    for pattern in sorted(declared_routes):
        print("    %s" % pattern)
    print("Live on %s:" % ZONE)
    for script, patterns in sorted(live.items()):
        print("  %s (%d):" % (script, len(patterns)))
        for pattern in sorted(patterns):
            print("    %s" % pattern)

    if problems:
        for problem in problems:
            print(("::warning::" if warn_only else "::error::") + problem)
        if warn_only:
            print("drift (warn-only): git and Cloudflare disagree; the deploy that "
                  "follows reconciles this on a push to main.")
            return 0
        print("DRIFT: git and Cloudflare disagree (see above).")
        return 1

    print("OK: git and Cloudflare agree on %d route(s)." % len(declared_routes))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
