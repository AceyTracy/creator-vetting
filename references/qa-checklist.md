# QA Checklist — runs before any output is marked ready

The skill must evaluate every item and fix failures before presenting results. This is the hook: nothing reaches a human marked "ready" without passing all checks. In Claude Code this file is wired as a Stop-hook checklist; in claude.ai it runs as the mandatory final step of the skill.

## Data integrity

- [ ] Every number in the Airtable row is fetched or hand-counted — zero guessed values
- [ ] Provenance (source + as-of date) recorded in notes for subs, avg views, and rate
- [ ] Avg views is the trimmed figure; outliers listed in notes if any were excluded
- [ ] Assumed CTR is exactly 0.01 or 0.005 and agrees with Integration Style
- [ ] Est Rate labeled `est., CPM method` — estimates never presented as quotes
- [ ] Skill's rubric math matches Airtable's formula output after the write
- [ ] Risk Flags each have a stated evidence line; no flag on vibes
- [ ] Status = Sourced, Last Touch empty — the row claims no contact that didn't happen

## Outreach draft

- [ ] Under 120 words; subject under 6 words
- [ ] Contains a specific, recent, named reference to the creator's content
- [ ] Fails the paste test: the first line could NOT be sent to a different creator unchanged
- [ ] Zero banned phrases (see outreach-voice.md)
- [ ] Rate anchor present and equal to the rubric math (sanity: anchor within $25–50 CPM band of avg views)
- [ ] Exactly one ask
- [ ] Draft saved to Qualitative Notes under `DRAFT OUTREACH:` — not sent, not queued, not scheduled anywhere

## Verdict

- [ ] Two-sentence verdict states the cluster and the single strongest number behind it
- [ ] If reject: the killing metric is named (payback, mismatch, fatigue count, trend)

Any unchecked box = output is not ready. Fix and re-run the list.