#!/usr/bin/env python3
"""Audit the committed Worker routing against the live Cloudflare zone.

The site is served by two Workers, and which of them owns the `amyelectric.com`
zone routes is the thing that silently drifted before (the `amy-electric-seo`
edge wrapper was deployed out-of-band, so nothing in git said it existed). This
script asserts that the repo and the zone still agree:

    seo-worker/wrangler.jsonc   the wrapper   -- must own its declared routes
    wrangler.jsonc              the origin    -- must own no zone routes

Exits non-zero on a real mismatch so CI fails when git and Cloudflare disagree.
Pass --warn-only to report a mismatch without failing: the workflow uses that on
pushes and pull requests, where the sync job is about to reconcile the zone from
git anyway, and reserves the hard failure for the weekly scheduled run, which is
the one that catches drift nobody meant to introduce.

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
WRAPPER_CONFIG = "seo-worker/wrangler.jsonc"
ORIGIN_CONFIG = "wrangler.jsonc"


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
    wrapper_name, wrapper_routes = declared(WRAPPER_CONFIG)
    origin_name, origin_routes = declared(ORIGIN_CONFIG)

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
    for label, name, declared_routes in (
        ("wrapper", wrapper_name, wrapper_routes),
        ("origin", origin_name, origin_routes),
    ):
        expected = declared_routes if label == "wrapper" else set()
        actual = live.get(name, set())
        if actual != expected:
            problems.append(
                "%s %s: %d declared, %d live -- only in git: %s; only in Cloudflare: %s"
                % (label, name, len(expected), len(actual),
                   sorted(expected - actual), sorted(actual - expected)))
    for script, patterns in sorted(live.items()):
        if script not in (wrapper_name, origin_name):
            problems.append("unexpected Worker %s owns %s" % (script, sorted(patterns)))

    print("Declared in git:")
    print("  %s (%d):" % (wrapper_name, len(wrapper_routes)))
    for pattern in sorted(wrapper_routes):
        print("    %s" % pattern)
    print("  %s (origin, expected 0): %d" % (origin_name, len(origin_routes)))
    print("Live on %s:" % ZONE)
    for script, patterns in sorted(live.items()):
        print("  %s (%d):" % (script, len(patterns)))
        for pattern in sorted(patterns):
            print("    %s" % pattern)

    if problems:
        for problem in problems:
            print(("::warning::" if warn_only else "::error::") + problem)
        if warn_only:
            print("drift (warn-only): git and Cloudflare disagree; the sync job "
                  "reconciles this on a push to main.")
            return 0
        print("DRIFT: git and Cloudflare disagree (see above).")
        return 1

    print("OK: git and Cloudflare agree on %d route(s)." % len(wrapper_routes))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
