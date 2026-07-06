# creator-vetting

A Claude Skill that turns a YouTube channel URL into a scored, risk-flagged CRM row and a review-ready outreach draft — the judgment layer of a creator-partnerships pipeline.

Built as a working artifact for the Blotato Partnerships Lead application. It slots into an existing stack: sourcing skills feed it candidates, humans take its output into negotiation.

```
sourcing skill ──▶ creator-vetting ──▶ human review ──▶ outreach ──▶ deal
                        │
                        ├── scripts/fetch_channel_stats.py   (YouTube Data API v3)
                        ├── rubric.md                        (funnel model + weights)
                        ├── references/airtable-mapping.md   (writes via Airtable MCP)
                        ├── references/outreach-voice.md     (house voice + banned phrases)
                        └── references/qa-checklist.md       (quality gate before "ready")
```

## What a run produces

1. **Verified stats** — subscribers, trimmed 90-day average views (Shorts/livestreams excluded, viral outliers reported separately), upload cadence, and a sponsor scan of recent descriptions with detected brand names.
2. **A scored Airtable row** — Expected MRR from a funnel model (views × CTR class × trial rates × ARPU), CPM-method rate estimate, evidence-based risk flags, and full data provenance. Written to the live pipeline base via MCP.
3. **A first-touch outreach draft** — under 120 words, personalized to named recent content, rate-anchored to the public math — saved to the record for human review. Never sent.

## Design choices

**Each skill does one thing well.** Vetting is deliberately separate from sourcing, outreach, and reporting. The seams between skills are where humans review, and small skills stay debuggable: when a score looks wrong, there is exactly one rubric file to check.

**A QA gate runs before anything is marked ready.** `qa-checklist.md` is the hook: banned-phrase scan, missing-personalization test ("could this first line be pasted to a different creator unchanged?"), rate-anchor sanity check against the CPM band, and a data-provenance audit — every number must trace to a fetch or a hand count. Any failure blocks the "ready" state.

**Human-in-the-loop by design.** The skill's hard stop is structural, not polite: it writes rows at `Sourced`, leaves `Last Touch` empty, and saves outreach as a draft inside the record. It cannot advance a relationship, because long-term creator relationships are the human component of this job — the machine's role is to make the human's judgment faster and better-armed, not to replace it.

**Estimates are labeled, always.** Rate estimates carry `est., CPM method`; every stat carries an as-of date. A pipeline is only as trustworthy as its worst-labeled number.

## A manual task I audited into this skill

I vetted the first 25 channels for this pipeline entirely by hand: open the channel, count views on the last 15 uploads, throw out the viral outlier, average, skim eight descriptions for sponsor reads, log everything with sources. It took roughly ten minutes per channel, and by channel six I could feel which 70% of it was mechanical. So I audited the workflow, split it — stats fetching, outlier trimming, and sponsor scanning became `fetch_channel_stats.py`; the scoring math became `rubric.md`; my own review standards became the QA checklist — and kept the 30% that should stay human: reading comment intent, judging audience fit, and deciding what the first email should say. The hand-built pass wasn't wasted — it's the ground truth this skill is calibrated against.

## Setup

1. Free YouTube Data API v3 key → `export YT_API_KEY=...`
2. Airtable MCP server connected, with access to the pipeline base (IDs in `references/airtable-mapping.md` — update for your own base)
3. Install the skill folder, then: *"Vet https://www.youtube.com/@channelname for sponsorship"*

## Honest limitations

Sponsor detection is a description scan — creators who only do verbal reads without description credits are undercounted, so top candidates get a 90-second human spot-check. View-trend classification needs a graph a human reads (Social Blade), not just two data points. Engagement quality is scored by reading comments, deliberately: it is the single best fraud-and-fit signal, and the one this pipeline refuses to fake with a proxy metric.

## Roadmap

Companion skills, same philosophy, one job each: `deal-tracker` (deals → deliverables → actuals), `weekly-report` (dashboard rollup → async summary, replacing status meetings), `renewal-nudge` (relationship cadence from Last Touch).
