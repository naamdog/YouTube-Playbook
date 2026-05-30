# Stage 8 — engage (comments)

Read comments → Claude drafts on-brand replies → post on **Instagram & YouTube**. **TikTok has no
public comment-posting API**, so TikTok replies are queued for a human.

> ⚠️ Gate everything behind `REQUIRE_HUMAN_APPROVAL` and `DAILY_REPLY_CAP`. Auto-comment spam is the
> fastest way to get an account restricted.

## Instagram — read + reply (`instagram_manage_comments`)
```http
# list comments on a media
GET  https://graph.facebook.com/v21.0/{ig_media_id}/comments?access_token={IG_TOKEN}
# reply to a comment
POST https://graph.facebook.com/v21.0/{comment_id}/replies?message={text}&access_token={IG_TOKEN}
# (also: hide=true to moderate; DELETE to remove)
```

## YouTube — read + reply (Data API)
```http
# list top-level comments
GET  https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}
# reply to a thread
POST https://www.googleapis.com/youtube/v3/comments?part=snippet
     body: {"snippet": {"parentId": "{comment_thread_id}", "textOriginal": "{reply}"}}
# OAuth scope: youtube.force-ssl
```

## TikTok — read only
```text
No official API to POST comments. Read where permitted; route replies to a human queue.
```

## Drafting loop
```python
caps = int(os.environ.get("DAILY_REPLY_CAP", 30)); sent = 0
for row in store.where(status="posted"):
    for c in fetch_new_comments(row):                 # IG/YT/TikTok
        reply = claude_draft_reply(brand_voice, row.idea, c.text)   # Claude writes the reply
        if needs_human(reply) or os.environ.get("REQUIRE_HUMAN_APPROVAL") == "true":
            queue_for_review(row, c, reply); continue
        if sent >= caps: break
        if   c.platform == "instagram": ig_reply(c.id, reply); sent += 1
        elif c.platform == "youtube":   yt_reply(c.id, reply); sent += 1
        else:                           queue_for_review(row, c, reply)   # tiktok → manual
```
</content>
