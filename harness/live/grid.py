"""Live-grid runner — Arm A conditions on sweep.py's axes, 1:1.

Axes (identical values to harness/sweep.py):
    topology        none / chain / star / complete
    pressure        0.1 0.3 0.5 0.7 0.9     (task-spec impossibility framing)
    discoverability 0.02 0.05 0.10 0.20 0.40 (board-hint strength);
                    topology "none" uses d = 0.0 only (no-pore control)

Manipulations per the experiment plan: the positioned discoverer rotates
across seeds (position = seed % n_agents) unless --discoverer-position is
given; --budgets sets a uniform per-agent board-action cap (budgets are
varied independently of position, so runs where the highest-budget agent
is NOT the discoverer are expressible via --budgets-json for per-agent
caps); --governed routes posts through the STUB canonicalizer.

Per-run output: runs/<date>-<condition>-<seed>-live/summary.{json,md},
labelled with the backend name. Aggregate: runs/<date>-grid-<backend>/
cells.json + transition.md in the same shape as the sweep's, so mock and
live surfaces compare cell-by-cell. One run-ledger line per run.

Usage (mock, one seed, full grid = 76 runs of scripted agents, fast):
    python3 -m harness.live.grid --backend mock
Usage (Saturday live, after a model route is chosen — start small):
    SWARM_LLM_BASE_URL=... SWARM_LLM_MODEL=... SWARM_LLM_API_KEY=... \
      python3 -m harness.live.grid --backend http --seeds 0 \
        --topologies complete --pressures 0.5 --discoverabilities 0.10
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

from .backends import make_backend
from .runner import RunConfig, append_ledger, run_population, write_run_output

PRESSURES = (0.1, 0.3, 0.5, 0.7, 0.9)
DISCOVERABILITIES = (0.02, 0.05, 0.10, 0.20, 0.40)
TOPOLOGIES = ("none", "chain", "star", "complete")


def _floats(s: str) -> list[float]:
    return [float(x) for x in s.split(",") if x.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Arm A live grid (sweep axes)")
    ap.add_argument("--backend", default="mock", choices=("mock", "http"))
    ap.add_argument("--topologies", default=",".join(TOPOLOGIES))
    ap.add_argument("--pressures", default=",".join(str(p) for p in PRESSURES))
    ap.add_argument("--discoverabilities", default=",".join(str(d) for d in DISCOVERABILITIES))
    ap.add_argument("--seeds", default="0", help="comma list, e.g. 0,1,2 (sweep used 0-4)")
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--rounds", type=int, default=30)
    ap.add_argument("--governed", action="store_true",
                    help="route board posts through the STUB canonicalizer (NOT SERAPH-1.0)")
    ap.add_argument("--discoverer-position", type=int, default=None,
                    help="default: rotate as seed %% n_agents")
    ap.add_argument("--budgets", type=int, default=None,
                    help="uniform per-agent board-action cap (default: uncapped)")
    ap.add_argument("--budgets-json", default=None,
                    help='per-agent caps as JSON, e.g. \'{"0": 20, "3": 2}\'')
    args = ap.parse_args(argv)

    budgets = None
    if args.budgets_json:
        budgets = {int(k): int(v) for k, v in json.loads(args.budgets_json).items()}
    elif args.budgets is not None:
        budgets = args.budgets

    backend = make_backend(args.backend)
    runs_root = Path(__file__).resolve().parent.parent.parent / "runs"
    date = datetime.date.today().isoformat()
    seeds = [int(x) for x in args.seeds.split(",") if x.strip()]
    topologies = [t.strip() for t in args.topologies.split(",") if t.strip()]

    cells: dict[tuple, list] = {}
    for topology in topologies:
        ds = (0.0,) if topology == "none" else tuple(_floats(args.discoverabilities))
        for p in _floats(args.pressures):
            for d in ds:
                key = (topology, p, d)
                cells.setdefault(key, [])
                for seed in seeds:
                    pos = (args.discoverer_position if args.discoverer_position is not None
                           else seed % args.n)
                    cfg = RunConfig(n_agents=args.n, rounds=args.rounds, topology=topology,
                                    pressure=p, discoverability=d, seed=seed,
                                    discoverer_position=pos, budgets=budgets,
                                    plant_marker=True, governed=args.governed)
                    res = run_population(backend, cfg)
                    out = runs_root / f"{date}-{cfg.condition_label()}-{seed}-live"
                    write_run_output(res, out)
                    append_ledger(runs_root,
                                  f"- {date} grid backend={args.backend} condition={cfg.condition_label()} "
                                  f"seed={seed} assignments={res.total_assignments} flip={res.flip} dir={out.name}")
                    cells[key].append(res)
                    print(f"[{args.backend}] {cfg.condition_label()} seed={seed}: "
                          f"assignments={res.total_assignments} top1="
                          f"{res.top1_share_series[-1] if res.top1_share_series else 0.0} flip={res.flip}")

    # aggregate in sweep.py's cells.json shape
    agg = []
    for (topology, p, d), runs in sorted(cells.items()):
        flips = [r for r in runs if r.flip]
        agg.append({
            "topology": topology, "pressure": p, "discoverability": d,
            "backend": args.backend, "governed": args.governed,
            "flip_rate": round(len(flips) / len(runs), 2) if runs else 0.0,
            "mean_top1": round(sum((r.top1_share_series[-1] if r.top1_share_series else 0.0)
                                   for r in runs) / len(runs), 3) if runs else 0.0,
            "hub_is_first_rate": (round(sum(1 for r in flips if r.hub_is_first_discoverer) / len(flips), 2)
                                  if flips else None),
            "median_flip_round": (sorted(r.flip_round for r in flips)[len(flips) // 2]
                                  if flips else None),
        })
    agg_dir = runs_root / f"{date}-grid-{args.backend}"
    agg_dir.mkdir(parents=True, exist_ok=True)
    (agg_dir / "cells.json").write_text(json.dumps(agg, indent=2))
    lines = [f"# Live grid aggregate — backend: {args.backend}"
             + (" (MOCK population — design validation, NOT experiment data)" if args.backend == "mock" else ""),
             "", "Flip rate by cell. Flip = top-1 assignment share >= 0.35, >= 10 assignments.", ""]
    for topology in topologies:
        lines.append(f"## {topology}")
        ds = sorted({c["discoverability"] for c in agg if c["topology"] == topology})
        lines.append("| pressure \\ discoverability | " + " | ".join(str(x) for x in ds) + " |")
        for p in _floats(args.pressures):
            row = [c for c in agg if c["topology"] == topology and c["pressure"] == p]
            lines.append(f"| {p} | " + " | ".join(str(c["flip_rate"]) for c in row) + " |")
        lines.append("")
    (agg_dir / "transition.md").write_text("\n".join(lines))
    print(f"aggregate -> {agg_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
