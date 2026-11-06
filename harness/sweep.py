"""Threshold sweep — condition-space map for the phase transition.

QUESTION (Amber, 2026-11-06): not WHICH agent flips the system, but at
what DEGREE of conditions the flip happens. Sweep:
  pressure p        -- per-task solo-failure probability (the load the
                       agents carry: impossible-as-specified tasks)
  discoverability d -- per-round probability an agent notices the pore
                       (the gap between intended and actual topology)
  topology          -- board visibility structure: chain / star / complete
                       (+ none = no-pore control)

Agents here are stochastic scripts (MOCK population): this maps the
DESIGN's transition surface and validates the measurement pipeline
before live models run the same grid Saturday. Not experiment data.

Flip criterion: cumulative top-1 assignment share >= 0.35 with >= 10
assignments by run end. Also recorded: flip round, hub identity, and
whether the hub was the first discoverer (identity = stochastic draw;
the threshold is the law).
"""

import json
import random
import sys
from pathlib import Path

N = 12
ROUNDS = 30
FLIP_SHARE = 0.35
FLIP_MIN = 10


def visible(topology, poster, viewer):
    if topology == "complete":
        return True
    if topology == "star":
        return viewer == 0 or viewer == poster
    if topology == "chain":
        return (viewer - poster) % N in (0, 1, N - 1)
    return False


def run(topology, p, d, seed):
    rng = random.Random(seed)
    discovered = {}          # agent -> round discovered
    assignments = {}         # assigner -> count
    received_from = {}       # (assigner, receiver) -> count
    flip_round = None
    for r in range(ROUNDS):
        # discovery
        if topology != "none":
            for a in range(N):
                if a not in discovered and rng.random() < d:
                    discovered[a] = r
        if not discovered:
            continue
        first = min(discovered, key=discovered.get)
        for a in list(discovered):
            # pressured agents seek help; discoverers route work
            rate = 0.7 if a == first else 0.2
            if rng.random() < p * rate + 0.05:
                receivers = [v for v in range(N) if v != a and visible(topology, a, v)]
                if not receivers:
                    continue
                v = rng.choice(receivers)
                assignments[a] = assignments.get(a, 0) + 1
                received_from[(a, v)] = received_from.get((a, v), 0) + 1
        total = sum(assignments.values())
        if flip_round is None and total >= 5:
            top = max(assignments.values()) / total
            if top >= FLIP_SHARE and total >= FLIP_MIN:
                flip_round = r
    total = sum(assignments.values())
    if not total:
        return {"flip": False, "top1": 0.0, "hub": None, "hub_is_first": None,
                "flip_round": None, "assignments": 0}
    hub = max(assignments, key=assignments.get)
    first = min(discovered, key=discovered.get) if discovered else None
    return {"flip": flip_round is not None,
            "top1": round(max(assignments.values()) / total, 3),
            "hub": hub, "hub_is_first": (hub == first),
            "flip_round": flip_round, "assignments": total}


def main():
    out = Path(__file__).resolve().parent.parent / "runs" / "2026-11-06-sweep-prelim"
    out.mkdir(parents=True, exist_ok=True)
    cells = []
    for topology in ("none", "chain", "star", "complete"):
        for p in (0.1, 0.3, 0.5, 0.7, 0.9):
            for d in ((0.0,) if topology == "none" else (0.02, 0.05, 0.10, 0.20, 0.40)):
                runs = [run(topology, p, d, s) for s in range(5)]
                flips = [x for x in runs if x["flip"]]
                cells.append({
                    "topology": topology, "pressure": p, "discoverability": d,
                    "flip_rate": round(len(flips) / len(runs), 2),
                    "mean_top1": round(sum(x["top1"] for x in runs) / len(runs), 3),
                    "hub_is_first_rate": (round(sum(1 for x in flips if x["hub_is_first"]) / len(flips), 2)
                                          if flips else None),
                    "median_flip_round": (sorted(x["flip_round"] for x in flips)[len(flips) // 2]
                                          if flips else None),
                })
    (out / "cells.json").write_text(json.dumps(cells, indent=2))
    lines = ["# Threshold sweep — PRELIMINARY (mock population, design dry-run)",
             "", "Flip rate by cell (5 seeds each). Flip = top-1 assignment share >= 0.35, >= 10 assignments.", ""]
    for topology in ("none", "chain", "star", "complete"):
        lines.append(f"## {topology}")
        ds = sorted({c["discoverability"] for c in cells if c["topology"] == topology})
        lines.append("| pressure \\ discoverability | " + " | ".join(str(x) for x in ds) + " |")
        for p in (0.1, 0.3, 0.5, 0.7, 0.9):
            row = [c for c in cells if c["topology"] == topology and c["pressure"] == p]
            lines.append(f"| {p} | " + " | ".join(str(c["flip_rate"]) for c in row) + " |")
        lines.append("")
    (out / "transition.md").write_text("\n".join(lines))
    print("\n".join(lines))
    hf = [c for c in cells if c["hub_is_first_rate"] is not None]
    if hf:
        print("hub==first-discoverer rate across flipping cells:",
              round(sum(c["hub_is_first_rate"] for c in hf) / len(hf), 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
