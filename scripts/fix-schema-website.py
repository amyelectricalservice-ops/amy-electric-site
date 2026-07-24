#!/usr/bin/env python3
"""Add WebSite JSON-LD schema to pages that don't have it."""
import re, glob, os

WEBSITE_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "AMY Electric",
  "url": "https://amyelectric.com",
  "sameAs": [
    "https://www.yelp.com/biz/amy-electric-los-angeles",
    "https://www.facebook.com/people/Amy-Electric/100063766463600/"
  ],
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://amyelectric.com/?q={search_term_string}"
    }
  }
}
</script>'''

html_files = sorted(
    glob.glob('/home/amram/WEBSITE/*.html') +
    glob.glob('/home/amram/WEBSITE/blog/*.html')
)
html_files = [f for f in html_files if '/amyelectric-site/' not in f and '/reports/' not in f]

changed = 0
skipped = 0

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already has WebSite schema
    if '"WebSite"' in content:
        skipped += 1
        continue

    # Find the last </script> that closes a JSON-LD block
    # Pattern: </script> followed by newline, where the script contained application/ld+json
    # We look for the last occurrence of a JSON-LD closing pattern
    last_jsonld_end = -1
    # Find all positions of </script> and check if preceded by JSON-LD content
    for m in re.finditer(r'</script>', content):
        pos = m.start()
        # Look backward from this </script> to find the opening <script type="application/ld+json">
        preceding = content[max(0, pos - 2000):pos]
        if 'application/ld+json' in preceding:
            # Find the LAST </script> that's part of a JSON-LD block
            last_jsonld_end = m.end()

    if last_jsonld_end == -1:
        print(f"  SKIP (no JSON-LD found): {os.path.relpath(filepath, '/home/amram/WEBSITE')}")
        skipped += 1
        continue

    # Insert WebSite schema after the last JSON-LD block
    new_content = content[:last_jsonld_end] + '\n' + WEBSITE_SCHEMA + content[last_jsonld_end:]

    with open(filepath, 'w') as f:
        f.write(new_content)

    changed += 1
    print(f"  {os.path.relpath(filepath, '/home/amram/WEBSITE')}")

print(f"\nTotal: {changed} files changed, {skipped} skipped")
