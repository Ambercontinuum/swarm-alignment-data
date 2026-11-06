"""Delegation/assignment extraction v2 — HEURISTIC, pattern-based.

Changes from v1 (v1 file kept unchanged for comparison):
  1. Hard per-message cap: at most ONE assignment event per target role
     per message, enforced with an explicit seen-set + assertion (v1 had
     this implicitly; v2 makes it a checked invariant).
  2. FRAMING class: a message whose pattern hits cover >= 3 distinct
     target roles is a charter/framing message (the signature of the
     Chief of Staff's opening frame, seq 1, and its ~9 restatements in
     window 0). All its hits are recorded with class="FRAMING" and are
     EXCLUDED from assignment events and assigner shares; framing counts
     are reported separately. Known cost, disclosed: a genuine broadcast
     assignment to 3+ roles (e.g. seq 159, SENTINEL's "point ask") is
     also classified FRAMING by this rule.
  3. Each event records which pattern matched and a short text excerpt,
     so the precision hand-check is auditable against the raw JSONL.

Signal discipline is unchanged from v1: explicit role names with
assignment verbs only (assign/take/own/lead/handle/cover/run/review/
check/build/scout/synthesize/draft/audit/verify), "Role[:=—-]" framing,
or direct address "@Role". No inference, no coreference.

Output remains PRELIMINARY / UNVERIFIED until the IDE-side replica and
the hand-checked precision sample are both in.

Usage: python delegation_extract_v2.py <transcript.jsonl> <out_dir> [window_minutes]
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
FRAMING_MIN_ROLES = 3


def extract(text: str, author: str) -> dict[str, tuple[str, str]]:
    """Return {target_role: (pattern_name, excerpt)} — at most one per role."""
    hits: dict[str, tuple[str, str]] = {}
    for role in ROLES:
        if role == author:
            continue
        esc = re.escape(role)
        pats = [
            ("role_delim", rf"{esc}\s*[:=—–-]\s"),
            ("direct_address", rf"@{esc}\b"),
            ("verb_then_role", rf"\b{VERBS}\b[^.\n]{{0,40}}\b{esc}\b"),
            ("role_then_verb", rf"\b{esc}\b[^.\n]{{0,20}}\b{VERBS}\b"),
        ]
        for name, p in pats:
            m = re.search(p, text)
            if m:
                s = max(0, m.start() - 40)
                excerpt = text[s:m.end() + 40].replace("\n", " ")
                hits[role] = (name, excerpt)
                break  # one event per target role per message — the cap
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
    per_window = defaultdict(Counter)          # ASSIGNMENT events only
    totals = Counter()                          # ASSIGNMENT events only
    framing_per_window = defaultdict(Counter)   # FRAMING hits
    framing_msgs = []
    seen: set[tuple[int, str]] = set()
    for r in rows:
        hits = extract(r["text"], r["author"])
        if not hits:
            continue
        w = int((r["timestamp_ms"] - t0) // window_ms)
        is_framing = len(hits) >= FRAMING_MIN_ROLES
        if is_framing:
            framing_msgs.append({"window": w, "from": r["author"],
                                 "seq": r.get("seq"), "ts": r.get("timestamp_et"),
                                 "targets": sorted(hits)})
        for target, (pat, excerpt) in hits.items():
            key = (id(r), target)
            assert key not in seen, "per-message cap violated"
            seen.add(key)
            cls = "FRAMING" if is_framing else "ASSIGNMENT"
            events.append({"window": w, "from": r["author"], "to": target,
                           "seq": r.get("seq"), "ts": r.get("timestamp_et"),
                           "class": cls, "pattern": pat, "excerpt": excerpt})
            if is_framing:
                framing_per_window[w][r["author"]] += 1
            else:
                per_window[w][r["author"]] += 1
                totals[r["author"]] += 1

    series = []
    for w in sorted(set(per_window) | set(framing_per_window)):
        c = per_window[w]
        tot = sum(c.values())
        entry = {"window": w, "assignments": tot,
                 "by_assigner": dict(c),
                 "framing_hits": sum(framing_per_window[w].values()),
                 "framing_by_author": dict(framing_per_window[w])}
        if tot:
            top = c.most_common(1)[0]
            entry["top_assigner"] = top[0]
            entry["top_share"] = round(top[1] / tot, 3)
        series.append(entry)
    grand = sum(totals.values())
    summary = {
        "extractor": "delegation_extract_v2",
        "total_assignment_events": grand,
        "total_framing_hits": sum(sum(c.values()) for c in framing_per_window.values()),
        "framing_messages": framing_msgs,
        "by_assigner_overall": {a: {"count": n, "share": round(n / grand, 3)}
                                for a, n in totals.most_common()},
        "windows": series,
    }
    (out_dir / "delegation_events_v2.json").write_text(json.dumps(events, indent=2))
    (out_dir / "delegation_summary_v2.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
