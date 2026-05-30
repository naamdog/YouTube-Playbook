# 04 — The End-to-End Pipeline Playbook (all 8 stages)

The runbook. Each stage = what triggers it, what it reads, what it does, what it writes back to the
**content calendar / results store** (the single source of truth). The store is what closes the loop
(Stage-7 metrics → Stage-1 plan).

> Reference implementations (key-gated pseudocode) for each stage live in [`scripts/`](../scripts/).

---

## Stage 1 — PLAN  (`/plan`)
- **Trigger:** weekly cron, or manual.
- **Reads:** TEFL Heaven brand brief, last week's metrics + learnings (Stage 7), trend digest (Stage 2).
- **Claude does:** generate N ideas → for each: platform mix (IG Reel / YT Short / TikTok), hook,
  15–45s script/shot-list, caption variants, hashtags, target post time, image/video prompt.
- **Writes:** new rows with `status=planned` (see [content/calendar.schema.md](../content/calendar.schema.md)).

## Stage 2 — RESEARCH TRENDS  (`/trends`)
- **Trigger:** before Stage 1 (or nightly).
- **Reads:** niche keywords (e.g. "teach English abroad", "TEFL Vietnam"), competitor handles.
- **Does:** pull YouTube `search`/`mostPopular`, TikTok Creative Center / Apify trend data, Google
  Trends → Claude clusters into "what's working now: formats, hooks, sounds, post times."
- **Writes:** a `trend_digest` artifact Stage 1 consumes. **⚠️ scraping = ToS risk; prefer APIs.**

## Stage 3 — GENERATE MEDIA  (`/generate`)
- **Trigger:** rows `status=planned` with a media prompt.
- **Does:** call **Higgsfield Cloud API** (image/video) via the adapter → submit → poll → output URL.
  Fallback to fal.ai/Kie.ai/PiAPI as needed.
- **Writes:** `media_url`, `media_type`, `gen_model`, `gen_cost`; `status=media_ready`.
- See [scripts/generate_media.md](../scripts/generate_media.md).

## Stage 4 — STORE MEDIA
- **Does:** download generated file → upload to **S3/R2/GCS** → record durable public/signed URL +
  metadata. (Or push straight into Blotato's media upload.)
- **Writes:** `stored_url`; `status=stored`.

## Stage 5 — SCHEDULE
- **Does:** decide post time per platform (Claude optimizes from past metrics); set Blotato
  `scheduledTime` or enqueue for your own scheduler.
- **Writes:** `scheduled_time`; `status=scheduled`.

## Stage 6 — POST  (`/publish`)
- **Trigger:** scheduled time reached (Blotato) OR your cron fires.
- **Does:** **Blotato** path → host media → create post with per-platform options (IG reels; TikTok
  privacy/disclosure; YouTube title/privacy/notify). **Native** path → IG Content Publishing,
  YouTube `videos.insert`, TikTok Content Posting (Direct Post).
- **Writes:** `post_id`/permalink per platform; `status=posted`. ⚠️ respect 25/day (IG), ~6/day (YT),
  TikTok audit. See [scripts/publish.md](../scripts/publish.md).

## Stage 7 — MEASURE  (`/report`)
- **Trigger:** ~24h and ~7d after posting.
- **Does:** pull **IG Insights**, **YouTube Analytics**, **TikTok analytics** → join to the row →
  Claude writes a performance summary + concrete learnings ("destination Reels beat talking-head by
  2.1× retention").
- **Writes:** metrics + `learnings`; `status=measured`. **Feeds Stage 1.**
- See [scripts/report.md](../scripts/report.md).

## Stage 8 — COMMENT  (`/engage`)
- **Trigger:** new comments on posted content (poll or webhook).
- **Does:** read comments → Claude drafts on-brand replies → **post on IG (`instagram_manage_comments`)
  and YouTube (`comments.insert`)**. **TikTok: queue for human** (no comment-posting API).
- **Writes:** `replies_posted`, `replies_queued`. ⚠️ gate behind approval + daily caps.
- See [scripts/engage.md](../scripts/engage.md).

---

## The loop, in one line

```
PLAN → TRENDS feed PLAN → GENERATE → STORE → SCHEDULE → POST → MEASURE → (learnings) → PLAN …
                                                              └── ENGAGE (comments) ──┘
```

## Minimal daily run (cron-friendly)

```bash
# nightly
claude -p "/trends"            # refresh trend digest
claude -p "/plan"              # top up the calendar
claude -p "/generate"          # make media for planned rows
claude -p "/publish --due"     # post anything scheduled for now (human-approved rows only)
claude -p "/report --due"      # pull metrics for posts at 24h/7d
claude -p "/engage --review"   # draft replies; hold for approval
```
</content>
