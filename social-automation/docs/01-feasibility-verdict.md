# 01 — Feasibility Verdict (stage by stage)

The honest, stage-by-stage answer to "can Claude Code do the whole lot?" Verified against official
APIs (sources in [07-sources.md](07-sources.md)). Each stage lists **what's possible**, **the tool
that does it**, and **the real limits**. Tailored to TEFL Heaven (teach-English-abroad: destinations,
teacher stories, how-to, course promos).

Legend: ✅ works well · ⚠️ works with caveats · ✗ not possible via official API

---

## Stage 1 — Planning & ideation ✅

**Verdict: Claude's home turf.** Content calendars, angle selection, hook lines, scripts, shot
lists, captions, hashtags, A/B titles, and repurposing one idea into an IG Reel + YT Short + TikTok
— all native LLM work, no external tool needed.

- For TEFL Heaven: "5 things nobody tells you about teaching in Vietnam," teacher testimonial Reels,
  "a day in the life" Shorts, course-deadline promos, destination carousels.
- Drive it from a structured plan file ([content/calendar.schema.md](../content/calendar.schema.md))
  via a slash command (`/plan`) or the Agent SDK.
- Feed Stage 2 trend data in so the plan is data-informed.

**Limit:** Claude can't *know* today's trends without being given data — that's Stage 2.

---

## Stage 2 — Trend & best-post research ⚠️ (clean on YouTube, gated on IG, scraper-only on TikTok)

**Verdict: Possible, but the quality of access varies sharply by platform.**

| Source | Access | Notes |
|---|---|---|
| **YouTube Data API** | ✅ Clean | `videos.list?chart=mostPopular` costs **1 unit**; `search.list` costs **100** — prefer mostPopular |
| **Instagram Hashtag Search API** | ⚠️ Gated | Business account + App Review (*Instagram Public Content Access*); **max 30 hashtags / rolling 7 days** |
| **Google Trends** | ⚠️ Unofficial | `pytrends` only (no official API); fragile, rate-limited, normalized 0–100 |
| **TikTok Creative Center** | ✗ No API | Web-only; ToS **bans** automated harvesting |
| **TikTok Research / Commercial APIs** | ✗ For us | Approved **academic/non-profit researchers only** — commercial users ineligible |
| Apify / Ensemble / RapidAPI scrapers | ⚠️ 3rd-party | Real for TikTok/IG/YT, but **ToS-sensitive**; vendor "compliant" labels are unverified |

**How Claude uses it:** pull raw data → Claude clusters patterns (formats, hooks, sounds, post times)
→ folds insights into Stage 1.

**Limit:** **There is no commercially viable first-party TikTok trend API.** Automated TikTok trend
ingestion means third-party scrapers (ToS risk). YouTube is clean and cheap; IG is clean but gated.

---

## Stage 3 — Prompt → image / video (Higgsfield) ✅

**Verdict: Yes — Higgsfield has a real official API, SDKs, and an MCP server.**

- **Official Higgsfield Cloud API.** Base `https://platform.higgsfield.ai`; auth header
  `Authorization: Key KEY_ID:KEY_SECRET` (an ID+secret pair, **not** a Bearer token); keys from
  `cloud.higgsfield.ai/api-keys`. Official **Python (`higgsfield-client`), Node (`higgsfield-js`),
  and CLI** SDKs.
- **Models:** **Soul** / Soul 2.0 (flagship photoreal image, style presets, Soul ID character
  consistency); **DoP** (image-to-video / text-to-video, 50+ camera-motion presets); **Speak**
  (lip-sync avatars). Also routes to Sora 2, Veo 3.1, Kling, Nano Banana, Flux. Up to ~4K images,
  ~15s video.
- **Pattern:** async — `submit`/`subscribe` a job → poll `/requests/{id}/status` (or use a
  `webhook_url`) → read output `images[].url` / `video`. **Failed jobs refund credits.**
- **Official MCP** (`higgsfield.ai/mcp`) + several community MCP servers — so Claude Code can drive it
  as MCP tools directly.
- **Billing:** credit-based (same credits as the platform account; no separate per-call API price
  sheet). Consumer tiers ~Starter $15 / Plus $39 / Ultra $99; a Soul image ≈ 0.25 credits.
- **Per-call fallbacks** (clearer per-generation pricing for just Soul/DoP): **Segmind**
  (~$0.12/image, ~$0.86/video) and **WaveSpeedAI**. ⚠️ Correction from first draft: **fal.ai,
  Replicate, PiAPI, and Kie.ai do *not* host Higgsfield's proprietary Soul/DoP models.**

The scaffolding hides Higgsfield behind one adapter
([scripts/generate_media.md](../scripts/generate_media.md)) so you can swap the official API for
Segmind/WaveSpeed without touching the pipeline.

