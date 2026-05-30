---
description: Publish approved, scheduled posts via Blotato (Stage 6)
---

Publish content that is ready and approved. SAFETY FIRST.

1. Abort immediately if `KILL_SWITCH=true`.
2. Select rows with `status=scheduled`. If `REQUIRE_HUMAN_APPROVAL=true`, skip rows without
   `approved_by`. With `--due`, only rows whose `scheduled_time` is now/past.
3. Enforce client-side caps BEFORE posting: `DAILY_POST_CAP_INSTAGRAM` (<25/24h),
   `DAILY_POST_CAP_YOUTUBE` (<~6/day). Stop a platform when its cap is hit.
4. For each row+platform, follow `scripts/publish.md`:
   - host `stored_url` with Blotato → hosted URL
   - create the post with per-platform options (IG reels; TikTok privacy + AIGC disclosure;
     YouTube title/privacy/notify) and `scheduledTime` if scheduling rather than immediate.
5. Set AI-content disclosure flags. For TikTok, remember: unaudited app ⇒ SELF_ONLY only.
6. Write `post_id_*` per platform; set `status=posted`. Log every action to the audit log.
7. Report what was posted, what was skipped (and why), and remaining cap headroom.
</content>
