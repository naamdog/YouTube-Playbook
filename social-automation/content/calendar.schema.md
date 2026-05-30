# Content Calendar / Results Store — schema

The single source of truth. Every pipeline stage reads and writes here. Implement as a Google Sheet,
Airtable, SQLite, or Postgres table — the columns are what matter. `status` drives the state machine.

## State machine (`status`)

```
planned → media_ready → stored → scheduled → posted → measured
                                                 └→ (engage runs against posted rows)
```

## Columns

| Column | Stage | Type | Notes |
|---|---|---|---|
| `id` | 1 | string | unique row id |
| `created_at` | 1 | datetime | |
| `status` | all | enum | planned / media_ready / stored / scheduled / posted / measured |
| `platforms` | 1 | list | e.g. `instagram;youtube;tiktok` |
| `pillar` | 1 | string | content pillar (destination / teacher-story / how-to / promo) |
| `idea` | 1 | string | one-line concept |
| `hook` | 1 | string | first 1–2s line |
| `script` | 1 | text | 15–45s script / shot list |
| `caption` | 1 | text | platform-tuned caption |
| `hashtags` | 1 | list | |
| `media_prompt` | 1 | text | prompt for Higgsfield |
| `media_kind` | 1 | enum | image / video |
| `trend_refs` | 2 | list | trend-digest items that informed this |
| `media_url` | 3 | url | raw Higgsfield output |
| `gen_model` | 3 | string | higgsfield-soul / fal / etc. |
| `gen_cost` | 3 | number | credits/$ |
| `stored_url` | 4 | url | durable public/signed URL (Blotato pulls this) |
| `scheduled_time` | 5 | datetime | per-platform if needed |
| `approved_by` | 5/6 | string | human gate (REQUIRE_HUMAN_APPROVAL) |
| `post_id_instagram` | 6 | string | permalink / media id |
| `post_id_youtube` | 6 | string | video id |
| `post_id_tiktok` | 6 | string | publish id (SELF_ONLY until audited) |
| `disclosure_ai` | 6 | bool | AI-content disclosure flag set |
| `metrics_24h` | 7 | json | views/reach/engagement/retention |
| `metrics_7d` | 7 | json | |
| `learnings` | 7 | text | Claude's analysis → feeds Stage 1 |
| `replies_posted` | 8 | int | IG/YT |
| `replies_queued` | 8 | int | TikTok (manual) |
| `error` | any | text | last failure, for retry/debug |
</content>
