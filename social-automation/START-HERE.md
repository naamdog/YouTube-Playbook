# 👋 Start Here — The Simple Version

This explains the whole social-media robot in plain words. No tech-speak. If you only read one page,
read this one. (The other files in `docs/` are the detailed, techy versions.)

---

## What we're building, in one sentence

A helper that **comes up with video ideas, makes the videos, posts them to Instagram, YouTube, and
TikTok, and then checks how they did** — mostly on its own, with you approving the important bits.

## Who does what (your team of helpers)

- 🧠 **Claude (the brain)** — thinks up the ideas, writes the captions and hashtags, and writes
  replies to comments. Smart and basically free of hassle.
- 🎨 **Higgsfield (the artist)** — Claude can't draw or film anything itself, so it asks Higgsfield to
  make the actual pictures and videos.
- 📮 **Blotato (the mailman)** — takes the finished video and posts it to Instagram, YouTube, and
  TikTok for you. Can also hold a post and send it later at the perfect time.
- 📊 **The report card** — after posting, Claude looks up the views and likes (on Instagram and
  YouTube) and learns what worked, so next week's ideas are better.

---

## Your weekly routine (the factory line)

Press go, and this happens in order:

1. 🔎 **Look around** — Claude checks what's trending for teaching-abroad content.
2. 🧠 **Make a plan** — Claude writes the week's ideas into a simple spreadsheet (idea, hook, caption,
   hashtags, and a description of the picture/video to make).
3. 🎨 **Make the videos** — Higgsfield creates each picture/video.
4. 💾 **Keep them** — the finished videos are saved (Blotato can hold them).
5. 👀 **You approve** — you look at the spreadsheet and thumbs-up the ones you like. *(Safety step.)*
6. 📮 **Post them** — Blotato sends the approved ones out, public, at the best time.
7. 📊 **Check the score** — a day or two later, Claude pulls the view/like numbers and notes what
   worked.
8. 💬 **Reply** — Claude drafts replies to comments; you approve; it posts them on Instagram and
   YouTube. (TikTok replies you do by hand — see "the catches" below.)

Then next week, step 2 uses what step 7 learned. It gets smarter over time. 🔁

---

## What you actually need (the shopping list)

Most of this is **signing up and pasting in keys**, not real coding.

| # | What | Just sign up, or build? |
|---|---|---|
| 1 | **Blotato** account (paid) + connect your IG / YT / TikTok | ✅ Sign up + click connect |
| 2 | **Higgsfield** account + log in (already installed here) | ✅ Sign up + log in |
| 3 | A **spreadsheet** (Google Sheet) to hold the plan | ✅ Make one |
| 4 | **Claude Code** with the keys plugged in | ⚙️ Light setup (mostly done) |
| 5 | The 5 ready-made commands: `/plan` `/trends` `/publish` `/report` `/engage` | ⚙️ Drafted, need testing |
| 6 | *(Optional)* **Apify** account for TikTok trends | ✅ Sign up if you want it |
| 7 | *(Optional, later)* Instagram/YouTube developer keys — only for reading comments & view counts | ⚙️ Some setup, can wait |

---

## The big good news: Blotato saves you the worst headache

The scary part of posting to TikTok/Instagram/YouTube is normally **"getting your app approved"** —
a slow, annoying review where TikTok even hides your posts until they inspect you.

**You skip all of that by using Blotato.** Blotato already got approved by every platform, and you're
borrowing their approval. So your posts go out **public, right away** — no waiting, no audit, no
review on your side. That's the whole reason to pay for a tool like Blotato.

---

## The catches (things even Blotato can't fix)

These are TikTok's own rules, and nobody can change them:

- 🚫 **TikTok won't let robots write comments.** So Claude can reply to comments on Instagram and
  YouTube, but TikTok replies you have to type yourself.
- 🚫 **TikTok won't share its view/like numbers** with outside tools. So your "report card" works
  great for Instagram and YouTube, but TikTok numbers you'd check by hand.
- 🔎 **TikTok trends** aren't handed out nicely either — getting them means using a scraper like
  **Apify** (see next).

---

## About Apify (the trend-peeker)

**Apify** is a tool that **scrapes** — it goes and *copies* info off websites, like what's trending or
what your competitors posted. It's the main way to get TikTok trend info, because TikTok won't give
it out the polite way.

⚠️ **Honest warning:** scraping is against these apps' rules. It usually works and lots of people do
it, but there's a small risk they **block you** or (rarely) send a legal complaint. Think of it as a
shortcut through the neighbor's yard. Use it carefully. The "allowed" door (YouTube) gives trends out
freely — start there.

---

## The safe way to roll this out

Don't flip everything on at once. Build trust in stages:

- **Week 1:** Sign up for Blotato + Higgsfield. Let Claude make plans and pictures into the
  spreadsheet. **No posting yet** — zero risk, just check the content is good.
- **Week 2:** Turn on posting, but **you approve every post by hand** first. Start with just
  Instagram + YouTube.
- **Week 3:** Add TikTok. Add the comment-reading and report-card pieces. Let it run more on its own
  once you trust it.

Always keep two safety switches on (they're built in):
- ✋ **"Ask me first"** — nothing gets posted or commented without your OK.
- 🛑 **A kill switch** — one setting that stops everything instantly.

---

## Where to go next

- Want the technical detail on any piece? → [`docs/`](docs/) (start with
  [`01-feasibility-verdict.md`](docs/01-feasibility-verdict.md)).
- Want the exact step-by-step build order? → [`docs/06-build-plan.md`](docs/06-build-plan.md).
- Want to know what's allowed vs risky? → [`docs/05-risks-compliance.md`](docs/05-risks-compliance.md).
</content>
