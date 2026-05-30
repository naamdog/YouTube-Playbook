# Social Media Automation with Claude Code — Deep Dive

> A feasibility deep-dive for **TEFL Heaven**: can Claude Code automate the *whole* social-media
> content lifecycle across **Instagram, YouTube, and TikTok**?

**The question:** plan content, research best trends/posts, go prompt → image/video (using
**Higgsfield**), store the media, schedule posts, post them, measure each post's success, and
comment — with **Blotato** as the posting layer. Is there a way to do all of it?

**Short answer: Yes — most of it works today.** Claude Code can be the *orchestrating brain* that
calls external tools through **MCP servers** and HTTP APIs. Every stage you asked about maps to a
real, working API. The ceiling is set by the **platforms**, not by Claude.

| Stage | Feasible? | How |
|---|---|---|
| 1. Planning & ideation (calendar, hooks, scripts, captions) | ✅ Fully | Claude itself |
| 2. Trend / best-post research | ✅ Mostly | Platform APIs + trend APIs + scrapers (ToS caveats) |
| 3. Prompt → image / video | ✅ Yes | **Higgsfield Cloud API** + fallbacks (fal.ai / Kie.ai / PiAPI) |
| 4. Media storage | ✅ Fully | Object storage (S3 / R2 / GCS) or Blotato hosted media |
| 5. Scheduling | ✅ Yes | Blotato `scheduledTime`, or your own cron/queue |
| 6. Posting | ✅ Yes | **Blotato API** (≈9 platforms) *or* native platform APIs |
| 7. Measuring success | ✅ Yes (native APIs) | IG Insights, YouTube Analytics, TikTok analytics |
| 8. Commenting | ⚠️ Partial | IG ✅ / YouTube ✅ / **TikTok ✗ (no comment-posting API)** |

## The five hard limits to design around (platform-imposed, not Claude-imposed)

1. **TikTok audit gate** — until your TikTok app passes audit, every API post is forced to
   `SELF_ONLY` (private). No public TikToks via API before audit.
2. **TikTok has no comment-posting API** — auto-replying to TikTok comments isn't possible officially.
3. **YouTube upload quota** — `videos.insert` costs ~1600 units; the default 10,000 units/day ≈
   **~6 uploads/day**. Request a quota increase for volume.
4. **Instagram cap** — ~**25 API-published posts / 24h** per account; needs a Business/Creator account
   + App Review for `instagram_content_publish`.
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

## Starter scaffolding (in this folder)

- [config/mcp.example.json](config/mcp.example.json) — Claude Code MCP servers (Blotato + custom Higgsfield).
- [.env.example](.env.example) — every API key/secret you'll need.
- [content/calendar.schema.md](content/calendar.schema.md) + [content/calendar.example.csv](content/calendar.example.csv) — the data model that drives the pipeline.
- [scripts/](scripts/) — annotated, key-gated reference implementations for each stage.
- [.claude/commands/](.claude/commands/) — Claude Code slash commands: `/plan`, `/trends`, `/publish`, `/report`, `/engage`.

## Recommended stack (TL;DR)

```
Claude Code (orchestrator + content brain)
        │  via MCP / HTTP
        ├── Higgsfield Cloud API ........ prompt → image/video
        ├── Object storage (S3 / R2) .... durable media + metadata
        ├── Blotato API ................. schedule + post to IG / YT / TikTok (≈9 platforms)
        ├── Native platform APIs ........ analytics + commenting (IG/YT), trend pulls
        └── Trend APIs / Apify actors ... trend & competitor research
```

Realistic effort to a **supervised MVP** across IG + YouTube: **~1 week**. Add TikTok public posting
only after the audit. The slow parts are platform approvals, not Claude.

> **Confidence note:** facts about the native platform APIs and Claude Code are well-established.
> A few specifics for **Higgsfield Cloud** and **Blotato** (exact endpoint paths, request schemas,
> current pricing) should be confirmed from their live dashboards/docs before you build — these are
> flagged **⚠️ confirm** throughout. The architecture keeps each behind a thin adapter so confirming
> them is a drop-in, not a rewrite.
</content>
