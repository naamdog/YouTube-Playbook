# Stage 3 — generate_media (Higgsfield Cloud API)

Adapter that turns a `media_prompt` row into a generated image/video URL. Higgsfield sits behind one
function so it can be swapped for Segmind/WaveSpeedAI without touching the pipeline.

> Verified facts: base `https://platform.higgsfield.ai`; auth `Authorization: Key KEY_ID:KEY_SECRET`
> (an ID+secret pair, **not** Bearer); official SDKs (`pip install higgsfield-client`,
> `npm i higgsfield-js`); async submit → poll `/requests/{id}/status` (or `webhook_url`) → output URL;
> failed jobs refund credits. Exact video length/resolution caps come from resellers — verify.

## Option A — official Python SDK (recommended)

```python
import os
from higgsfield_client import HiggsfieldClient   # pip install higgsfield-client

# Reads HF_KEY="id:secret" (or HF_API_KEY / HF_API_SECRET) from env
hf = HiggsfieldClient()

def generate(prompt: str, kind: str) -> dict:
    """kind = 'image' | 'video'. Returns {url, model, cost}."""
    if kind == "image":
        job = hf.subscribe("soul/text-to-image",
                           input={"prompt": prompt, "aspect_ratio": "9:16"},
                           with_polling=True)
        return {"url": job.images[0].url, "model": "higgsfield-soul", "cost": job.credits}
    else:
        job = hf.subscribe("/v1/image2video/dop",
                           input={"prompt": prompt, "quality": "dop-turbo",
                                  "duration": 5, "aspect_ratio": "9:16"},
                           with_polling=True)
        return {"url": job.video.url, "model": "higgsfield-dop", "cost": job.credits}
```

## Option B — raw REST (when you need control / no SDK)

```python
import os, time, requests
BASE = "https://platform.higgsfield.ai"
KEY  = f'Key {os.environ["HIGGSFIELD_API_KEY_ID"]}:{os.environ["HIGGSFIELD_API_KEY_SECRET"]}'
H    = {"Authorization": KEY, "Content-Type": "application/json"}

def generate(prompt, kind):
    endpoint = "/v1/text2image/soul" if kind == "image" else "/v1/image2video/dop"
    r = requests.post(BASE + endpoint, headers=H,
                      json={"prompt": prompt, "aspect_ratio": "9:16"}, timeout=60)
    r.raise_for_status()
    req_id = r.json()["id"]
    for _ in range(120):                                   # poll up to a few minutes
        s = requests.get(f"{BASE}/requests/{req_id}/status", headers=H, timeout=30).json()
        if s["status"] == "Completed":
            out = s.get("images", [{}])[0].get("url") or s.get("video", {}).get("url")
            return {"url": out, "model": f"higgsfield-{kind}", "cost": s.get("credits")}
        if s["status"] in ("Failed", "NSFW", "Cancelled"):
            raise RuntimeError(f"Higgsfield job {s['status']}: {s}")
        time.sleep(3)
    raise TimeoutError("Higgsfield job timed out")
```

## Fallback — Segmind / WaveSpeedAI (per-call billing for just Soul/DoP)

```python
# Segmind Soul text-to-image (~$0.12/image)
# POST https://api.segmind.com/v1/higgsfield-text2image-soul
#   header: x-api-key: ${SEGMIND_API_KEY}
#   body:   {"prompt": ..., "width_and_height": "1080x1920", "quality": "1080p", "style_id": ...}
# WaveSpeedAI DoP image-to-video: https://wavespeed.ai/docs/.../higgsfield-dop-image-to-video
```

## Pipeline glue

```python
for row in store.where(status="planned", media_prompt__ne=None):
    try:
        out = generate(row.media_prompt, row.media_kind)
        store.update(row.id, media_url=out["url"], gen_model=out["model"],
                     gen_cost=out["cost"], status="media_ready")
    except Exception as e:
        store.update(row.id, error=str(e))
```

Then Stage 4 either passes `media_url` straight to Blotato `mediaUrls`, or re-hosts it on S3/R2 and
sets `stored_url`, `status="stored"`.

> Model slugs above (e.g. `soul/text-to-image`, `/v1/image2video/dop`, `/v1/speak/higgsfield`) follow
> the SDK examples; confirm exact slugs/params against the installed SDK source, which is the most
> reliable spec (public REST docs are thin).
