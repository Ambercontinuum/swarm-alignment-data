"""CHANDRA per-agent/per-window adapter (NEW code, this sprint).

Reads a multi-agent transcript JSONL (Footprint Committee format:
{author, timestamp_ms, text, kind}), buckets entries into time windows,
and for each agent x window runs CHANDRA's full_diagnostic on that
agent's text. Emits per-agent state series + message-share series.

CHANDRA itself is PREEXISTING and unmodified (github.com/Ambercontinuum/CHANDRA).
Its scores are operational pattern scores from an unvalidated instrument;
say so wherever these numbers travel.

Usage:
    python chandra_adapter.py <transcript.jsonl> <chandra_dir> <out_dir> [window_minutes]
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def main() -> int:
    src, chandra_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    window_min = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    out_dir.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(chandra_dir))
    from chandra import CHANDRA  # noqa: E402

    rows = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r.get("text") and r.get("timestamp_ms")]
    rows.sort(key=lambda r: r["timestamp_ms"])
    t0 = rows[0]["timestamp_ms"]
    window_ms = window_min * 60 * 1000

    buckets: dict[tuple[int, str], list[str]] = defaultdict(list)
    counts: dict[tuple[int, str], int] = defaultdict(int)
    for r in rows:
        w = (r["timestamp_ms"] - t0) // window_ms
        buckets[(w, r["author"])].append(r["text"])
        counts[(w, r["author"])] += 1

    diag = CHANDRA()
    windows = sorted({w for (w, _a) in buckets})
    series = []
    share_series = []
    for w in windows:
        total = sum(c for (ww, _a), c in counts.items() if ww == w)
        shares = {
            a: round(c / total, 3)
            for (ww, a), c in counts.items()
            if ww == w
        }
        top_agent = max(shares, key=shares.get) if shares else None
        share_series.append(
            {"window": int(w), "total_messages": total, "shares": shares,
             "top_agent": top_agent, "top_share": shares.get(top_agent, 0.0)}
        )
        for (ww, author), texts in sorted(buckets.items()):
            if ww != w:
                continue
            res = diag.full_diagnostic("\n".join(texts), ai_responses=texts)
            chn = res["chn_profile"]
            series.append({
                "window": int(w),
                "author": author,
                "messages": counts[(ww, author)],
                "share": shares.get(author, 0.0),
                "dominant_level": chn["dominant_level"]["level"],
                "dominant_name": chn["dominant_level"].get("name"),
                "stage": chn.get("stage") or chn.get("developmental_stage"),
                "avg_vulnerability": res["symbolic_pressure"]["average_vulnerability"],
                "overall_health": res["overall_health"],
            })

    (out_dir / "chandra_series.json").write_text(json.dumps(series, indent=2))
    (out_dir / "share_series.json").write_text(json.dumps(share_series, indent=2))
    print(f"windows={len(windows)} agent_windows={len(series)}")
    for s in share_series:
        print(f"window {s['window']}: n={s['total_messages']} top={s['top_agent']} share={s['top_share']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
