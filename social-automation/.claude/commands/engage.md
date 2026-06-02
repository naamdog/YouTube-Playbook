---
description: Read comments and draft/post replies (Stage 8)
---

Engage with comments responsibly. Spam = bans, so default to drafting, not blasting.

1. Abort if `KILL_SWITCH=true`. Enforce `DAILY_REPLY_CAP`.
2. For each `status=posted` row, fetch new comments (IG, YouTube, TikTok) per `scripts/engage.md`.
3. For each comment, draft an on-brand, specific reply (match TEFL Heaven voice; never generic spam).
4. With `--review` OR if `REQUIRE_HUMAN_APPROVAL=true`: queue replies for human approval, post none.
5. Otherwise post replies ONLY on Instagram and YouTube (within the cap). TikTok replies always go
   to the human queue (no comment-posting API).
6. Flag anything sensitive (complaints, legal, refunds, PR risk) for a human instead of auto-replying.
7. Report: replies posted (per platform), replies queued, anything escalated.
