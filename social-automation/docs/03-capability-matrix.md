# 03 — Capability Matrix (facts, limits, auth)

Verified against official docs/SDKs as of **2026-05** (sources in [07-sources.md](07-sources.md)).
A few values are flagged **⚠️** where official pages reported inconsistently or blocked automated
fetch; verify those live at integration time.

---

## Blotato (posting / scheduling layer)

| Item | Status | Detail |
|---|---|---|
| Public REST API | ✅ | Base `https://backend.blotato.com/v2`; header `blotato-api-key`; verify with `GET /users/me` |
| Platforms (9) | ✅ | Instagram, YouTube, TikTok, Facebook, X/Twitter, LinkedIn, Pinterest, Threads, Bluesky |
| Media | ✅ | Public URL in `mediaUrls` (no upload), or `POST /v2/media` (host-by-URL), or `POST /v2/media/uploads` (presigned) |
| Scheduling | ✅ | Top-level `scheduledTime` (ISO-8601+offset) or `useNextFreeSlot`; nesting them in `post` = ignored |
| Per-platform options | ✅ | TikTok: `privacyLevel`, `disabledComments/Duet/Stitch`, `isAiGenerated`… · YouTube: `title`, `privacyStatus`, `shouldNotifySubscribers` |
| Content rule | ✅ | `content.platform` must equal `target.targetType`; `accountId` from `GET /v2/users/me/accounts` |
| Plan required | ✅ | **API included on every paid plan** (Starter ~$29/mo, 7-day trial); no separate add-on |
| Analytics back | ✗ | None (on roadmap) → use native analytics APIs |
| Comments | ✗ | No comment/reply endpoint found |
| Integrations | ✅ | **Hosted MCP** `https://mcp.blotato.com/mcp` · official n8n (`@blotato/n8n-nodes-blotato`) · Make · (Zapier "coming soon") |
| ⚠️ confirm | — | Media size (200MB vs 1GB) and Creator/Agency exact pricing reported inconsistently |

---

## Higgsfield (image / video generation)

| Item | Status | Detail |
|---|---|---|
| Official Cloud API | ✅ | Base `https://platform.higgsfield.ai`; auth `Authorization: Key KEY_ID:KEY_SECRET` |
| Keys / dashboard | ✅ | `cloud.higgsfield.ai/api-keys` |
| SDKs | ✅ | Python `higgsfield-client`, Node `higgsfield-js`, CLI |
| Pattern | ✅ | Async `submit`/`subscribe` → poll `/requests/{id}/status` or `webhook_url` → `images[].url` / `video`; failed jobs refund credits |
| Models | ✅ | Soul/Soul 2.0 + Soul ID (image), DoP (`/v1/image2video/dop`), Speak (`/v1/speak/higgsfield`); routes to Sora2/Veo/Kling/Flux |
| Output | ⚠️ | ~4K image; video 5/10s at 480/720/1080p (length/res from resellers — verify) |
| Billing | ✅ | Credit-based (same as platform; no per-call price sheet). Soul image ≈ 0.25 credits |
| MCP | ✅ | Official `higgsfield.ai/mcp` + community MCP servers |
| Per-call fallbacks | ✅ | **Segmind** (~$0.12/img, ~$0.86/video), **WaveSpeedAI**. ✗ NOT on fal.ai/Replicate/PiAPI/Kie |
| Claude native gen | ✗ | Anthropic API cannot generate images/video — external model mandatory |

---

## Instagram (Instagram Graph API / Instagram API with Instagram Login)

| Capability | Status | Detail |
|---|---|---|
| Publish image / carousel / **Reels** / **Stories** | ✅ | Two-step: `POST /{ig-user-id}/media` → `/media_publish`; **professional** (Business/Creator) account |
| **Rate limit** | ⚠️ | **~50 API posts / 24h** (rolling; carousels = 1). *Old "25" is outdated; some sources say 100.* Check `content_publishing_limit` live |
| Insights / analytics | ✅ | `/{ig-media-id}/insights`, `/{ig-user-id}/insights`; perm `instagram_manage_insights` (some metrics need ≥100 followers) |
| Comments read/reply/hide/delete | ✅ | `instagram_manage_comments` |
| Hashtag search | ⚠️ | `ig_hashtag_search` → top/recent media; **max 30 hashtags / 7 days**; needs *Public Content Access* review |
| Auth | — | Meta app + OAuth; **App Review** (screencast per permission) for publish/comments/insights |

