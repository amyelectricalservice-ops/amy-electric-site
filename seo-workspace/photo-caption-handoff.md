# Photo caption handoff (vision pass)

Backlog: /tmp/opencode/photo-caption-backlog.csv (161 rows, all slugs whose
caption still starts with "Electrical project photo").

Columns: slug, source_file, category, city, year, variant400w (thumbnail path)

For each row, open variant400w (or source_file) and write a specific caption
10-125 chars. Output a CSV with columns: slug,caption (optional: action,new_category).

Apply with:
  python3 scripts/apply-photo-captions.py /path/to/captions.csv
  python3 scripts/update-gallery.py
Then run the pre-push gate and push.

Rules for good captions (from update-gallery.py alt_text + gallery.html):
- Start with the subject (panel, conduit, EV charger, lighting, etc.)
- Include one concrete detail (color-coded wiring, NEMA outlet, meter, etc.)
- End with "(work in progress)" or "(finished installation)" or "(equipment detail)"
- Keep under 125 chars (hard cap; alt_text truncates)
- Never include PII, addresses, license plates, or utility account numbers
- If a photo is unusable (blurry, duplicate, PII unredactable): action=cull

Categories (use one): panel, commercial, new-construction, lighting, team,
lifestyle, exterior, other. Recategorize with action=recategorize,new_category=...
