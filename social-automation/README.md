# Social Media Automation with Claude Code — Deep Dive

> A feasibility deep-dive for **TEFL Heaven**: can Claude Code automate the *whole* social-media
> content lifecycle across **Instagram, YouTube, and TikTok**?

**The question:** plan content, research best trends/posts, go prompt → image/video (using
**Higgsfield**), store the media, schedule posts, post them, measure each post's success, and
comment — with **Blotato** as the posting layer. Is there a way to do all of it?

**Short answer: Yes — most of it works today,** and the research below is now verified against the
official APIs (sources in [docs/07-sources.md](docs/07-sources.md)). Claude Code is the
*orchestrating brain* that calls external tools through **MCP servers** and HTTP APIs. Every stage
you asked about maps to a real, working API. The ceiling is set by the **platforms**, not by Claude.

| Stage | Feasible? | How |
|---|---|---|
| 1. Planning & ideation (calendar, hooks, scripts, captions) | ✅ Fully | Claude itself |
| 2. Trend / best-post research | ✅ Mostly | YouTube API (clean) · IG hashtag (gated) · TikTok (scrapers only) |
| 3. Prompt → image / video | ✅ Yes | **Higgsfield Cloud API** (`platform.higgsfield.ai`) + Segmind/WaveSpeed fallbacks |
| 4. Media storage | ✅ Fully | S3 / R2 / GCS, or Blotato hosts the media for you |
| 5. Scheduling | ✅ Yes | Blotato `scheduledTime` (ISO-8601), or your own cron |
| 6. Posting | ✅ Yes | **Blotato API** (9 platforms) *or* native platform APIs |
| 7. Measuring success | ✅ Yes (native APIs) | IG Insights, YouTube Analytics — **TikTok ✗ (no commercial analytics API)** |
| 8. Commenting | ⚠️ Partial | IG ✅ / YouTube ✅ / **TikTok ✗ (no comment API)** |

## The constraints to design around (platform-imposed, not Claude-imposed)

After verification, **TikTok is the real bottleneck**, Instagram needs approval, and **YouTube turned
out to be the easy one**:

1. **TikTok audit gate** — until your TikTok app passes audit, every API post is forced to
   `SELF_ONLY` (private), and unaudited apps are capped at **5 posting users / 24h**. No public
   TikToks via API before audit (~2–4 weeks, community estimate).
2. **TikTok is API-poor for the rest** — **no comment-posting API at all**, and **no commercial
   analytics API** (the Display API is read-only public metadata; real analytics is the
   researcher-only Research API). Also no first-party trend API.
3. **Instagram gates + cap** — Business/Creator account + **Meta App Review** for publishing,
   comments, and insights; **~50 API-published posts / 24h** (rolling; carousels count as 1). *(The
   old "25/24h" figure is outdated.)*
4. **YouTube is now generous** — `videos.insert` dropped from ~1600 to **~100 quota units on
   2025-12-04**, so the default 10k/day quota allows **~100 uploads/day**, not ~6. Still needs OAuth
   verification + a compliance audit for production.
5. **Claude can't generate media itself** — any image/video *must* come from Higgsfield (or another
   model). This is why Higgsfield is in the design.

> ⚠️ **This is not "fire-and-forget at scale."** Mass automation, fake engagement, and ToS-breaking
> scraping get accounts banned and carry legal risk. Keep a human in the loop on publish/comment
> until you trust the system. See [docs/05-risks-compliance.md](docs/05-risks-compliance.md).

---

## Read in this order

1. [docs/01-feasibility-verdict.md](docs/01-feasibility-verdict.md) — stage-by-stage verdict.
2. [docs/02-architecture.md](docs/02-architecture.md) — reference architecture, Claude Code at center.
3. [docs/03-capability-matrix.md](docs/03-capability-matrix.md) — hard-facts table: every tool/API, limits, auth.
4. [docs/04-pipeline-playbook.md](docs/04-pipeline-playbook.md) — the runbook for all 8 stages.
5. [docs/05-risks-compliance.md](docs/05-risks-compliance.md) — ToS, rate limits, ban risk.
6. [docs/06-build-plan.md](docs/06-build-plan.md) — phased plan, MVP → full autonomy.
7. [docs/07-sources.md](docs/07-sources.md) — verified source URLs for every claim.

## Starter scaffolding (in this folder)

- [config/mcp.example.json](config/mcp.example.json) — Claude Code MCP servers (official Blotato + Higgsfield).
- [.env.example](.env.example) — every API key/secret you'll need.
- [content/calendar.schema.md](content/calendar.schema.md) + [content/calendar.example.csv](content/calendar.example.csv) — the data model that drives the pipeline.
- [scripts/](scripts/) — annotated reference implementations for each stage, with verified request shapes.
- [.claude/commands/](.claude/commands/) — Claude Code slash commands: `/plan`, `/trends`, `/publish`, `/report`, `/engage`.

## Recommended stack (TL;DR)

```
Claude Code (orchestrator + content brain)
        │  via MCP / HTTP
        ├── Higgsfield Cloud API ........ prompt → image/video (official MCP + SDKs exist)
        ├── Object storage (S3 / R2) .... durable media + metadata (optional; Blotato can host)
        ├── Blotato API ................. schedule + post to IG / YT / TikTok (9 platforms; hosted MCP)
        ├── Native platform APIs ........ analytics + commenting (IG/YT), YouTube trend pulls
        └── Trend APIs / Apify actors ... trend research (IG gated; TikTok = scrapers, ToS risk)
```

Realistic effort to a **supervised MVP** across IG + YouTube: **~1 week**. Add TikTok public posting
only after the audit. The slow parts are platform approvals, not Claude.

> **Two automation gotchas to remember:** (1) interactive skills/slash-commands don't run in
> `claude -p` headless mode — pass the task as a prompt instead; (2) from **2026-06-15**, Agent SDK /
> `claude -p` usage on subscription plans draws from a separate credit pool — budget an API key for
> high-volume runs.
</content>
