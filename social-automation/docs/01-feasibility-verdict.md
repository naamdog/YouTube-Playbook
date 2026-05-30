# 01 — Feasibility Verdict (stage by stage)

The honest, stage-by-stage answer to "can Claude Code do the whole lot?" Each stage lists **what's
possible**, **the tool that does it**, and **the real limits**. Tailored to TEFL Heaven's niche
(teach-English-abroad: destination content, teacher stories, how-to, course promos).

Legend: ✅ works well · ⚠️ works with caveats · ✗ not possible via official API

---

## Stage 1 — Planning & ideation ✅

**Verdict: Claude's home turf.** Content calendars, angle selection, hook lines, scripts, shot
lists, captions, hashtags, A/B titles, and repurposing one idea into an IG Reel + YT Short + TikTok
— all native LLM work, no external tool needed.

- For TEFL Heaven: "5 things nobody tells you about teaching in Vietnam," teacher testimonial Reels,
  "a day in the life" Shorts, course-deadline promos, destination highlight carousels.
- Drive it from a structured plan file ([content/calendar.schema.md](../content/calendar.schema.md))
  via a slash command (`/plan`) or the Agent SDK.
- Feed Stage 2 trend data in so the plan is data-informed.

**Limit:** Claude can't *know* today's trends without being given data — that's Stage 2.

---

## Stage 2 — Trend & best-post research ⚠️ (mostly works)

**Verdict: Possible. The clean sources are rate-limited; the richest sources are scraping (ToS risk).**

| Source | Access | Notes |
|---|---|---|
| YouTube Data API (`search`, `videos`, `mostPopular`) | ✅ Official | Niche search + trending; costs quota |
| Google Trends | ⚠️ Unofficial (`pytrends`) | No official API; libraries break periodically |
| TikTok Creative Center (trending hashtags/sounds) | ⚠️ Web UI; no clean public API | Programmatic pull = scraping / 3rd-party |
| Instagram Hashtag Search API | ⚠️ Graph API, restricted | Rate-limited; useful for hashtag volume |
| Apify actors (TikTok/IG/YT scrapers) | ⚠️ 3rd-party paid | Strong for competitor/best-post mining; **ToS grey area** |
| Ensemble Data / RapidAPI trend endpoints | ⚠️ 3rd-party paid | Convenient, unofficial |

**How Claude uses it:** pull raw trend/competitor data → Claude analyzes patterns (formats, hooks,
sounds, post times) → folds insights into Stage 1.

**Limit:** "Research competitors' best posts" usually means scraping, which violates platform ToS to
varying degrees. Use official APIs first; treat scraping as informed, opt-in risk.

---

## Stage 3 — Prompt → image / video (Higgsfield) ✅

**Verdict: Yes. Higgsfield offers a Cloud API for programmatic generation.**

- The Higgsfield consumer app (`higgsfield.ai`) does AI **images** (incl. the "Soul" model) and
  **video** (image-to-video / text-to-video with camera & motion presets).
- A separate **Higgsfield Cloud** offering exposes generation via API key + a **credit-based** model.
  The standard async pattern applies: **submit a job → poll → receive output URL(s).**
- **⚠️ confirm** the exact base URL, endpoint paths, request schema, and per-credit costs from your
  logged-in Higgsfield Cloud dashboard / API-keys page before building.
- **Fallbacks** if a needed model isn't covered: **fal.ai**, **Kie.ai**, **PiAPI**, **Replicate**
  host many image/video models behind clean APIs.

The scaffolding hides Higgsfield behind one adapter
([scripts/generate_media.md](../scripts/generate_media.md)) so you can drop in the confirmed endpoint
without touching the rest of the pipeline.

**Hard limit:** the Anthropic/Claude API **cannot generate images or video** — an external model is
mandatory for this stage.

---

## Stage 4 — Media storage ✅

**Verdict: Trivial and fully automatable.**

- Store generated media in object storage (**S3 / Cloudflare R2 / GCS**) with a metadata record
  (prompt, model, cost, the calendar row, public/signed URL).
- **Blotato needs a public URL** for media — it has an upload endpoint that ingests a source URL and
  returns a Blotato-hosted URL. So either host on R2/S3 and pass the URL, or upload into Blotato.

**Limit:** None of consequence. Decide: self-host (R2) for durability + your own analytics, or lean
on Blotato hosting for simplicity.

---

## Stage 5 — Scheduling ✅

**Verdict: Two clean options.**

1. **Blotato-native:** the create-post call accepts a future `scheduledTime` (ISO-8601). Simplest.
2. **Your own scheduler:** cron / queue / n8n Schedule Trigger / GitHub Actions `schedule:` that runs
   the pipeline and posts at the right moment.

Claude can compute *optimal* posting times per platform/audience from past metrics and write them in.

---

## Stage 6 — Posting ✅

**Verdict: Yes — build-vs-buy choice.**

- **Buy: Blotato API** — one API posts to ≈**9 platforms** (Instagram, TikTok, YouTube, Facebook,
  Threads, LinkedIn, X/Twitter, Pinterest, Bluesky). Handles per-platform options. Typically a
  **two-step** flow (host media → create post). Needs a **paid plan with API access**. Community
  **MCP servers** exist, so Claude Code can call it as MCP tools. **⚠️ confirm** current endpoints/
  pricing.
- **Build: native APIs** — full control, no per-seat tool cost, but you implement OAuth + publishing
  + audits per platform yourself.

**Platform limits apply either way:** IG ~25 posts/24h; YouTube ~6 uploads/day default; TikTok
SELF_ONLY until audited.

---

## Stage 7 — Measuring success ✅ (native analytics APIs)

**Verdict: Yes.**

- **Instagram:** Insights via Graph API (reach, impressions, engagement, saves…).
- **YouTube:** **YouTube Analytics & Reporting API** (views, watch time, retention, traffic sources).
- **TikTok:** analytics via Display/Business APIs (more limited; richer metrics need a Business
  account / the restricted Research API).

Claude pulls these, joins to the calendar row, writes a performance report, and feeds learnings into
the next Stage 1 — the loop closes. Blotato is posting-focused; go native for metrics.

---

## Stage 8 — Commenting ⚠️ (platform-dependent)

**Verdict: Mixed. This is where "the whole lot" hits a wall on TikTok.**

| Platform | Read comments | Reply / post comments | Notes |
|---|---|---|---|
| **Instagram** | ✅ | ✅ | `instagram_manage_comments`: read, reply, hide, delete |
| **YouTube** | ✅ | ✅ | `commentThreads.insert` / `comments.insert` |
| **TikTok** | ⚠️ limited | ✗ | **No public API to post comments** |

**How Claude uses it:** read comments → draft on-brand replies → post on IG/YT via API; TikTok
replies go to a human queue. Gate auto-replies behind review early — auto-comment spam is the fastest
route to a shadowban.

---

## Bottom line

You can build a Claude-Code-orchestrated system that plans content, researches trends, generates
images/videos with Higgsfield, stores them, schedules and posts to IG/YouTube/TikTok via Blotato (or
native APIs), pulls analytics, and replies to comments on IG and YouTube. The non-negotiables are
**platform-imposed**: TikTok's public-posting audit, TikTok's missing comment API, YouTube's upload
quota, Instagram's 25/day cap, and Claude needing an external model for any media. Design around
those five and the rest is engineering.
</content>
