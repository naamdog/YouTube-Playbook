# Stage 7 — report (analytics pull → learnings)

Blotato is posting-focused, so metrics come from **native analytics APIs**. Pull at ~24h and ~7d,
join to the row, let Claude write `learnings` that feed the next `/plan`.

## Instagram — Insights (Graph API)
```http
GET https://graph.facebook.com/v21.0/{ig_media_id}/insights
    ?metric=reach,impressions,saved,likes,comments,shares,total_interactions
    &access_token={IG_LONG_LIVED_TOKEN}
```

## YouTube — YouTube Analytics API
```http
GET https://youtubeanalytics.googleapis.com/v2/reports
    ?ids=channel==MINE
    &startDate=...&endDate=...
    &metrics=views,estimatedMinutesWatched,averageViewPercentage,likes,comments,shares
    &filters=video=={video_id}
# OAuth bearer token with scope yt-analytics.readonly
```

## TikTok — analytics (limited)
```text
Video metrics via TikTok Display/Business APIs (Business account recommended).
Richer engagement requires the Research API (restricted access). Capture what you can:
views, likes, comments, shares, profile-level follower deltas.
```

## Join + analyze
```python
for row in store.where(status="posted"):
    m = {}
    if row.post_id_instagram: m["instagram"] = ig_insights(row.post_id_instagram)
    if row.post_id_youtube:   m["youtube"]   = yt_analytics(row.post_id_youtube)
    if row.post_id_tiktok:    m["tiktok"]    = tiktok_metrics(row.post_id_tiktok)
    store.set(row.id, "metrics_24h", m)   # or metrics_7d on the 7-day pass

# Hand metrics + the row's hook/format to Claude:
#   "Compare these TEFL posts. Which hooks/formats/post-times drove the best
#    retention & engagement? Output 3 concrete rules for next week's /plan."
# Write the response to row.learnings — this closes the loop.
```
