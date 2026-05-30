# Stage 3 — generate_media (Higgsfield Cloud API)

Adapter that turns a `media_prompt` row into a generated image/video URL. Higgsfield sits behind one
function so it can be swapped for fal.ai/Kie.ai/PiAPI without touching the pipeline.

> ⚠️ **Confirm the exact base URL, endpoint paths, request schema, and credit costs** from your
> logged-in Higgsfield Cloud dashboard. The shape below is the standard async gen-media pattern
> (submit → poll → fetch); adjust field names to match the live docs.

```python
import os, time, requests

BASE = os.environ["HIGGSFIELD_API_BASE"]      # ⚠️ confirm
KEY  = os.environ["HIGGSFIELD_API_KEY"]
H    = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

def generate(prompt: str, kind: str) -> dict:
    """kind = 'image' | 'video'. Returns {url, model, cost}."""
    # 1) submit a generation job  (CONFIRM endpoint + body from dashboard)
    endpoint = "/image/generations" if kind == "image" else "/video/generations"
    payload = {
        "prompt": prompt,
        "aspect_ratio": "9:16",          # shorts/reels/tiktok vertical
        # image: "model": "soul"; video: motion/camera preset + "duration": 5, ...
    }
    r = requests.post(BASE + endpoint, headers=H, json=payload, timeout=60)
    r.raise_for_status()
    job_id = r.json()["id"]

    # 2) poll until complete
    for _ in range(120):                  # up to a few minutes
        s = requests.get(f"{BASE}/jobs/{job_id}", headers=H, timeout=30).json()
        if s["status"] in ("completed", "succeeded"):
            return {"url": s["output"][0]["url"], "model": "higgsfield", "cost": s.get("credits")}
        if s["status"] in ("failed", "error"):
            raise RuntimeError(f"Higgsfield job failed: {s}")
        time.sleep(3)
    raise TimeoutError("Higgsfield job timed out")

# --- fallback adapters (same signature) -----------------------------------
# def generate_fal(prompt, kind):  ... fal.ai/run/<model> ...
# def generate_kie(prompt, kind):  ... kie.ai ...
```

Pipeline glue:

```python
for row in store.where(status="planned", media_prompt__ne=None):
    try:
        out = generate(row.media_prompt, row.media_kind)
        store.update(row.id, media_url=out["url"], gen_model=out["model"],
                     gen_cost=out["cost"], status="media_ready")
    except Exception as e:
        store.update(row.id, error=str(e))
```

Then Stage 4 downloads `media_url`, uploads to S3/R2, sets `stored_url`, `status="stored"`.
</content>
