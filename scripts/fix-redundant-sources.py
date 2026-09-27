#!/usr/bin/env python3
"""Remove <source> elements the browser can never reach.

35 pages carry copy-pasted duplicate <source> children inside <picture>. The
browser selects the first <source> whose media query matches, so any <source>
that repeats an earlier one's srcset with no media attribute of its own can never
be used.

The rule is deliberately narrow: only a source whose srcset exactly matches an
earlier, media-less source is dropped. Sources that differ only by media are
complementary and are kept. Idempotent.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
PICTURE = re.compile(r"(?is)(<picture[^>]*>)(.*?)(</picture>)")
SOURCE = re.compile(r"(?is)<source\b[^>]*>")
SRCSET = re.compile(r'(?is)\bsrcset\s*=\s*"([^"]*)"')
MEDIA = re.compile(r'(?is)\bmedia\s*=')


def clean(inner):
    out = []
    pos = 0
    removed = 0
    always = set()      # srcsets already seen with no media (match everything)
    for m in SOURCE.finditer(inner):
        srcset = SRCSET.search(m.group(0))
        key = srcset.group(1).strip() if srcset else None
        if key is not None and key in always:
            out.append(inner[pos:m.start()])
            pos = m.end()
            removed += 1
            continue
        if key is not None and not MEDIA.search(m.group(0)):
            always.add(key)
        out.append(inner[pos:m.end()])
        pos = m.end()
    out.append(inner[pos:])
    return "".join(out), removed


total = 0
pages = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames
                   if d not in (".git", "node_modules", ".wrangler", "img", "css", "js",
                                "fonts", "extensions", "open-seo", "gallery-pipeline",
                                "accessibility-audit", "audit", "seo-workspace", "reports")]
    for f in sorted(filenames):
        if not f.endswith(".html"):
            continue
        path = os.path.join(dirpath, f)
        doc = open(path, encoding="utf-8", errors="replace").read()
        if "<picture" not in doc:
            continue
        n = 0

        def repl(m):
            global n
            new_inner, removed = clean(m.group(2))
            n += removed
            return m.group(1) + new_inner + m.group(3)

        new_doc = PICTURE.sub(repl, doc)
        if n:
            total += n
            pages += 1
            if APPLY:
                new_doc = re.sub(r"[ \t]+\n", "\n", new_doc)
                open(path, "w", encoding="utf-8").write(new_doc)

print("mode:                    %s" % ("APPLY" if APPLY else "DRY RUN"))
print("pages changed:           %d" % pages)
print("unreachable <source> removed: %d" % total)
