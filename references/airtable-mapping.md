# Airtable Mapping — Blotato Partnership Pipeline

Where the skill writes its output. Use the Airtable MCP connection.

- **Base:** Blotato Partnership Pipeline (`apprZ0T9txietXNkD`)
- **Table:** Creators (`tblEE1J5UJLGFFxmV`)

## Field map (skill output → Airtable field)

| Skill output | Field name | Type | Rules |
|---|---|---|---|
| channel | Channel | text (primary) | Channel title as YouTube shows it |
| url | YouTube URL | text/url | Canonical channel URL |
| — | Cluster | single select | `A - Priority` / `B - Evaluate` / `C - Strategic reject`, from the verdict |
| audience judgment | Audience Type | single select | `Solopreneur` / `SMB` / `Agency` / `Developer` / `Spectator` |
| CTR class | Integration Style | single select | `Tutorial-native` / `Standard read` — must agree with Assumed CTR |
| verdict rationale + provenance | Qualitative Notes | long text | Include `DRAFT OUTREACH:` section after QA passes |
| subscribers | Subs | number | From API, as-of date noted |
| avg_views_trimmed | 90d Avg Views | number | Trimmed average only; note outliers excluded |
| trend judgment | View Trend | single select | `Rising` / `Flat` / `Declining` — from views graph, not subs |
| comment-read score | Engagement Quality | rating 1–5 | Human-confirmed; tracker-derived scores get a note |
| sponsor scan | Sponsor Reads/Month | number | Counted, not guessed; brands into Qualitative Notes |
| CPM estimate | Est Rate USD | currency | Midpoint $37.50 CPM; label `est., CPM method` in notes |
| CTR class value | Assumed CTR | number | 0.01 or 0.005 only |
| evidence-based flags | Risk Flags | multi select | Blank = vetted clean; never fill without evidence |
| — | Status | single select | Always `Sourced` on creation; the skill never advances status |
| — | Last Touch | date | Always empty on creation — no contact has occurred |
| next step | Next Action | text | e.g. `Human review of outreach draft` |

Formula fields (Expected MRR, Payback Months, ROI Score) are computed by Airtable — never write them. Cross-check: the skill's own rubric math should match the formula output after the write; a mismatch means a data-entry error.