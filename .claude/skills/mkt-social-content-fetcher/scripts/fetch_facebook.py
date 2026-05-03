# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Fetch viral AI posts from Facebook pages using Apify."""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
APIFY_BASE = "https://api.apify.com/v2"
ACTOR_ID = "apify~facebook-posts-scraper"


def find_sources_file(sources_file: str | None) -> Path | None:
    if sources_file:
        return Path(sources_file)
    candidates = [
        Path(__file__).parent.parent / "sources.json",
        Path(".claude/skills/mkt-social-content-fetcher/sources.json"),
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def load_pages(sources_file: str | None, pages_arg: str | None) -> list[str]:
    if pages_arg:
        return [p.strip() for p in pages_arg.split(",")]
    path = find_sources_file(sources_file)
    if path:
        data = json.loads(path.read_text())
        return [entry["page"] for entry in data.get("facebook", [])]
    return []


def run_actor(pages: list[str], date_from: str, min_likes: int) -> list[dict]:
    if not APIFY_TOKEN:
        print("Error: APIFY_API_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    input_data = {
        "startUrls": [
            {"url": f"https://www.facebook.com/{p}"} for p in pages
        ],
        "resultsLimit": 20,
        "onlyPostsNewerThan": date_from,
    }

    headers = {"Content-Type": "application/json"}
    params = {"token": APIFY_TOKEN}

    # Start actor run
    resp = requests.post(
        f"{APIFY_BASE}/acts/{ACTOR_ID}/runs",
        headers=headers,
        params=params,
        json=input_data,
        timeout=30,
    )
    resp.raise_for_status()
    run_id = resp.json()["data"]["id"]

    # Poll until finished (max 5 min)
    deadline = time.time() + 300
    while time.time() < deadline:
        time.sleep(10)
        status_resp = requests.get(
            f"{APIFY_BASE}/acts/{ACTOR_ID}/runs/{run_id}",
            params=params,
            timeout=15,
        )
        status_resp.raise_for_status()
        status = status_resp.json()["data"]["status"]
        if status == "SUCCEEDED":
            break
        if status in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"Error: Apify actor run {status}", file=sys.stderr)
            sys.exit(1)

    # Fetch dataset items
    dataset_resp = requests.get(
        f"{APIFY_BASE}/acts/{ACTOR_ID}/runs/{run_id}/dataset/items",
        params={**params, "format": "json", "limit": 200},
        timeout=30,
    )
    dataset_resp.raise_for_status()
    raw_items = dataset_resp.json()

    # Normalize
    items = []
    for p in raw_items:
        likes = p.get("likes", 0) or 0
        if likes < min_likes:
            continue
        items.append({
            "title": (p.get("text") or p.get("message") or "")[:200],
            "url": p.get("url", ""),
            "author": p.get("pageName", "") or p.get("authorName", ""),
            "views": p.get("videoViewCount", 0) or 0,
            "likes": likes,
            "shares": p.get("shares", 0) or 0,
            "comments": p.get("comments", 0) or 0,
            "published_at": p.get("date", "")[:10] if p.get("date") else "",
            "tags": [],
            "thumbnail_url": p.get("media", [{}])[0].get("thumbnail", "") if p.get("media") else "",
        })

    items.sort(key=lambda x: x["likes"], reverse=True)
    return items


def main():
    parser = argparse.ArgumentParser(description="Fetch viral Facebook AI posts via Apify")
    parser.add_argument("--pages", help="Comma-separated Facebook page names (overrides sources.json)")
    parser.add_argument("--date-from", help="Fetch posts from this date YYYY-MM-DD (default: 7 days ago)")
    parser.add_argument("--min-likes", type=int, default=100, help="Minimum likes filter")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--sources-file", help="Path to sources.json")
    args = parser.parse_args()

    pages = load_pages(args.sources_file, args.pages)
    if not pages:
        print("Error: No Facebook pages found. Provide --pages or configure sources.json", file=sys.stderr)
        sys.exit(1)

    date_from = args.date_from or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    items = run_actor(pages, date_from, args.min_likes)

    result = {
        "source": "facebook",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "date_from": date_from,
        "pages_fetched": pages,
        "total_items": len(items),
        "items": items,
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Saved {len(items)} Facebook items to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
