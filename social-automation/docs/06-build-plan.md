# 06 — Phased Build Plan (MVP → full autonomy)

A pragmatic order to build this without getting a TEFL Heaven account banned on day one.

## Phase 0 — Foundations (½–1 day)
- [ ] Pick the **state store**: start with a Google Sheet or SQLite (`content/calendar.*`).
- [ ] Copy `.env.example` → `.env`; fill keys you have. Set up a secrets store.
- [ ] **Build vs buy** for posting: start with **Blotato** (fastest); keep native APIs for Phase 4.
      Blotato's API is included on every paid plan (Starter ~$29/mo) — no separate add-on.
- [ ] Wire the official MCP servers into Claude Code (`config/mcp.example.json`): Blotato hosted MCP
      (`mcp.blotato.com/mcp`) + Higgsfield MCP (`higgsfield.ai/mcp`).

## Phase 1 — Content brain only (1 day) — *zero account risk*
- [ ] Implement `/trends` (YouTube Data API first).
- [ ] Implement `/plan` → writes rows to the store.
- [ ] **No posting yet.** Validate Claude produces good TEFL calendars from trend data.

## Phase 2 — Generation + storage (1–2 days) — *zero account risk*
- [ ] Confirm Higgsfield Cloud API endpoints/keys from your dashboard; fill the adapter.
- [ ] Implement `/generate` (Higgsfield → poll → URL) + storage upload.
- [ ] Review media quality; tune prompts. Still no posting.

## Phase 3 — Posting with a human gate (1–2 days) — *low risk*
- [ ] Implement `/publish` via Blotato, **draft/approval required** (trust-ladder Phase A).
- [ ] Start with **one platform** (IG or YouTube). Enforce rate limits client-side.
- [ ] TikTok: complete the **app audit** before attempting public posts.
- [ ] Set AI-content disclosure flags.

## Phase 4 — Measurement loop (1–2 days)
- [ ] Implement `/report` against IG Insights + YouTube Analytics (+ TikTok where available).
- [ ] Confirm learnings flow back into `/plan`. The loop now closes.

## Phase 5 — Engagement (1 day) — *handle with care*
- [ ] Implement `/engage`: read comments, Claude drafts replies, **hold for approval**.
- [ ] Enable auto-reply only on IG/YT, template-bounded, daily-capped (trust-ladder Phase C).
- [ ] TikTok comments stay manual.

## Phase 6 — Scheduling & autonomy
- [ ] Move trusted stages to **headless cron / GitHub Actions** (`claude -p`).
- [ ] Keep `publish`/`engage` human-gated longer than the rest.
- [ ] Add the **kill switch** + **audit log** before any unattended posting.

## Build-vs-buy quick guidance

| | Blotato (buy) | Native APIs (build) |
|---|---|---|
| Time to first post | hours | days–weeks (OAuth + App Review/audit per platform) |
| Per-platform control | good | total |
| Cost | subscription + API access | dev time + free-tier quotas |
| Analytics & comments | not covered → still need native | native covers it |
| Recommendation | **start here** | add later for analytics/comments + control |

> Realistic effort to a supervised MVP across IG + YouTube: **~1 week**. Add TikTok public posting
> after the audit. Full closed-loop autonomy: a few weeks, mostly platform approvals — not Claude.