---

## YouTube (Data API v3 + Analytics/Reporting API)

| Capability | Status | Detail |
|---|---|---|
| Upload video / **Shorts** | ✅ | `videos.insert` (Shorts inferred from aspect/length, no separate endpoint); scope `youtube.upload` |
| **Quota cost** | ✅ | **~100 units** per upload **since 2025-12-04** (was ~1600) — verify on Quota Calculator |
| **Daily quota** | ✅ | **10,000 units/day** default → **~100 uploads/day** (was ~6). All requests consume quota |
| Comments read/post | ✅ | `commentThreads.insert` / `comments.insert` (write ~50 units); scope `youtube.force-ssl` |
| Analytics | ✅ | **YouTube Analytics API** (queries) + **Reporting API** (bulk CSV) |
| Trend pulls | ✅ | `videos.list?chart=mostPopular` = **1 unit**; `search.list` = 100 |
| Auth | — | Google Cloud + OAuth verification; production needs API services audit |

---

## TikTok (Content Posting API + Display API)

| Capability | Status | Detail |
|---|---|---|
| Publish video / photo | ✅ | Content Posting API: **Direct Post** (publishes) or **Upload** (to inbox draft); scopes `video.publish` / `video.upload` |
| **Public posting (native path)** | ⚠️ | **Unaudited → `SELF_ONLY` only**, **≤5 posting users / 24h**. Pass **audit** for public |
| **Public posting (via Blotato)** | ✅ | No audit needed — Blotato's app is already audited; set `privacyLevel: PUBLIC_TO_EVERYONE` |
| Rate limits | ⚠️ | ~6 req/min (publish/status), ~20 req/min (creator-info); ~15 posts/creator/day (approx, unpublished) |
| Analytics | ✗ for us | Display API = read-only public metadata; real analytics only via researcher-gated Research API / Business APIs |
| **Post comments** | ✗ | No comment-posting API; comment *reading* only via Research API (approved researchers) |
| Auth | — | TikTok app + Login Kit (OAuth); product approval + **client audit** for public posting; domain verification for PULL_FROM_URL |

---

## Trend / research sources

| Source | Access | ToS |
|---|---|---|
| YouTube Data API (`mostPopular` 1u / `search` 100u) | ✅ Official | ✅ within quota |
| Instagram Hashtag Search (30/7d, gated) | ⚠️ Official, gated | ✅ within limits |
| Google Trends (`pytrends`) | ⚠️ Unofficial | grey |
| TikTok Creative Center | ✗ No API (web only) | scraping **banned** |
| TikTok Research/Commercial API | ✗ Researchers only | n/a for commercial |
| Apify / Ensemble / RapidAPI | ⚠️ 3rd-party paid | **ToS-sensitive**; "compliant" labels unverified |

---

## Claude Code orchestration

| Capability | Status | Detail |
|---|---|---|
| Connect to external tools | ✅ | **MCP** via `.mcp.json` (`claude mcp add --transport http/stdio …`) + Messages API tool use |
| Headless / scriptable | ✅ | `claude -p` (`--output-format json`, `--json-schema`, `--permission-mode`, `--bare` for CI) |
| Build custom agents | ✅ | **Claude Agent SDK** (Python `claude-agent-sdk`, TS `@anthropic-ai/claude-agent-sdk`) |
| Scheduled / autonomous | ✅ | cron + `-p`; GitHub Actions `anthropics/claude-code-action` (`on: schedule:`); **Claude Code on the web Routines** (scheduled/API/GitHub triggers) |
| Hooks / skills | ✅ | Hooks before/after events; skills = `/name` (interactive only — in `-p`, pass task as prompt) |
| Native image/video gen | ✗ | Must call an external model (Higgsfield/Segmind/etc.) |
| ⚠️ Billing | — | From **2026-06-15**, Agent SDK / `claude -p` on subscription draws a separate credit pool — budget an API key for volume |
