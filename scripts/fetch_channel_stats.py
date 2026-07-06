#!/usr/bin/env python3
"""
fetch_channel_stats.py — pull vetting stats for a YouTube channel.

Usage:
    YT_API_KEY=xxxx python fetch_channel_stats.py "https://www.youtube.com/@nateherk"
    YT_API_KEY=xxxx python fetch_channel_stats.py "@nateherk" --videos 15

Outputs JSON with: subscribers, total views, recent regular uploads (Shorts and
livestreams excluded), trimmed 90d average views (outliers >3x or <1/3 of the
median excluded and reported), upload cadence, and a sponsor scan of recent
descriptions (count + detected brand mentions).

Requires only the Python standard library. Free API key:
https://console.cloud.google.com/apis/library/youtube.googleapis.com
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from statistics import median

API = "https://www.googleapis.com/youtube/v3"

SPONSOR_PATTERNS = [
    r"sponsored by ([A-Z][\w .&-]{2,40})",
    r"thanks to ([A-Z][\w .&-]{2,40}) for sponsoring",
    r"this video is brought to you by ([A-Z][\w .&-]{2,40})",
    r"brought to you by ([A-Z][\w .&-]{2,40})",
    r"today'?s sponsor[,:]? ([A-Z][\w .&-]{2,40})",
    r"use (?:code|coupon) [A-Z0-9]{3,20}",
    r"partner(?:ed)? with ([A-Z][\w .&-]{2,40})",
]


def api_get(endpoint: str, **params) -> dict:
    params["key"] = os.environ["YT_API_KEY"]
    url = f"{API}/{endpoint}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def resolve_channel(handle_or_url: str) -> str:
    """Return a channel ID from a URL, @handle, or bare name."""
    s = handle_or_url.strip()
    m = re.search(r"youtube\.com/channel/(UC[\w-]{22})", s)
    if m:
        return m.group(1)
    m = re.search(r"youtube\.com/@([\w.-]+)", s)
    handle = m.group(1) if m else s.lstrip("@")
    data = api_get("channels", part="id", forHandle=f"@{handle}")
    items = data.get("items", [])
    if not items:  # last resort: search
        data = api_get("search", part="snippet", q=handle, type="channel", maxResults=1)
        items = data.get("items", [])
        if not items:
            sys.exit(f"ERROR: channel not found for '{handle_or_url}'")
        return items[0]["snippet"]["channelId"]
    return items[0]["id"]


def iso_duration_seconds(d: str) -> int:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def scan_sponsors(text: str) -> list[str]:
    hits = []
    for pat in SPONSOR_PATTERNS:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            hits.append(m.group(1).strip() if m.groups() and m.group(1) else "promo code")
    return hits


def main() -> None:
    if "YT_API_KEY" not in os.environ:
        sys.exit("ERROR: set the YT_API_KEY environment variable (free YouTube Data API v3 key).")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    target = sys.argv[1]
    n_videos = 15
    if "--videos" in sys.argv:
        n_videos = int(sys.argv[sys.argv.index("--videos") + 1])

    cid = resolve_channel(target)
    ch = api_get("channels", part="snippet,statistics,contentDetails", id=cid)["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]

    # Pull enough playlist items to survive Shorts/livestream filtering.
    video_ids, page = [], None
    while len(video_ids) < n_videos * 3:
        kw = {"part": "contentDetails", "playlistId": uploads, "maxResults": 50}
        if page:
            kw["pageToken"] = page
        pl = api_get("playlistItems", **kw)
        video_ids += [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
        page = pl.get("nextPageToken")
        if not page:
            break

    vids = []
    for i in range(0, len(video_ids), 50):
        batch = api_get(
            "videos",
            part="snippet,statistics,contentDetails,liveStreamingDetails",
            id=",".join(video_ids[i : i + 50]),
        )
        vids += batch.get("items", [])

    regular = [
        v for v in vids
        if iso_duration_seconds(v["contentDetails"].get("duration", "")) > 90
        and "liveStreamingDetails" not in v
    ][:n_videos]

    if not regular:
        sys.exit("ERROR: no regular uploads found (channel may be Shorts-only).")

    views = [int(v["statistics"].get("viewCount", 0)) for v in regular]
    med = median(views)
    kept = [x for x in views if med / 3 <= x <= med * 3] or views
    outliers = [x for x in views if x not in kept]
    avg = round(sum(kept) / len(kept))

    newest = datetime.fromisoformat(regular[0]["snippet"]["publishedAt"].replace("Z", "+00:00"))
    oldest = datetime.fromisoformat(regular[-1]["snippet"]["publishedAt"].replace("Z", "+00:00"))
    weeks = max(((newest - oldest).days / 7), 1)
    per_month = round(len(regular) / weeks * 4.33, 1)

    ninety_days_ago = datetime.now(timezone.utc) - timedelta(days=90)
    in_window = sum(
        1 for v in regular
        if datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00")) >= ninety_days_ago
    )

    sponsor_hits, sponsored_videos = [], 0
    for v in regular[:8]:
        hits = scan_sponsors(v["snippet"].get("description", ""))
        if hits:
            sponsored_videos += 1
            sponsor_hits += hits
    reads_per_month = round(sponsored_videos / max(len(regular[:8]) / max(per_month, 0.1), 0.1), 1) if per_month else None

    print(json.dumps({
        "channel": ch["snippet"]["title"],
        "channel_id": cid,
        "url": f"https://www.youtube.com/channel/{cid}",
        "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "subscribers": int(ch["statistics"].get("subscriberCount", 0)),
        "total_views": int(ch["statistics"].get("viewCount", 0)),
        "sampled_regular_uploads": len(regular),
        "uploads_in_last_90d": in_window,
        "uploads_per_month": per_month,
        "avg_views_trimmed": avg,
        "outlier_views_excluded": outliers,
        "raw_recent_views": views,
        "sponsor_scan": {
            "videos_scanned": len(regular[:8]),
            "sponsored_videos": sponsored_videos,
            "estimated_reads_per_month": reads_per_month,
            "detected_brands": sorted(set(sponsor_hits)),
            "note": "Description scan only — verify first 90s of top candidates by watching.",
        },
        "provenance": "YouTube Data API v3; Shorts (<=90s) and livestreams excluded; outliers >3x or <1/3 median trimmed.",
    }, indent=2))


if __name__ == "__main__":
    main()
