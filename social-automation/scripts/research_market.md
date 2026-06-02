# Stage 2 (deep) — research_market: understand competitor YouTube videos

Powers the `/research` command. Two ways to get competitor data: the **YouTube Data API** (free,
allowed, do first) and **Apify** (paid, scraped, deeper). Both return rows of videos that Claude then
analyzes into a "what's working" report.

---

## Door 1 — YouTube Data API (the polite front door)

Free, within YouTube's rules. Needs `YOUTUBE_API_KEY` (from a Google Cloud project).

```python
import os, requests
KEY = os.environ["YOUTUBE_API_KEY"]
Y = "https://www.googleapis.com/youtube/v3"

def search_niche(query, n=25):
    """Find the top videos in your market by keyword. Costs ~100 quota units."""
    r = requests.get(f"{Y}/search", params={
        "key": KEY, "q": query, "part": "snippet",
        "type": "video", "order": "viewCount", "maxResults": n,
        "relevanceLanguage": "en",
    }, timeout=30)
    r.raise_for_status()
    return [it["id"]["videoId"] for it in r.json()["items"]]

def video_stats(video_ids):
    """Get full stats for a batch of videos. Costs ~1 quota unit per call (up to 50 ids)."""
    r = requests.get(f"{Y}/videos", params={
        "key": KEY, "id": ",".join(video_ids),
        "part": "snippet,statistics,contentDetails",
    }, timeout=30)
    r.raise_for_status()
    rows = []
    for v in r.json()["items"]:
        rows.append({
            "title":    v["snippet"]["title"],
            "channel":  v["snippet"]["channelTitle"],
            "published":v["snippet"]["publishedAt"],
            "views":    int(v["statistics"].get("viewCount", 0)),
            "likes":    int(v["statistics"].get("likeCount", 0)),
            "comments": int(v["statistics"].get("commentCount", 0)),
            "duration": v["contentDetails"]["duration"],   # ISO-8601, e.g. PT3M12S
            "url":      f"https://youtu.be/{v['id']}",
        })
    return rows

# Usage:
ids  = search_niche("teach English abroad")
rows = video_stats(ids)              # hand `rows` to Claude to analyze
```

---

## Door 2 — Apify YouTube Scraper (deeper, optional, ToS-sensitive)

Use when you want *everything* from named competitor channels (more than the API hands over neatly).
Needs `APIFY_TOKEN`. ⚠️ Scraping is against YouTube ToS — low risk, common, but your call.

```python
import os, requests, time
TOKEN = os.environ["APIFY_TOKEN"]
ACTOR = "streamers~youtube-scraper"      # https://apify.com/streamers/youtube-scraper

def apify_channel_videos(channel_urls, max_per_channel=50):
    # 1) start the actor run
    run = requests.post(
        f"https://api.apify.com/v2/acts/{ACTOR}/runs?token={TOKEN}",
        json={"startUrls": [{"url": u} for u in channel_urls],
              "maxResults": max_per_channel},
        timeout=60,
    ).json()["data"]
    run_id, dataset_id = run["id"], run["defaultDatasetId"]

    # 2) wait for it to finish
    while True:
        status = requests.get(
            f"https://api.apify.com/v2/actor-runs/{run_id}?token={TOKEN}", timeout=30
        ).json()["data"]["status"]
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        time.sleep(5)

    # 3) pull the results (one row per video: title, views, likes, date, length, etc.)
    items = requests.get(
        f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={TOKEN}&format=json",
        timeout=60,
    ).json()
    return items

# Usage:
# rows = apify_channel_videos(["https://www.youtube.com/@SomeTEFLChannel"])
```

---

## What Claude does with `rows`

Hand the rows (from either door) to Claude with a prompt like:

> "Here are competitor YouTube videos in the 'teach English abroad' market. Identify: winning topics,
>  title patterns, best length, thumbnail styles, what's surging in the last 60 days, and content gaps
>  TEFL Heaven could own. Then give me 5 concrete video ideas (hook + format + length) backed by the
>  data. Cite the video/channel for each claim. Don't invent numbers."

Save the answer as a dated `market_report` and offer to push the 5 ideas into the calendar via
`/plan` (as `status=planned` rows).

> A small runnable version you can try on your own machine is in
> [research_market_demo.py](research_market_demo.py).
