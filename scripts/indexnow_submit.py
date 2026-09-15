#!/usr/bin/env python3
"""Submit URLs to Bing via IndexNow protocol."""

import sys
import json
import argparse
import urllib.request
import urllib.error
from typing import List, Optional


INDEXNOW_KEY = "16076f14-4d06-4581-b281-38a7a89804ca"
HOST = "amyelectric.com"
ENDPOINT = "https://api.indexnow.org/indexnow"


def submit_urls(urls: List[str], key: str = INDEXNOW_KEY, host: str = HOST) -> dict:
    """Submit a batch of URLs to IndexNow."""
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return {
                "status": response.status,
                "success": True,
                "urls_submitted": len(urls)
            }
    except urllib.error.HTTPError as e:
        return {
            "status": e.code,
            "success": False,
            "error": str(e),
            "urls_submitted": len(urls)
        }
    except Exception as e:
        return {
            "status": 0,
            "success": False,
            "error": str(e),
            "urls_submitted": len(urls)
        }


def verify_key(key: str = INDEXNOW_KEY, host: str = HOST) -> bool:
    """Verify IndexNow key is accessible at the declared location."""
    url = f"https://{host}/{key}.txt"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8').strip()
            return content == key
    except Exception:
        return False


def submit_from_file(filepath: str, key: str = INDEXNOW_KEY, host: str = HOST) -> dict:
    """Submit URLs from a file (one URL per line)."""
    with open(filepath, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return submit_urls(urls, key, host)


def main():
    parser = argparse.ArgumentParser(description="Submit URLs to Bing via IndexNow")
    parser.add_argument("--host", default=HOST, help="Host domain")
    parser.add_argument("--key", default=INDEXNOW_KEY, help="IndexNow key")
    parser.add_argument("--urls", nargs="+", help="URLs to submit")
    parser.add_argument("--urls-file", help="File with URLs (one per line)")
    parser.add_argument("--verify-only", action="store_true", help="Only verify key")
    
    args = parser.parse_args()
    
    if args.verify_only:
        valid = verify_key(args.key, args.host)
        print(json.dumps({"key_valid": valid, "host": args.host}))
        sys.exit(0 if valid else 1)
    
    if args.urls_file:
        result = submit_from_file(args.urls_file, args.key, args.host)
    elif args.urls:
        result = submit_urls(args.urls, args.key, args.host)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
