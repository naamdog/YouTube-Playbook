# 03 — Capability Matrix (facts, limits, auth)

What was established as of **2026-05**. Items flagged **⚠️ confirm** are real capabilities whose exact
value (endpoint path, schema, price) should be confirmed from the live dashboard/docs, because those
sources are behind login or change often. Native-platform and Claude-Code facts are well-established.

---

## Blotato (posting / scheduling layer)

| Item | Status | Detail |
|---|---|---|
| Public REST API | ✅ | API-key auth (key from the Blotato settings page) |
| Platforms | ✅ | ≈9: Instagram, TikTok, YouTube, Facebook, Threads, LinkedIn, X/Twitter, Pinterest, Bluesky |
| Flow | ✅ | Typically **two-step**: host/upload media → create post |
| Scheduling | ✅ | Future `scheduledTime` supported on create-post |
| Media | ✅ | Upload-by-URL → Blotato-hosted URL (needs a reachable source URL) |
| Per-platform options | ✅ | IG reels; TikTok privacy/comments/duet/stitch/disclosure; YouTube title/privacy/notify |
| Plan required | ⚠️ confirm | Paid plan with **API access** (verify current tier/cost) |
| Base URL / exact schema | ⚠️ confirm | Verify from Blotato docs + community MCP repos |
| Analytics back | ✗ | Not its focus → use native analytics APIs |
| Comments | ✗ | Not exposed → use native APIs |
| Integrations | ✅ | n8n + Make templates; community MCP server(s) for Claude Code |

---

## Higgsfield (image / video generation)

| Item | Status | Detail |
|---|---|---|
| Consumer app (`higgsfield.ai`) | ✅ | AI images ("Soul" model), image/text→video, camera & motion presets |
| Official Cloud API | ✅ | "Higgsfield Cloud" — programmatic generation via API key, credit-billed |
| Pattern | ✅ | Async: submit job → poll → output URL(s) |
| Exact base URL / endpoints / credit costs | ⚠️ confirm | From logged-in Higgsfield Cloud dashboard |
| Fallback APIs | ✅ | fal.ai, Kie.ai, PiAPI, Replicate host comparable image/video models |
| Claude native gen | ✗ | Anthropic API **cannot** generate images/video — external model mandatory |

---

## Instagram (Instagram Graph API / Instagram API with Instagram Login)

| Capability | Status | Detail |
|---|---|---|
| Publish image / carousel / **Reels** | ✅ | Content Publishing API; **Business/Creator** account + linked Page |
| Publish **Stories** | ✅ | Supported for Business accounts |
| **Rate limit** | ⚠️ | ~**25 API-published posts / 24h** per account |
| Insights / analytics | ✅ | Reach, impressions, engagement, saves, etc. |
| Comments read/reply/hide/delete | ✅ | `instagram_manage_comments` |
| Auth | — | Meta app + tokens; **App Review** for `instagram_content_publish`, `instagram_manage_comments` |

---

## YouTube (Data API v3 + Analytics API)

| Capability | Status | Detail |
|---|---|---|
| Upload video / **Shorts** | ✅ | `videos.insert` (resumable upload) |
| **Quota cost** | ⚠️ | ~**1600 units** per upload |
| **Daily quota** | ⚠️ | **10,000 units/day** default ≈ **~6 uploads/day** → request increase for volume |
| Comments read/post | ✅ | `commentThreads.insert`, `comments.insert` |
| Analytics | ✅ | **YouTube Analytics & Reporting API** |
| Auth | — | OAuth 2.0; scopes incl. `youtube.upload`, `youtube.force-ssl` |

---

## TikTok (Content Posting API + Display API)

| Capability | Status | Detail |
|---|---|---|
| Publish video / photo | ✅ | Content Posting API: **Direct Post** (publishes) or **Upload** (draft in inbox) |
| **Public posting** | ⚠️ | **Unaudited apps → `SELF_ONLY`/private only**; pass TikTok **audit** for public |
| Analytics | ⚠️ | Limited; richer metrics need Business account / restricted Research API |
| **Post comments** | ✗ | **No public API to post comments** |
| Auth | — | OAuth 2.0; scopes `video.publish`, `video.upload`; app review/audit |

---

## Trend / research sources

| Source | Access | ToS |
|---|---|---|
| YouTube Data API (`search`, `mostPopular`) | ✅ Official | ✅ within quota |
| Google Trends (`pytrends`) | ⚠️ Unofficial | grey |
| TikTok Creative Center | ⚠️ Web UI; programmatic = scrape/3rd-party | grey |
| Instagram Hashtag Search API | ⚠️ Restricted, rate-limited | ✅ within limits |
| Apify actors (TikTok/IG/YT scrapers) | ⚠️ 3rd-party paid | **ToS-sensitive** |
| Ensemble Data / RapidAPI | ⚠️ 3rd-party paid | unofficial |

---

## Claude Code orchestration

| Capability | Status | Detail |
|---|---|---|
| Connect to external tools | ✅ | **MCP servers** (`.mcp.json`/settings) + HTTP tool-use |
| Headless / scriptable | ✅ | `claude -p "..."` print mode for cron |
| Build custom agents | ✅ | **Claude Agent SDK** (TypeScript + Python) |
| Scheduled / autonomous | ✅ | cron + headless, GitHub Actions `schedule:`, Claude Code on the web |
| Hooks / slash commands / skills | ✅ | SessionStart hooks; custom commands for repeatable steps |
| Native image/video gen | ✗ | Must call an external model (Higgsfield/fal/etc.) |

> Verify the ⚠️-flagged Blotato/Higgsfield specifics against their live docs before building. The
> adapter pattern in [scripts/](../scripts/) keeps those changes localized.
</content>
