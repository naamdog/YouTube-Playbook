#!/usr/bin/env python3
"""
research_market_demo.py — a tiny, real, runnable "spy on my YouTube market" tool.

Run this on YOUR OWN machine (this cloud sandbox blocks the needed network calls).
It uses the FREE, allowed YouTube Data API (no scraping) to pull the top videos in a
niche and print a plain-English summary you can hand to Claude.

SETUP (one time):
  1. Get a free YouTube Data API key:
       https://console.cloud.google.com  ->  enable "YouTube Data API v3"  ->  create an API key
  2. pip install requests
  3. export YOUTUBE_API_KEY="your-key-here"

RUN:
  python research_market_demo.py "teach English abroad"
  python research_market_demo.py "TEFL Vietnam" --max 30

This stays inside YouTube's rules (official API). For deeper competitor digging
(scraping whole channels), see scripts/research_market.md — Door 2 (Apify).
"""

import os
import sys
import argparse
import requests

Y = "https://www.googleapis.com/youtube/v3"


def iso_duration_to_text(d: str) -> str:
    """Turn 'PT3M12S' into '3m12s' so it's readable."""
    out, num = "", ""
    for ch in d.replace("PT", ""):
        if ch.isdigit():
            num += ch
        else:
            out += num + ch.lower()
            num = ""
    return out or "?"


def search_niche(key: str, query: str, n: int):
    r = requests.get(f"{Y}/search", params={
        "key": key, "q": query, "part": "snippet",
        "type": "video", "order": "viewCount", "maxResults": n,
        "relevanceLanguage": "en",
    }, timeout=30)
    r.raise_for_status()
    return [it["id"]["videoId"] for it in r.json()["items"]]


def video_stats(key: str, video_ids):
    rows = []
    # the videos endpoint takes up to 50 ids per call
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        r = requests.get(f"{Y}/videos", params={
            "key": key, "id": ",".join(batch),
            "part": "snippet,statistics,contentDetails",
        }, timeout=30)
        r.raise_for_status()
        for v in r.json()["items"]:
            s = v.get("statistics", {})
            rows.append({
                "title":    v["snippet"]["title"],
                "channel":  v["snippet"]["channelTitle"],
                "views":    int(s.get("viewCount", 0)),
                "likes":    int(s.get("likeCount", 0)),
                "comments": int(s.get("commentCount", 0)),
                "length":   iso_duration_to_text(v["contentDetails"]["duration"]),
                "url":      f"https://youtu.be/{v['id']}",
            })
    return rows


def main():
    ap = argparse.ArgumentParser(description="Spy on your YouTube market (official API).")
    ap.add_argument("query", nargs="?", default="teach English abroad",
                    help='niche keyword, e.g. "teach English abroad"')
    ap.add_argument("--max", type=int, default=25, help="how many videos to pull (default 25)")
    args = ap.parse_args()

    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("ERROR: set YOUTUBE_API_KEY first (see the setup notes at the top of this file).")

    print(f'\n🔎 Researching YouTube market for: "{args.query}"\n')
    ids = search_niche(key, args.query, args.max)
    rows = video_stats(key, ids)
    rows.sort(key=lambda r: r["views"], reverse=True)

    print(f"Top {len(rows)} videos by views:\n")
    print(f'{"VIEWS":>12}  {"LIKES":>8}  {"LEN":>7}  CHANNEL / TITLE')
    print("-" * 90)
    for r in rows:
        print(f'{r["views"]:>12,}  {r["likes"]:>8,}  {r["length"]:>7}  '
              f'{r["channel"][:22]:22} | {r["title"][:46]}')

    # quick at-a-glance signals
    if rows:
        avg = sum(r["views"] for r in rows) // len(rows)
        longest = max(rows, key=lambda r: len(r["title"]))
        print("\n— Quick signals —")
        print(f"  • Average views across these: {avg:,}")
        print(f'  • Top performer: "{rows[0]["title"]}" ({rows[0]["views"]:,} views) by {rows[0]["channel"]}')
        print(f"  • Tip: paste this whole list to Claude and ask: "
              f'"what topics, titles, and lengths are winning, and give me 5 video ideas?"')
    print()


if __name__ == "__main__":
    main()
