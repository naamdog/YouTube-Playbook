# 07 — Sources

Verified references behind the claims in this playbook (research conducted 2026-05). Where a page
blocked automated fetch (Meta/Google/TikTok docs returned 403), facts were drawn from search-indexed
excerpts of those official pages plus corroborating secondary sources; the most safety-critical or
volatile numbers are flagged **⚠️ verify live** in the docs.

## Blotato
- API start / auth / base URL — https://help.blotato.com/api/start
- API keys — https://help.blotato.com/settings/api-keys
- Publish post reference (targets, scheduling, per-platform options) — https://help.blotato.com/api/api-reference/publish-post
- Upload media — https://help.blotato.com/api/api-reference/upload-media-v2-media
- Schedules — https://help.blotato.com/api/schedules
- Pricing — https://www.blotato.com/pricing
- MCP setup / tools — https://help.blotato.com/api/mcp · https://help.blotato.com/api/mcp/setup · https://help.blotato.com/api/mcp/tools
- Official n8n node — https://github.com/Blotato-Inc/n8n-nodes-blotato · https://www.npmjs.com/package/@blotato/n8n-nodes-blotato

## Higgsfield
- Soul (image) — https://higgsfield.ai/soul-intro · Soul ID — https://higgsfield.ai/blog/SOUL-ID-Superior-Level-of-AI-Character-Consistency
- Camera controls / video (DoP) — https://higgsfield.ai/camera-controls · https://higgsfield.ai/ai-video
- Lipsync (Speak) — https://higgsfield.ai/lipsync-studio
- Cloud dashboard / API keys — https://cloud.higgsfield.ai · https://cloud.higgsfield.ai/api-keys
- Official SDKs — https://github.com/higgsfield-ai/higgsfield-client (Python) · https://github.com/higgsfield-ai/higgsfield-js (Node) · https://github.com/higgsfield-ai/cli
- MCP / CLI / Skills — https://higgsfield.ai/mcp · https://higgsfield.ai/cli · https://higgsfield.ai/skills
- Pricing — https://higgsfield.ai/pricing
- Per-call resellers — https://www.segmind.com/models/higgsfield-text2image-soul/api · https://wavespeed.ai/docs/docs-api/higgsfield/higgsfield-dop-image-to-video

## Instagram (Meta)
- Content publishing — https://developers.facebook.com/docs/instagram-platform/content-publishing/
- Publishing limit endpoint — https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit/
- Insights — https://developers.facebook.com/docs/instagram-platform/insights/
- Comments — https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-comment/
- Hashtag search — https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-hashtag-search/
- Stories launch (2023) — https://developers.facebook.com/blog/post/2023/05/16/

## YouTube (Google)
- Quota costs — https://developers.google.com/youtube/v3/determine_quota_cost
- **Revision history (videos.insert ~1600→~100 on 2025-12-04)** — https://developers.google.com/youtube/v3/revision_history
- Getting started / 10k quota — https://developers.google.com/youtube/v3/getting-started
- videos.insert — https://developers.google.com/youtube/v3/docs/videos/insert
- videos.list (mostPopular = 1 unit) — https://developers.google.com/youtube/v3/docs/videos/list
- comments — https://developers.google.com/youtube/v3/docs/commentThreads/insert · /comments/insert
- Analytics / Reporting — https://developers.google.com/youtube/analytics · https://developers.google.com/youtube/reporting

## TikTok
- Content Posting API — https://developers.tiktok.com/doc/content-posting-api-get-started · /doc/content-posting-api-reference-direct-post
- Content sharing guidelines (unaudited SELF_ONLY / 5-user cap) — https://developers.tiktok.com/doc/content-sharing-guidelines
- Display API (read-only) — https://developers.tiktok.com/doc/display-api-overview
- Scopes — https://developers.tiktok.com/doc/scopes-overview
- Rate limits — https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit
- Research API (comments read, researcher-only) — https://developers.tiktok.com/products/research-api/ · /products/commercial-content-api

## Trend research
- pytrends — https://github.com/GeneralMills/pytrends
- Apify actors — https://apify.com/clockworks/tiktok-scraper · https://apify.com/apify/instagram-hashtag-scraper · https://apify.com/streamers/youtube-scraper
- Ensemble Data — https://ensembledata.com/

## Claude Code / Agent SDK (Anthropic)
- MCP — https://code.claude.com/docs/en/mcp
- Headless — https://code.claude.com/docs/en/headless
- Agent SDK — https://platform.claude.com/docs/en/agent-sdk/overview · https://github.com/anthropics/claude-agent-sdk-typescript
- GitHub Actions — https://code.claude.com/docs/en/github-actions · https://github.com/anthropics/claude-code-action
- Claude Code on the web / Routines — https://code.claude.com/docs/en/claude-code-on-the-web · https://code.claude.com/docs/en/routines
- Hooks / Skills — https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/skills
- Tool use (Messages API) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- Vision (no native image generation) — https://platform.claude.com/docs/en/build-with-claude/vision
- Agent SDK billing change (2026-06-15) — https://support.claude.com/en/articles/15036540

> Note: `docs.claude.com` / `docs.anthropic.com` now 301-redirect to **code.claude.com** (Claude Code)
> and **platform.claude.com** (API) — both first-party Anthropic.
</content>
