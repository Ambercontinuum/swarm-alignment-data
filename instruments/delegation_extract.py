"""Delegation/assignment extraction v1 — HEURISTIC, pattern-based.

The P2/P3 variable is assignment share (who assigns work to whom), not
message share. v1 extracts (assigner -> assignee) events from transcript
text using explicit signals only:
  - role names mentioned with assignment verbs (assign, take, own, lead,
    handle, cover, run, review, check, build, scout, synthesize...)
  - "Name = ..." / "Name:" framing at line starts
  - direct address forms ("@Name", "Name —")

Known limits: heuristic recall is partial; precision needs a hand-checked
sample before any number from this script is cited. Output is PRELIMINARY.

Usage: python delegation_extract.py <transcript.jsonl> <out_dir> [window_minutes]
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROLES = ["Chief of Staff", "SENTINEL", "Reviewer", "Scout", "Builder", "Research"]
VERBS = (
    r"(?:assign\w*|take|own\w*|lead\w*|handl\w*|cover\w*|run\w*|review\w*|"
    r"check\w*|build\w*|scout\w*|synthes\w*|draft\w*|audit\w*|verif\w*)"
)


def extract(text: str, author: str) -> list[str]:
    hits = []
    for role in ROLES:
        if role == author:
            continue
        esc = re.escape(role)
        pats = [
            rf"{esc}\s*[:=—–-]\s",                       # "Reviewer = signal quality"
            rf"@{esc}\b",
            rf"\b{VERBS}\b[^.\n]{{0,40}}\b{esc}\b",       # verb ... role
            rf"\b{esc}\b[^.\n]{{0,20}}\b{VERBS}\b",       # role ... verb
        ]
        if any(re.search(p, text) for p in pats):
            hits.append(role)
    return hits


def main() -> int:
    src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    window_min = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r.get("text") and r.get("timestamp_ms")]
    rows.sort(key=lambda r: r["timestamp_ms"])
    t0 = rows[0]["timestamp_ms"]
    window_ms = window_min * 60 * 1000

    events = []
    per_window = defaultdict(Counter)
    totals = Counter()
    for r in rows:
        for target in extract(r["text"], r["author"]):
            w = int((r["timestamp_ms"] - t0) // window_ms)
            events.append({"window": w, "from": r["author"], "to": target,
                           "seq": r.get("seq"), "ts": r.get("timestamp_et")})
            per_window[w][r["author"]] += 1
            totals[r["author"]] += 1

    series = []
    for w in sorted(per_window):
        c = per_window[w]
        tot = sum(c.values())
        top = c.most_common(1)[0]
        series.append({"window": w, "assignments": tot,
                       "by_assigner": dict(c),
                       "top_assigner": top[0], "top_share": round(top[1] / tot, 3)})
    grand = sum(totals.values())
    summary = {
        "total_assignment_events": grand,
        "by_assigner_overall": {a: {"count": n, "share": round(n / grand, 3)}
                                for a, n in totals.most_common()},
        "windows": series,
    }
    (out_dir / "delegation_events.json").write_text(json.dumps(events, indent=2))
    (out_dir / "delegation_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print("\n--- sample events ---")
    for e in events[:15]:
        print(e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
