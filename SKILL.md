---
name: creator-vetting
description: Vets a YouTube channel for Blotato sponsorship fit. Input is a channel URL or handle. Pulls current stats, computes the weighted ROI score against the partnerships rubric, flags risks, writes a scored row to the Creators table in Airtable via MCP, and drafts a first-touch outreach email in the house voice — then stops for human review. Use this skill whenever evaluating any new creator, community, newsletter, or influencer as a potential partner, whenever someone asks "should we sponsor X", "vet this channel", "score this creator", or pastes a YouTube link in a partnerships context, even if they don't say the word "vet".
---

# creator-vetting

One job: turn a channel URL into a scored, risk-flagged Airtable row and a review-ready outreach draft. Sourcing happens upstream (sourcing skill). Sending happens downstream (a human). This skill is the judgment layer in between.

## Workflow

Follow these steps in order. Do not skip the QA checklist and never send outreach.

### 1. Fetch channel stats

Run the bundled script (requires `YT_API_KEY` env var — free YouTube Data API v3 key):

```bash
python scripts/fetch_channel_stats.py "<channel URL or @handle>"
```

It returns JSON: subscribers, last-15-regular-upload views (Shorts and livestreams excluded), a 90d average with outliers trimmed (anything >3x or <1/3 of the median is excluded and reported separately), an upload-cadence figure, and a sponsor scan of recent descriptions (count + detected brand names).

**Fallback (no API key):** collect the same numbers manually — channel page for subs, Videos tab sorted by Latest for the last 10–15 regular uploads, average them excluding outliers. Never proceed with guessed numbers; every stat must be fetched or hand-counted.

### 2. Score against the rubric

Read `rubric.md` and compute:

- **Expected MRR** — funnel model with the CTR class from the rubric (tutorial-native vs standard read).
- **Est Rate USD** — CPM method, labeled as an estimate.
- **ROI Score and Payback** — per the rubric formulas (these mirror the Airtable formula fields, so the numbers you compute should match what Airtable shows after the write; if they don't, something is wrong — stop and check).
- **Audience Type** — judged from content topics and comment intent, not subscriber count.

### 3. Flag risks

Apply flags only with evidence, per the criteria in `rubric.md` §Risk Flags: Declining trend (from view trajectory), Sponsor fatigue (4+ reads/month counted, or documented category saturation), Audience mismatch (viewer profile doesn't buy workflow SaaS), Brand risk (concrete controversy only), Competitor exclusivity (rival scheduler seen in recent reads). A channel with zero flags is a valid and meaningful result — do not invent flags to fill the field.

### 4. Write the Airtable row

Use the Airtable MCP connection. Read `references/airtable-mapping.md` for the base, table, and exact field names, then create one record in the Creators table with everything computed above. Put data provenance in the Data Notes field (source + as-of date for every number). Set Status to `Sourced`. Leave Last Touch empty — no contact has happened.

### 5. Draft first-touch outreach

Read `references/outreach-voice.md` and draft ONE short email (under 120 words) personalized to something specific and recent from the channel. Include the rate anchor from the rubric math. Save the draft into the record's Qualitative Notes under a `DRAFT OUTREACH:` heading.

### 6. QA gate, then stop

Run every item in `references/qa-checklist.md` against the draft and the row. Fix failures and re-run. When all checks pass, present the scored row summary and the outreach draft to the human with the verdict (`prioritize / evaluate / reject` and why, in two sentences).

**Hard stop: this skill never sends outreach, never updates Status beyond Sourced, and never contacts a creator.** Relationships are the human component. The output of this skill is a decision-ready package, not an action.
