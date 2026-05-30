# 05 — Risks, Compliance & What Will Get You Banned

Automating social media is **technically** very doable. The risk is **policy and account safety**,
not code. Read this before wiring anything to a real TEFL Heaven account.

## The five hard platform limits (recap)

1. **TikTok audit gate** — until your TikTok app passes audit, every API post is `SELF_ONLY` (private).
2. **TikTok has no comment-posting API** — auto-commenting on TikTok isn't possible officially.
3. **YouTube upload quota** — ~6 uploads/day on the default 10k-unit quota; request an increase.
4. **Instagram ~25 posts / 24h** via the Content Publishing API, per account.
5. **Claude can't make media** — image/video must come from Higgsfield or another model.

## Account-ban / policy risks (the real danger)

| Risk | Why it bites | Mitigation |
|---|---|---|
| **Inauthentic / spammy automation** | All three platforms ban automated behavior that mimics a human at scale | Keep volume human-plausible; human-in-loop on publish/comment |
| **Auto-comment spam** | Fastest path to shadowban / ban | Draft-then-approve; rate-limit replies; never bulk-DM |
| **Fake engagement** | Buying/automating likes/follows/comments = ToS violation + legal risk | Don't. Out of scope. |
| **Scraping for trend/competitor data** | Apify/IG/TikTok scraping violates ToS; can trigger blocks & legal letters | Prefer official APIs; treat scraping as informed opt-in risk |
| **Disclosure rules** | AI-generated media must be labeled on some platforms (TikTok AIGC, Meta AI labels) | Set disclosure flags; label AI content |
| **Token / credential leakage** | One leaked long-lived token = account takeover | Secrets manager; never commit `.env`; rotate tokens |
| **Copyright / music** | Auto-adding trending sounds can infringe | Use licensed/commercial-safe audio |

## Compliance checklist before going live

- [ ] Each platform app created with **least-privilege scopes**; App Review/audit done where required.
- [ ] **Human approval** required for `publish` and `comment` actions (at least initially).
- [ ] **AI-content disclosure** flags set per platform.
- [ ] **Rate limits** enforced *client-side* below platform ceilings (don't rely on a 429).
- [ ] Secrets in a vault / `.env` (git-ignored), not in code or the calendar store.
- [ ] **Audit log** of every automated action (what posted/commented, when, which run).
- [ ] A **kill switch** (one flag that halts all posting/commenting).
- [ ] Legal review if you scrape, target many accounts, operate for clients, or in the EU (GDPR).

## What this playbook will NOT help you do

- Mass-create accounts, buy/automate fake engagement, run follow/unfollow bots.
- Evade platform detection or rate limits.
- Scrape at scale in violation of ToS.
- Impersonate people or generate deceptive deepfakes.

These violate platform policy and, in places, the law — out of scope by design.

## Recommended trust ladder

1. **Phase A:** everything generates into drafts; a human reviews and clicks publish.
2. **Phase B:** auto-publish *scheduled* posts a human approved in advance; comments still manual.
3. **Phase C:** auto-reply to comments from an approved template set on IG/YT only, with daily caps.
4. Never remove the kill switch or the audit log.
</content>