**Hard limit:** the Anthropic/Claude API **cannot generate images or video** — an external model is
mandatory for this stage.

---

## Stage 4 — Media storage ✅

**Verdict: Trivial and fully automatable, and you may not even need your own bucket.**

- **Blotato can host the media for you:** pass any public URL in `mediaUrls` (Blotato fetches it),
  or `POST /v2/media` (host-by-URL → Blotato URL), or `POST /v2/media/uploads` (presigned PUT →
  `publicUrl`). File size limit ~200 MB (docs vary).
- For durability + your own metadata/analytics, also keep originals in **S3 / R2 / GCS** with a
  record (prompt, model, credit cost, the calendar row, URL).

**Limit:** None of consequence.

---

## Stage 5 — Scheduling ✅

**Verdict: Built into Blotato.**

- On `POST /v2/posts`, add a **top-level** `scheduledTime` (ISO-8601 with offset, e.g.
  `2026-06-02T17:00:00+00:00`) — Blotato fires it then. Or `useNextFreeSlot: true` for the next
  Content Calendar slot. **If you nest these inside `post`, they're ignored and it posts immediately.**
- Alternatively run your own cron / GitHub Actions / Claude Code **Routines** and post at the moment.

Claude can compute *optimal* post times per platform from past metrics and write them in.

---

## Stage 6 — Posting ✅

**Verdict: Yes — build-vs-buy choice.**

- **Buy: Blotato API** — one API posts to **9 platforms** (Instagram, TikTok, YouTube, Facebook,
  X/Twitter, LinkedIn, Pinterest, Threads, Bluesky). Base `https://backend.blotato.com/v2`, header
  `blotato-api-key`. Flow: media (URL or upload) → `POST /v2/posts` with per-platform `target`
  options (TikTok privacy/disclosure/duet/stitch; YouTube title/privacy/notify). **API is included on
  every paid plan** (Starter ~$29/mo; no separate API add-on). **Official hosted MCP** at
  `https://mcp.blotato.com/mcp` + official **n8n** and **Make** nodes.
- **Build: native APIs** — full control, no tool subscription, but you implement OAuth + App
  Review/audit per platform.

**Platform limits apply either way:** IG ~50 posts/24h (rolling); YouTube ~100 uploads/day (default
quota); TikTok SELF_ONLY + 5 users/24h until audited.

---

## Stage 7 — Measuring success ⚠️ (great on IG/YouTube, not on TikTok)

| Platform | Analytics via API? | How |
|---|---|---|
| **Instagram** | ✅ | Insights API (reach, views, saves, engagement); perm `instagram_manage_insights` |
| **YouTube** | ✅ | **YouTube Analytics API** (queries) + **Reporting API** (bulk CSV) |
| **TikTok** | ✗ for us | Display API is read-only public metadata; real analytics only via researcher-gated Research API or Business/Ads APIs |

**Verdict:** Closed-loop measurement works on IG and YouTube. **TikTok has no commercial analytics
API** — you'd read what limited public metadata the Display API exposes, or pull numbers manually /
via (ToS-risky) scrapers. Blotato returns **no** analytics (it's posting-only; metrics are on their
roadmap). Claude joins metrics to the calendar row and writes learnings that feed the next `/plan`.

---

## Stage 8 — Commenting ⚠️ (platform-dependent)

| Platform | Read comments | Reply / post comments | Notes |
|---|---|---|---|
| **Instagram** | ✅ | ✅ | `instagram_manage_comments`: read, reply, hide, delete |
| **YouTube** | ✅ | ✅ | `commentThreads.insert` / `comments.insert` (write costs ~50 units) |
| **TikTok** | ⚠️ researcher-only | ✗ | **No comment-posting API at all**; reading is Research-API-gated |

**How Claude uses it:** read comments → draft on-brand replies → post on IG/YT via API; TikTok
replies go to a human queue. Gate auto-replies behind review early — auto-comment spam is the fastest
route to a shadowban. (Blotato has no comment API either.)

---

## Bottom line

You can build a Claude-Code-orchestrated system that plans content, researches trends (cleanly on
YouTube, gated on IG, scraper-only on TikTok), generates images/videos with Higgsfield, stores them
(Blotato can host), schedules and posts to IG/YouTube/TikTok via Blotato, pulls analytics on IG/YT,
and replies to comments on IG/YT. The non-negotiables are **TikTok-shaped**: the public-posting
audit, no TikTok comment API, no TikTok commercial analytics, and no TikTok trend API. Instagram
needs Meta App Review; YouTube is now the easy platform. And Claude always needs an external model
(Higgsfield) for media. Design around those and the rest is engineering.
</content>
