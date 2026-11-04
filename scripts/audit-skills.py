#!/usr/bin/env python3
"""Audit skill wiring for the AMY Electric site.

Checks:
1. Every skill id referenced in AGENTS.md and .opencode/agents/*.md resolves
   to .agents/skills/<id>/SKILL.md.
2. .claude/skills/<id> entries are symlinks into .agents/skills/.
3. skills-lock.json keys match .agents/skills/ directories.
4. No vendored skill content drift (hash in lock matches SKILL.md).

Exit 0 on pass, 1 on failure. Run: python3 scripts/audit-skills.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".agents/skills"
CLAUDE = ROOT / ".claude/skills"
LOCK = ROOT / "skills-lock.json"

# Backtick-quoted lowercase kebab ids that look like skill ids.
SKILL_ID_RE = re.compile(r"`([a-z][a-z0-9-]{2,40})`")
# Words that are not skills even when backticked in AGENTS.md/agents.
ALLOWLIST = {
    # files / code identifiers
    "wrangler.jsonc", "cloudflare.config.ts", "worker.js", "run_worker_first",
    "schema-tool.py", "audit-site.py", "audit-price-drift.py", "audit-skills.py",
    "audit-cloudflare-routes.py", "sync-faq-schema.py", "notify-indexnow.sh",
    "test-estimator.mjs", "test-book.mjs", "test-worker-geo.mjs",
    "test-geo-personalize.mjs", "test-worker-images.mjs",
    "generate-city-pages.py", "build-css.py", "build-js.py",
    "refresh-sitemap-lastmod.py", "fix-radiogroup-labels.py",
    "sync-mobile-touch-css.py", "expand-city-pages.py",
    "site_data.py", "estimate-schema.sql", "package.json", "wrangler",
    "cf", "npx", "node", "bash", "python3", "git", "curl", "grep",
    # HTML/CSS/JS selectors and ids
    "topbar", "nav-book", "request-type-label", "request_type", "request-type",
    "radio-group", "radiogroup", "nav-cta", "webmcp", "book-widget",
    "touch-targets", "nav", "topbar-responsive-fix", "route-config", "plugins",
    "hand-edited", "selector", "field", "concepts", "hooks",
    # site / business facts
    "amy-electric-site", "amy-electric-seo", "amy-electric-estimator",
    "amyelectric.com", "amy-electric", "c-10", "evitp",
    "seo", "gbp", "geo-linking", "web-perf", "permission", "permissions",
    "run_worker_first", "run-worker-first", "max-age", "must-revalidate",
    "stay-while-revalidate", "public", "private", "no-store", "immutable",
    "injected", "default", "r2", "d1", "kv", "actions", "hooks",
    "dependencies", "scripts", "format", "lint", "test", "build", "deploy",
    "updates", "schedules", "validation", "endpoints", "bindings", "perms",
    "examples", "tests", "com", "menu", "fig", "folder", "events",
    "functions", "function", "skill", "skills", "global", "repo", "vendored",
    "directory", "entry", "upstream", "public", "local", "unknown", "applied",
    "unapplied", "inputs", "outputs", "header", "request", "response",
    "success", "warning", "error", "info", "contrast", "accessibility",
    "debounce", "timing", "rendering", "performance", "example",
    "index", "blog", "case-studies", "city", "gallery", "reviews",
    "testimonials", "service-areas", "privacy-policy", "sitemap", "robots",
    "llms", "llms-full", "api-catalog", "well-known", "main", "skip", "ci",
    "dry-run", "diagnose", "deleted", "deprecated", "authoritative",
    "structured", "executing", "monitoring", "paid", "learnings",
    "explicitly", "signaling", "multiple", "argument", "anotifierglow",
    "controller-managed", "contextual", "observability", "annotations",
    "participants", "replacement", "timezone", "structural",
    "google", "bing", "driver", "plugins", "roles", "upsell", "fleet",
    "sam", "internal", "product", "toolResult", "cluster-by",
    "deferred", "rsvp", "stalled", "sudo-then-exec", "functions",
    "querystring", "instantiation", "verifier", "reviews", "connector",
    "evaluator", "workspace", "workflow", "pipeline", "schedule",
    "storage", "frames", "parameters", "bypass", "system",
    "namespace", "orchestration", "sanitize", "exponential", "jetstream",
    "workers", "agents", "harnesses", "containers", "streams", "offerings",
    "windows", "queued", "parked", "merged", "summaries", "grounding",
    "splicing", "reachability", "readiness", "upscale", "spoofing",
    "debugging", "solid", "assistants", "dependently", "sanitization",
    "cheekily", "persistent", "pre-approval", "upscale",
    "projections", "fissile", "doubt", "inspired", "provenance",
    "summaries", "mistral", "matchmaking", "sleek", "author-side",
    "front-matter", "multi-target", "via", "trusted", "plans", "steps",
    "produces", "adapts", "command", "scorecard", "dataclass",
    "matchmaking", "munching", "metadata", "step",
    "no-store", "ui", "shoulders", "harnessed",
    "bucket-id", "test-cluster", "observability-triage",
    "custom-tool", "daily", "browser-snapshot", "providers",
    # city / page slugs and Worker names backticked in AGENTS.md
    "amy-electric-consolidate", "cdn-cgi", "city-edith-norman",
    "city-el-sobrante", "city-health-campadre", "dataforseo-mcp-server",
    "emergency-electrical", "emergency-electrician", "workflows-starter-template",
    "open-seo", "every-app", "every-app/open-seo", "seo",
}


def load_skill_dirs():
    return {p.name for p in AGENTS.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}


def referenced_skill_ids():
    texts = []
    agents_md = ROOT / "AGENTS.md"
    if agents_md.exists():
        texts.append(agents_md.read_text())
    for md in (ROOT / ".opencode/agents").glob("*.md"):
        texts.append(md.read_text())
    ids = set()
    for t in texts:
        for m in SKILL_ID_RE.findall(t):
            if m not in ALLOWLIST and "-" in m:
                ids.add(m)
    return ids


def main():
    errors, warnings = [], []
    skill_dirs = load_skill_dirs()

    # 1. referenced ids resolve
    refs = referenced_skill_ids()
    known_nonskills = {"find-skills", "create-repo-skill", "merge-ready",
                        "papercuts", "security-ownership-map", "security-threat-model",
                        "gmail", "google-drive"}
    for rid in sorted(refs):
        if rid not in skill_dirs and rid not in known_nonskills:
            errors.append(f"UNRESOLVED skill reference: {rid!r} in AGENTS.md/.opencode/agents "
                          f"has no .agents/skills/{rid}/SKILL.md")

    # 2. .claude/skills mirror is symlinks resolving to canonical dirs
    if CLAUDE.exists():
        for link in CLAUDE.iterdir():
            name = link.name
            if name not in skill_dirs:
                warnings.append(f"MIRROR EXTRA: .claude/skills/{name} has no canonical .agents/skills/{name}")
            if not link.is_symlink():
                errors.append(f"MIRROR NOT SYMLINK: .claude/skills/{name} is a copy, must be a symlink")
            else:
                target = (link.resolve())
                if not (target / "SKILL.md").exists():
                    errors.append(f"MIRROR BROKEN: .claude/skills/{name} -> {target} has no SKILL.md")
        for name in sorted(skill_dirs):
            if not (CLAUDE / name).exists():
                warnings.append(f"MIRROR MISSING: .claude/skills/{name} not linked")
    else:
        warnings.append("MIRROR ABSENT: .claude/skills/ does not exist")

    # 3. lock matches directories
    lock = json.load(open(LOCK))
    locked = set(lock.get("skills", {}))
    for name in sorted(skill_dirs - locked):
        errors.append(f"LOCK MISSING: .agents/skills/{name} not in skills-lock.json")
    for name in sorted(locked - skill_dirs):
        errors.append(f"LOCK ORPHAN: skills-lock.json has {name!r} but no .agents/skills/{name}/")

    # 4. hashes match
    for name, meta in lock.get("skills", {}).items():
        p = AGENTS / name / "SKILL.md"
        if not p.exists():
            continue
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        expected = meta.get("computedHash")
        if expected and expected != actual and meta.get("sourceType") != "local":
            errors.append(f"HASH DRIFT: .agents/skills/{name}/SKILL.md changed (lock {expected[:12]}…, actual {actual[:12]}…)")

    for w in warnings:
        print(f"WARNING {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\nFAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nPASS: {len(skill_dirs)} skills, {len(locked)} locked, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
