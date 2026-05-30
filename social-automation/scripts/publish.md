# Stage 6 — publish (Blotato primary, native APIs alternative)

## Blotato path (recommended start)

Two steps: host the media, then create the post.

> ⚠️ Confirm the base URL, header name, and exact request schema against Blotato's current docs and
> a community MCP server before relying on the field names below.

```python
import os, requests
BASE = os.environ["BLOTATO_API_BASE"]                 # ⚠️ confirm
H = {"blotato-api-key": os.environ["BLOTATO_API_KEY"], "Content-Type": "application/json"}  # ⚠️ confirm header

def blotato_upload(media_url: str) -> str:
    r = requests.post(f"{BASE}/media", headers=H, json={"url": media_url}, timeout=120)
    r.raise_for_status()
    return r.json()["url"]                             # Blotato-hosted URL

def blotato_post(account_id, platform, hosted_url, text, scheduled_time=None, **opts):
    payload = {
        "post": {
            "accountId": account_id,
            "target": {"targetType": platform, **opts},   # per-platform options
            "content": {"text": text, "mediaUrls": [hosted_url], "platform": platform},
        }
    }
    if scheduled_time:
        payload["scheduledTime"] = scheduled_time          # ISO-8601 → Blotato schedules it
    r = requests.post(f"{BASE}/posts", headers=H, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()
```

Per-platform `target`/option hints (confirm against Blotato docs):
- **instagram**: video → Reel.
- **tiktok**: `privacyLevel`, `disableComments`, `disableDuet`, `disableStitch`, content disclosure.
- **youtube**: `title`, `privacyStatus` (public/unlisted/private), `notifySubscribers`.

Glue (with safety gates):

```python
if os.environ.get("KILL_SWITCH") == "true":
    raise SystemExit("kill switch on")

for row in store.where(status="scheduled"):
    if os.environ.get("REQUIRE_HUMAN_APPROVAL") == "true" and not row.approved_by:
        continue                                  # skip un-approved rows
    hosted = blotato_upload(row.stored_url)
    for platform in row.platforms:
        acct = ACCOUNT_IDS[platform]
        res = blotato_post(acct, platform, hosted, f"{row.caption}\n{' '.join(row.hashtags)}",
                           scheduled_time=row.scheduled_time)
        store.set(row.id, f"post_id_{platform}", res.get("id"))
    store.update(row.id, status="posted")
```

## Native API path (more control; needed anyway for analytics + comments)

- **Instagram** (Graph API): `POST /{ig-user-id}/media` (create container) → `POST /{ig-user-id}/media_publish`.
  Business/Creator account, `instagram_content_publish`. **Cap client-side < 25/24h.**
- **YouTube**: `videos.insert` (resumable upload). **~1600 quota units each; ~6/day on default 10k.**
- **TikTok** (Content Posting API, Direct Post): init → upload → publish. **Unaudited app = SELF_ONLY
  only**; pass audit for public. Set AIGC disclosure.

> Enforce `DAILY_POST_CAP_*` from `.env` before every call — don't rely on receiving a 429.
</content>
