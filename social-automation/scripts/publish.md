# Stage 6 — publish (Blotato primary, native APIs alternative)

## Blotato path (recommended start)

Verified shapes. Base `https://backend.blotato.com/v2`, header `blotato-api-key`. You can pass a
public media URL directly (no upload), or host it on Blotato first. `scheduledTime` is a **top-level**
sibling of `post` — nesting it inside `post` makes it post immediately. `content.platform` **must
equal** `target.targetType`. Get `accountId` from `GET /v2/users/me/accounts`.

```python
import os, requests
BASE = "https://backend.blotato.com/v2"
H = {"blotato-api-key": os.environ["BLOTATO_API_KEY"], "Content-Type": "application/json"}

def blotato_host(media_url: str) -> str:
    """Optional: re-host an external URL on Blotato. You can also skip this and
    pass the original public URL straight into mediaUrls."""
    r = requests.post(f"{BASE}/media", headers=H, json={"url": media_url}, timeout=120)
    r.raise_for_status()
    return r.json()["url"]

def blotato_post(account_id, platform, media_url, text, scheduled_time=None, **target_opts):
    payload = {
        "post": {
            "accountId": account_id,
            "content": {"text": text, "mediaUrls": [media_url], "platform": platform},
            "target": {"targetType": platform, **target_opts},
        }
    }
    if scheduled_time:
        payload["scheduledTime"] = scheduled_time          # ISO-8601 + offset, top-level
    r = requests.post(f"{BASE}/posts", headers=H, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()
```

Verified per-platform `target` options:
- **tiktok**: `privacyLevel` (`SELF_ONLY` | `PUBLIC_TO_EVERYONE` | `MUTUAL_FOLLOW_FRIENDS` |
  `FOLLOWER_OF_CREATOR`), `disabledComments`, `disabledDuet`, `disabledStitch`, `isBrandedContent`,
  `isYourBrand`, `isAiGenerated`, `autoAddMusic`.
- **youtube**: `title`, `privacyStatus` (`private`|`public`|`unlisted`), `shouldNotifySubscribers`.
- **instagram**: video → Reel; multiple `mediaUrls` → carousel.

Glue (with safety gates):

```python
if os.environ.get("KILL_SWITCH") == "true":
    raise SystemExit("kill switch on")

for row in store.where(status="scheduled"):
    if os.environ.get("REQUIRE_HUMAN_APPROVAL") == "true" and not row.approved_by:
        continue
    media = row.stored_url or row.media_url                 # public URL is fine
    for platform in row.platforms:
        opts = {}
        if platform == "tiktok":
            opts = {"privacyLevel": "PUBLIC_TO_EVERYONE", "isAiGenerated": True}   # SELF_ONLY until audited!
        if platform == "youtube":
            opts = {"title": row.idea[:95], "privacyStatus": "public", "shouldNotifySubscribers": True}
        res = blotato_post(ACCOUNT_IDS[platform], platform, media,
                           f"{row.caption}\n{' '.join(row.hashtags)}",
                           scheduled_time=row.scheduled_time, **opts)
        store.set(row.id, f"post_id_{platform}", res.get("id"))
    store.update(row.id, status="posted")
```

## Native API path (more control; needed anyway for analytics + comments)

- **Instagram** (Graph API): `POST /{ig-user-id}/media` (container; `media_type=REELS/STORIES/CAROUSEL`)
  → `POST /{ig-user-id}/media_publish`. Professional account, `instagram_content_publish`.
  **Cap < ~50/24h** (rolling; check `content_publishing_limit`).
- **YouTube**: `videos.insert` (resumable). **~100 quota units each since 2025-12-04** → ~100/day on
  the default 10k quota (was ~6).
- **TikTok** (Content Posting API, Direct Post): query creator-info → init (PULL_FROM_URL / upload)
  → poll `/status/fetch/`. **Unaudited app = SELF_ONLY + ≤5 users/24h**; pass audit for public. Set
  `isAiGenerated`.

> Enforce `DAILY_POST_CAP_*` from `.env` before every call — don't rely on receiving a 429.
