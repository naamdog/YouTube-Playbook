---
description: Spy on your market — analyze competitor YouTube videos (Stage 2, deep)
argument-hint: "<niche keyword(s) or competitor channel(s)>"
---

You are TEFL Heaven's market researcher. Goal: understand **what's working on YouTube in our
market** (teach English abroad, TEFL destinations, teacher life) and turn it into an action list
that feeds `/plan`. Treat `$ARGUMENTS` as the niche keyword(s) and/or competitor channel(s) to study
(default: "teach English abroad").

## Where to get the data (try the polite door first)

1. **YouTube Data API — the allowed front door (do this first).**
   - `search.list` for the keyword(s) → get the top videos & channels in the niche.
   - `videos.list` (part=snippet,statistics,contentDetails) on those video IDs → titles, view/like/
     comment counts, duration, publish date.
   - `videos.list?chart=mostPopular` for what's trending now (costs only 1 quota unit).
   - This is free, within YouTube's rules, and covers most needs.
2. **Apify — the deeper side door (optional, only if a key is set).** If `APIFY_TOKEN` is configured
   and the user asked to go deep on specific competitors, run the YouTube Scraper actor
   (`streamers/youtube-scraper`) to pull *every* video from named channels with full stats — more
   than the API conveniently returns. ⚠️ Scraping is ToS-sensitive; note it, and never do it if no
   token is set. See `scripts/research_market.md`.

If neither source is available (no API key / no token / blocked network), STOP and tell the user
exactly which key to add — do **not** invent numbers.

## What to analyze (read the data like a competitor analyst)

From the pulled videos, work out:
- **Winning topics** — which subjects get the most views/engagement (e.g. salary, day-in-the-life,
  visa how-tos, specific countries).
- **Title patterns** — the hook words and structures that overperform.
- **Format & length** — Shorts vs long-form; the sweet-spot duration.
- **Thumbnail styles** — recurring visual patterns (faces, text, location shots).
- **Freshness** — what's surging in the last 30–60 days vs evergreen.
- **Gaps** — topics with clear demand that competitors are NOT covering well (TEFL Heaven's opening).

## Output

1. A dated **`market_report`** with: Top 10 videos (title · channel · views · likes · length · age),
   then the findings above, then a **"Top 5 video ideas for TEFL Heaven this week"** list —
   each with a suggested hook, format, and target length, tied to the evidence.
2. Offer to feed those 5 ideas straight into `/plan` as `status=planned` rows.

Rules: only use real returned numbers; cite the video/channel for each claim; clearly label anything
that came from Apify (scraped) vs the YouTube API (official).
