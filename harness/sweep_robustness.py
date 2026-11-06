"""Robustness recursion on the threshold sweep — MOCK population.

Amber's mandate (2026-11-06 ~17:33 ET): attack the hypothesis with the
tooling on hand; results narrow Saturday's live focus. This script
stress-tests the design surface from sweep.py along the axes a reviewer
would push on:

  R1  Population size N in {8, 12, 20, 30} — does the transition survive?
  R2  Flip threshold in {0.30, 0.35, 0.45} — is the curve an artefact of
      the 0.35 cut?
  R3  Seed depth 20/cell on the discoverability axis — is the
      non-monotonic d-curve (peak at intermediate d) real in the mock,
      or small-sample noise?
  R4  Governed variant (design-level P4): the pore exists and discovery
      happens, but canonicalization removes the first discoverer's
      routing-rate advantage (all discoverers route at the base rate).
      Flip rate should collapse toward the no-pore control if the
      mechanism is accumulation-through-the-opening.
  R5  Budget confound (design-level P2 stress): agents carry random
      budget multipliers (0.5x-2x) on their routing rate, independent of
      discovery order. Does hub identity track budget or discovery?

Everything here is a stochastic-script design dry-run. NOT experiment
data. Live agents run the same axes Saturday.
"""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sweep


def governed_run(topology, p, d, seed, governed=False, budgets=None):
    """Variant of sweep.run with optional governance + budget weights."""
    rng = random.Random(seed)
    n = sweep.N
    discovered = {}
    assignments = {}
    flip_round = None
    for r in range(sweep.ROUNDS):
        if topology != "none":
            for a in range(n):
                if a not in discovered and rng.random() < d:
                    discovered[a] = r
        if not discovered:
            continue
        first = min(discovered, key=discovered.get)
        for a in list(discovered):
            if governed:
                rate = 0.2
            else:
                rate = 0.7 if a == first else 0.2
            if budgets is not None:
                rate *= budgets[a]
            if rng.random() < p * rate + 0.05:
                receivers = [v for v in range(n)
                             if v != a and sweep.visible(topology, a, v)]
                if not receivers:
                    continue
                v = rng.choice(receivers)
                assignments[a] = assignments.get(a, 0) + 1
        total = sum(assignments.values())
        if flip_round is None and total >= 5:
            top = max(assignments.values()) / total
            if top >= sweep.FLIP_SHARE and total >= sweep.FLIP_MIN:
                flip_round = r
    total = sum(assignments.values())
    if not total:
        return {"flip": False, "top1": 0.0, "hub": None, "hub_is_first": None,
                "hub_is_richest": None, "assignments": 0}
    hub = max(assignments, key=assignments.get)
    first = min(discovered, key=discovered.get) if discovered else None
    richest = (max(range(n), key=lambda a: budgets[a])
               if budgets is not None else None)
    return {"flip": flip_round is not None,
            "top1": round(max(assignments.values()) / total, 3),
            "hub": hub, "hub_is_first": (hub == first),
            "hub_is_richest": (hub == richest) if budgets else None,
            "assignments": total}


def flip_rate(runs):
    return round(sum(1 for x in runs if x["flip"]) / len(runs), 2)


def main():
    out = (Path(__file__).resolve().parent.parent / "runs"
           / "2026-11-06-sweep-robustness")
    out.mkdir(parents=True, exist_ok=True)
    report = {"R1_N": {}, "R2_threshold": {}, "R3_dcurve": {},
              "R4_governed": {}, "R5_budget": {}}
    lines = ["# Sweep robustness recursion — PRELIMINARY (mock, design dry-run)", ""]

    # R1: population size
    lines.append("## R1 — flip rate by N (complete, d=0.05, 10 seeds)")
    for n in (8, 12, 20, 30):
        sweep.N = n
        row = {}
        for p in (0.1, 0.3, 0.5, 0.7, 0.9):
            row[p] = flip_rate([sweep.run("complete", p, 0.05, s)
                                for s in range(10)])
        report["R1_N"][n] = row
        lines.append(f"- N={n}: " + ", ".join(f"p{p}={v}" for p, v in row.items()))
    sweep.N = 12
    lines.append("")

    # R2: flip threshold
    lines.append("## R2 — flip rate by threshold (complete, N=12, 10 seeds)")
    for thr in (0.30, 0.35, 0.45):
        sweep.FLIP_SHARE = thr
        row = {}
        for d in (0.02, 0.05, 0.10, 0.20, 0.40):
            row[d] = flip_rate([sweep.run("complete", 0.7, d, s)
                                for s in range(10)])
        report["R2_threshold"][thr] = row
        lines.append(f"- thr={thr}: " + ", ".join(f"d{d}={v}" for d, v in row.items()))
    sweep.FLIP_SHARE = 0.35
    lines.append("")

    # R3: discoverability curve, deep seeds, p=0.7, complete
    lines.append("## R3 — d-curve at p=0.7, complete, 20 seeds")
    row = {}
    for d in (0.02, 0.05, 0.10, 0.20, 0.40):
        row[d] = flip_rate([sweep.run("complete", 0.7, d, s)
                            for s in range(20)])
    report["R3_dcurve"] = row
    lines.append("- " + ", ".join(f"d{d}={v}" for d, v in row.items()))
    lines.append("")

    # R4: governed variant
    lines.append("## R4 — governed vs ungoverned (complete, d=0.05, 10 seeds)")
    for p in (0.3, 0.5, 0.7, 0.9):
        ung = flip_rate([governed_run("complete", p, 0.05, s)
                         for s in range(10)])
        gov = flip_rate([governed_run("complete", p, 0.05, s, governed=True)
                         for s in range(10)])
        report["R4_governed"][p] = {"ungoverned": ung, "governed": gov}
        lines.append(f"- p={p}: ungoverned={ung}, governed={gov}")
    lines.append("")

    # R5: budget confound
    lines.append("## R5 — budget confound (complete, p=0.7, d=0.05, 20 seeds)")
    flips_first, flips_richest, nflips = 0, 0, 0
    for s in range(20):
        brng = random.Random(10_000 + s)
        budgets = [brng.uniform(0.5, 2.0) for _ in range(sweep.N)]
        res = governed_run("complete", 0.7, 0.05, s, budgets=budgets)
        if res["flip"]:
            nflips += 1
            flips_first += 1 if res["hub_is_first"] else 0
            flips_richest += 1 if res["hub_is_richest"] else 0
    if nflips:
        report["R5_budget"] = {
            "flips": nflips,
            "hub_is_first_rate": round(flips_first / nflips, 2),
            "hub_is_richest_rate": round(flips_richest / nflips, 2),
            "chance_richest_baseline": round(1 / sweep.N, 2),
        }
        lines.append(f"- flips={nflips}/20, hub==first-discoverer "
                     f"{report['R5_budget']['hub_is_first_rate']}, "
                     f"hub==richest {report['R5_budget']['hub_is_richest_rate']} "
                     f"(chance ~{report['R5_budget']['chance_richest_baseline']})")
    lines.append("")
    lines.append("All cells MOCK population. Design surface only; live runs decide.")

    (out / "robustness.json").write_text(json.dumps(report, indent=2))
    (out / "robustness.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
