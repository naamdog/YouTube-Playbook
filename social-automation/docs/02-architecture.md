# 02 — Reference Architecture

Claude Code sits in the middle as the **orchestrator + content brain**. Everything else is a tool it
calls, over **MCP** (Model Context Protocol) or plain HTTP.

```
                         ┌────────────────────────────────────────────────┐
                         │                 CLAUDE CODE                      │
                         │   (orchestrator • planner • copywriter •         │
                         │    analyst • reply-drafter)                      │
                         │   runs via: interactive • `claude -p` headless • │
                         │   Agent SDK • cron / GitHub Actions • web        │
                         └───────┬───────────────┬───────────────┬─────────┘
                                 │ MCP / HTTP     │               │
            ┌────────────────────┘                │               └───────────────────┐
            ▼                                      ▼                                   ▼
   ┌──────────────────┐              ┌──────────────────────┐            ┌──────────────────────┐
   │ TREND / RESEARCH │              │   MEDIA GENERATION    │            │   POSTING LAYER       │
   │ • YouTube Data   │              │ • Higgsfield Cloud API│            │ • Blotato API (≈9)    │
   │ • TikTok CC*     │              │   (image + video)     │            │   host media → post   │
   │ • Apify actors*  │              │ • fal.ai / Kie.ai /   │            │   scheduledTime       │
   │ • Google Trends* │              │   PiAPI (fallback)    │            │  (or native APIs)     │
   └────────┬─────────┘              └───────────┬───────────┘            └──────────┬───────────┘
            │                                    │                                   │
            │                                    ▼                                   │
            │                        ┌──────────────────────┐                       │
            │                        │   MEDIA STORAGE       │                       │
            │                        │ • S3 / R2 / GCS       │◄──────────────────────┘
            │                        │ • public/signed URLs  │   (Blotato pulls media by URL)
            │                        │ • metadata            │
            │                        └──────────────────────┘
            │                                                                        │
            ▼                                                                        ▼
   ┌──────────────────────────────────────────────────────────────────────────────────────┐
   │                       STATE: Content Calendar + Results store                           │
   │   (Google Sheet / SQLite / Postgres / Airtable) — the single source of truth           │
   │   row lifecycle: idea → script → media → schedule → post_id → metrics → learnings       │
   └──────────────────────────────────────────────────────────────────────────────────────┘
            ▲                                                                        │
            │                                                                        ▼
   ┌──────────────────┐                                              ┌──────────────────────┐
   │  ANALYTICS PULL  │                                              │   COMMENTS           │
   │ • IG Insights    │                                              │ • IG  read+reply ✅   │
   │ • YouTube Analytics                                             │ • YT  read+reply ✅   │
   │ • TikTok (limited)                                              │ • TikTok read-only ⚠️ │
   └──────────────────┘                                              └──────────────────────┘
       * = unofficial / ToS-sensitive
```

## Why this shape

- **One source of truth (the calendar/results store).** Every stage reads and writes rows here.
  This is what lets the loop *close*: Stage-7 metrics feed Stage-1 planning.
- **Adapters, not hardwiring.** Higgsfield and the posting layer each sit behind a thin adapter, so
  you can swap Higgsfield→fal.ai or Blotato→native APIs without rewriting the pipeline.
- **Claude = stateless brain, the store = memory.** Each run, Claude reads context from the store,
  decides, calls tools, writes results back — exactly the pattern the Agent SDK + MCP support.

## How Claude Code connects to tools (3 layers)

1. **MCP servers** — cleanest. Configure in `.mcp.json` / settings
   ([config/mcp.example.json](../config/mcp.example.json)). Blotato has community MCP servers; you
   write a tiny one for Higgsfield (or use HTTP tool-use).
2. **HTTP / tool-use** — for anything without an MCP server, Claude calls the REST API directly
   (Higgsfield Cloud, YouTube Data API, IG Graph API, Apify).
3. **Shell scripts** — Claude Code runs `scripts/*` wrappers; handy for cron jobs.

## How it runs (autonomy options)

| Mode | Use for | How |
|---|---|---|
| **Interactive** | Building, supervising, approving | normal Claude Code session |
| **Headless** (`claude -p "..."`) | A single scheduled task | cron / systemd timer |
| **Agent SDK** (TS/Python) | A long-running custom agent | your own service |
| **GitHub Actions** (`schedule:`) | Free-ish daily/weekly runs | `.github/workflows/*.yml` |
| **Claude Code on the web** | Triggered / remote runs | code.claude.com |

Recommended: **human-in-the-loop interactive for publish/comment** at first; graduate low-risk
stages (generate, store, analytics-pull) to headless cron once trusted.
</content>
