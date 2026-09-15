#!/usr/bin/env python3
"""Pull backlink data from Bing Webmaster Tools API."""

import sys
import json
import argparse
import urllib.request
import urllib.error
import os
from typing import Optional


BING_API_KEY = os.environ.get("BING_WEBMASTER_API_KEY", "")


def get_backlinks(url: str, api_key: str = BING_API_KEY, count: int = 50) -> dict:
    """Fetch backlinks for a URL from Bing Webmaster Tools API."""
    if not api_key:
        return {
            "error": "BING_WEBMASTER_API_KEY not set",
            "url": url,
            "backlinks": []
        }
    
    # Bing Webmaster Tools API endpoint for backlinks
    endpoint = f"https://api.bing.com/webmaster/v1.0/backlinks?url={url}&count={count}"
    
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Basic {api_key}",
            "User-Agent": "Mozilla/5.0"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return {
                "url": url,
                "backlinks": data.get("d", {}).get("results", []),
                "total": data.get("d", {}).get("count", 0)
            }
    except urllib.error.HTTPError as e:
        return {
            "error": f"HTTP {e.code}: {e.reason}",
            "url": url,
            "backlinks": []
        }
    except Exception as e:
        return {
            "error": str(e),
            "url": url,
            "backlinks": []
        }


def compare_backlinks(url_a: str, url_b: str, api_key: str = BING_API_KEY) -> dict:
    """Compare backlink profiles between two URLs."""
    backlinks_a = get_backlinks(url_a, api_key)
    backlinks_b = get_backlinks(url_b, api_key)
    
    return {
        "url_a": url_a,
        "url_b": url_b,
        "backlinks_a": backlinks_a,
        "backlinks_b": backlinks_b,
        "comparison": {
            "count_a": backlinks_a.get("total", 0),
            "count_b": backlinks_b.get("total", 0)
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Bing backlink analysis")
    parser.add_argument("command", choices=["links", "compare"], help="Command to run")
    parser.add_argument("urls", nargs="*", help="URLs to analyze")
    parser.add_argument("--api-key", default=BING_API_KEY, help="Bing API key")
    parser.add_argument("--count", type=int, default=50, help="Number of backlinks to fetch")
    
    args = parser.parse_args()
    
    if args.command == "links":
        if len(args.urls) != 1:
            print("Error: links command requires exactly one URL")
            sys.exit(1)
        result = get_backlinks(args.urls[0], args.api_key, args.count)
    elif args.command == "compare":
        if len(args.urls) != 2:
            print("Error: compare command requires exactly two URLs")
            sys.exit(1)
        result = compare_backlinks(args.urls[0], args.urls[1], args.api_key)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
