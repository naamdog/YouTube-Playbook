---
description: Pull analytics and write learnings (Stage 7)
---

Measure posted content and close the loop.

1. Select `status=posted` rows due for a 24h or 7d measurement pass (`--due`).
2. Pull native analytics per `scripts/report.md`:
   - Instagram Insights, YouTube Analytics API, TikTok metrics (limited).
3. Store raw metrics in `metrics_24h` / `metrics_7d`. Mark `status=measured` after the 7d pass.
4. Analyze across recent posts: which hooks, formats, lengths, and post-times drove the best
   retention and engagement? Produce 3–5 concrete, actionable rules.
5. Write those to each row's `learnings` and to a rolling `learnings` note that `/plan` reads.
6. Report a short performance summary (winners, losers, the one change to make next week).

Only use real returned metrics. Never invent numbers.
