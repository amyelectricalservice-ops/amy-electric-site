#!/usr/bin/env bash
# ------------------------------------------------------------
# extract_site_images.sh
#   Scans all .html files in the website for <img> tags,
#   extracts the src attribute and the alt attribute (if any),
#   and writes a CSV file: img/site_images.csv
#
#   Usage (run from the project root):
#       chmod +x scripts/extract_site_images.sh
#       ./scripts/extract_site_images.sh
# ------------------------------------------------------------

# Ensure we are in the project root
cd "$(dirname "$(realpath "$0")")/.."

OUTFILE="img/site_images.csv"
echo "source_file,src,alt_text" > "$OUTFILE"

# Find every *.html file, then extract img tags line‑by‑line
while IFS= read -r -d '' htmlfile; do
  # Use grep to pull lines that contain <img>
  while IFS= read -r line; do
    # Collapse multiline tags into one line (remove newlines)
    line=$(echo "$line" | tr -d '\n')
    # Extract the src attribute
    src=$(echo "$line" | grep -oP 'src\s*=\s*"\K[^"]+')
    # Extract the alt attribute (may be missing)
    alt=$(echo "$line" | grep -oP 'alt\s*=\s*"\K[^"]*')
    # If no alt attribute, leave empty
    printf '%s,"%s","%s"\n' "$(realpath --relative-to=. \"$htmlfile\")" "$src" "$alt" >> "$OUTFILE"
  done < <(grep -i -o '<img[^>]*>' "$htmlfile")
# Use null separator for robustness with whitespace in filenames
done < <(find . -type f -name '*.html' -print0)

echo "✅ Extraction complete – results saved to $OUTFILE"
