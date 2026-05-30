---
description: Research current trends for the TEFL niche (Stage 2)
---

Build a `trend_digest` for TEFL Heaven's niche (teach English abroad, destinations, teacher life).
Prefer official APIs; flag any scraping as ToS-sensitive.

1. Pull from available sources:
   - YouTube Data API: `search` + `mostPopular` for niche keywords (e.g. "teach English abroad",
     "TEFL Vietnam", "day in the life teacher").
   - Google Trends (pytrends) for rising queries (note: unofficial).
   - TikTok Creative Center / Apify trend actors for trending hashtags & sounds (note: ToS risk).
   - Instagram hashtag search (if configured).
2. Cluster the raw data into: trending FORMATS, HOOK patterns, SOUNDS, TOPICS, best POST TIMES.
3. For each cluster, note why it's working and how it maps to TEFL Heaven.
4. Write the result as a dated `trend_digest` for `/plan` to consume.
5. Call out the single highest-opportunity trend to act on this week.

Do not fabricate numbers — only report what the APIs returned. If a source is unavailable, say so.
</content>
