# Partnerships Scoring Rubric

Single source of truth for how creators are scored. The Airtable formula fields implement the same math; if a skill run and the base disagree, this file wins and the discrepancy gets investigated.

## Funnel model (Expected MRR per integration)

```
Expected MRR = 90d Avg Views × CTR × 0.15 × 0.40 × $45
                                │      │      │      └─ blended ARPU (plans $29–$229, most convert low-tier)
                                │      │      └─ trial-to-paid (7-day trial)
                                │      └─ landing-to-trial
                                └─ sponsor-link CTR by integration class (below)
```

### CTR classes — the only two values ever used

| Integration class | CTR | When it applies |
|---|---|---|
| Tutorial-native | 0.01 | Product is demonstrated inside the lesson/workflow; the integration IS content |
| Standard read | 0.005 | Scripted 30–90s sponsor segment, list/roundup mentions, news channels |

Do not tune CTR per channel on soft signals. It is a ranking assumption, not a prediction; uniform values keep the comparison fair. Real CTRs from tracking links replace assumptions after the first deals go live.

## Rate estimation (Est Rate USD)

CPM method: `90d Avg Views ÷ 1,000 × $25–50`, midpoint $37.50 as the recorded number.
Lean high ($40–50) for high-intent business audiences with sponsor demand; lean low ($25–30) for no sponsor history or spectator-heavy audiences. Always label: `est., CPM method`. The estimate is replaced by the creator's actual quote at first contact; the gap between the two is negotiation room (anchor line: "your average views price this at $X on standard CPMs").

## Derived metrics

```
ROI Score      = (Expected MRR × 12) ÷ Est Rate USD     — sort descending
Payback Months = Est Rate USD ÷ Expected MRR            — reject/renegotiate above ~4
```

Note: with uniform CPM estimates, ROI clusters by CTR class (≈8.6 tutorial-native, ≈4.3 standard). Pre-negotiation ranking therefore leans on Expected MRR magnitude, audience fit, trend, and sponsor density. ROI Scores spread out once real quotes replace estimates.

## Weighted fit assessment (for the verdict, not a formula field)

| Factor | Weight | Evidence source |
|---|---|---|
| Audience fit | 30% | Comment intent + content topics: solopreneurs/creators/SMB owners building content systems |
| Expected ROI | 25% | Funnel model vs estimated rate; payback period |
| Engagement quality | 15% | 30 comments across 2 recent videos: "I built this" (5) → "cool video" (1) |
| Growth trend | 10% | 90-day view trajectory (Social Blade / ViewStats graph) |
| Sponsor density | 10% | Reads counted in last 8 descriptions, normalized to monthly |
| Brand safety & fit | 5% | Drama-free; transparency-about-AI ethos |
| Negotiation ease / affiliate appetite | 5% | Sponsor history, openness to hybrid flat+rev-share |

## Risk Flags — evidence criteria

Apply a flag ONLY when its criterion is met. Blank = vetted, clean.

- **Declining trend**: 90-day views graph visibly down. In a rising category this is a loud signal.
- **Sponsor fatigue**: 4+ reads/month counted, OR documented saturation of the channel's category. Record the count.
- **Audience mismatch**: viewers are researchers, developers-for-entertainment, or salaried employees — profiles that don't buy social-publishing SaaS regardless of content quality.
- **Brand risk**: concrete, citable controversy or safety issue. Never on vibes.
- **Competitor exclusivity**: a competing scheduler seen in recent sponsor reads, or exclusivity confirmed in negotiation.

## Verdict bands

- **Prioritize**: tutorial-native, clean flags, Expected MRR in the channel's top tier, payback < 2 months.
- **Evaluate**: mixed signals — strong on some axes, flagged on others; needs a human judgment call or better data.
- **Reject**: audience mismatch, confirmed fatigue, declining trend, or payback > 4 months. State the killing number in one sentence.
