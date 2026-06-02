# scripts/ — reference implementations

**Annotated, key-gated reference implementations**, written at pseudocode/skeleton level on purpose:
they show the exact API calls and data flow for each stage, but need the secrets in `.env`, and a
couple of endpoints (Higgsfield Cloud, Blotato) must be **confirmed from the live docs/dashboard**
before they'll run. Treat them as the spec for the real code.

| File | Stage | Purpose |
|---|---|---|
| [research_market.md](research_market.md) | 2 | Competitor YouTube analysis — YouTube API (free) + Apify (deep) |
| [research_market_demo.py](research_market_demo.py) | 2 | **Runnable** demo: pull top niche videos via the official YouTube API |
| [generate_media.md](generate_media.md) | 3 | Higgsfield Cloud API: submit → poll → output URL (+ fallbacks) |
| [publish.md](publish.md) | 6 | Blotato host-media → create-post (+ native API notes) |
| [report.md](report.md) | 7 | Pull IG Insights / YouTube Analytics / TikTok metrics |
| [engage.md](engage.md) | 8 | Read comments, Claude drafts replies, post on IG/YT |

Stages 1 (`/plan`) and 2 (`/trends`, `/research`) are driven from Claude Code slash commands in
[`.claude/commands/`](../.claude/commands/), since they're mostly Claude reasoning over data.

> Examples use a Python-ish / `curl` style for clarity. Port to whatever you run the pipeline in
> (Python, Node, or pure Claude Agent SDK tool calls).
