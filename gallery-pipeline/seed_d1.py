#!/usr/bin/env python3
"""Seed D1 with gallery photos using wrangler's OAuth token."""

import csv
import json
import os
import sys
import urllib.request

DB_ID = "f2a77e29-fcb5-4db2-b1b2-6b18095ba093"
ACCOUNT_ID = "a08528fe46962a4d732de2d8d30eeef5"
TOKEN_FILE = os.path.expanduser("~/.wrangler/config/default.toml")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(SCRIPT_DIR, "photo_manifest.csv")
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "processed")
BATCH_SIZE = 50


def get_token():
    with open(TOKEN_FILE) as f:
        for line in f:
            if line.startswith("oauth_token"):
                return line.split("=", 1)[1].strip().strip('"')
    raise RuntimeError("No OAuth token found")


def run_sql(sql, token):
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/d1/database/{DB_ID}/query"
    data = json.dumps({"sql": sql}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            if not result.get("success"):
                print(f"  API error: {result.get('errors')}", file=sys.stderr)
                return False
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  HTTP {e.code}: {body[:200]}", file=sys.stderr)
        return False


def main():
    token = get_token()
    print(f"Token loaded ({len(token)} chars)")

    entries = []
    with open(MANIFEST) as f:
        for row in csv.DictReader(f):
            fname = row["filename"]
            category = row["category"]
            description = row["description"]
            location = row["location"]
            date = row.get("date", "")
            stem = os.path.splitext(fname)[0].lower()
            cat_dir = os.path.join(PROCESSED_DIR, category)
            if not os.path.isdir(cat_dir):
                continue
            matches = [f for f in os.listdir(cat_dir) if f.endswith(".jpg") and stem in f]
            if not matches:
                continue
            proc_name = matches[0]
            safe = lambda s: str(s).replace("'", "''")
            entries.append(
                f"INSERT INTO gallery_images (filename, category, title, description, location, width, height, shoot_date, created_at) "
                f"VALUES ('{safe(proc_name)}', '{safe(category)}', '{safe(description)}', '{safe(description)}', "
                f"'{safe(location)}', 0, 0, '{safe(date)}', datetime('now'))"
            )

    run_sql("DELETE FROM gallery_images WHERE filename = 'test-photo.jpg';", token)

    total = 0
    for i in range(0, len(entries), BATCH_SIZE):
        batch = entries[i:i + BATCH_SIZE]
        sql = ";\n".join(batch) + ";"
        if run_sql(sql, token):
            total += len(batch)
            print(f"  {total}/{len(entries)} seeded...")
        else:
            print(f"  FAILED at batch starting at {i}")
            break

    count_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/d1/database/{DB_ID}/query"
    count_data = json.dumps({"sql": "SELECT COUNT(*) as total FROM gallery_images;"}).encode()
    count_req = urllib.request.Request(count_url, data=count_data, method="POST")
    count_req.add_header("Content-Type", "application/json")
    count_req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(count_req) as resp:
        result = json.loads(resp.read())
        count = result["result"][0]["total"]
        print(f"\nDone: {count} rows in gallery_images")


if __name__ == "__main__":
    main()
