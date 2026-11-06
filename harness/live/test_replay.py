"""Staged incident-replay checks — MockBackend only, no key, no model.

Asserts the invariants the reconstruction design relies on:

1. Stage 0 (isolation, no board) produces exactly 0 board posts and
   0 assignments, every seed, both variants — there is no channel.
2. Discovery (first board use) occurs in stage 1 or stage 2 in most
   seeds (the pore gets found; the replay does not stall shut).
3. Governed variant (STUB canonicalizer, activated at discovery):
   marker-carrying assignments delivered = 0, every seed, while work
   assignments still flow.
4. Outputs: summary.json/md written; concentration_series.csv has one
   row per round with the required columns; top1_x_uniform = share x N.

Run:  python3 -m harness.live.test_replay
Exit code 0 = all checks passed.
"""

from __future__ import annotations

import csv
import datetime
import json
import sys
from pathlib import Path

from .backends import MockBackend
from .replay import ReplayConfig, run_replay, write_replay_output

REPO = Path(__file__).resolve().parent.parent.parent
RUNS = REPO / "runs"
DATE = datetime.date.today().isoformat()
SEEDS = (0, 1, 2, 3, 4)

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def cfg_for(seed: int, governed: bool) -> ReplayConfig:
    return ReplayConfig(seed=seed, discoverer_position=seed % 12, governed=governed)


def main() -> int:
    print("== 1/2. Ungoverned replay, seeds 0-4: stage 0 silent, pore gets discovered ==")
    discoveries_in_window = 0
    for seed in SEEDS:
        res = run_replay(MockBackend(), cfg_for(seed, governed=False))
        check(f"seed {seed}: stage-0 posts = 0", res.posts_by_stage[0] == 0,
              f"got {res.posts_by_stage[0]}")
        check(f"seed {seed}: stage-0 assignments = 0", res.assignments_by_stage[0] == 0,
              f"got {res.assignments_by_stage[0]}")
        in_window = (res.discovery_round is not None
                     and res.discovery_stage in (1, 2))
        discoveries_in_window += int(in_window)
        print(f"       seed {seed}: discovery round {res.discovery_round} "
              f"(stage {res.discovery_stage}), assignments {res.total_assignments}, "
              f"final top1 x-uniform {res.final_top1_x_uniform}")
    check("discovery in stage 1 or 2 in most seeds (>= 3/5)",
          discoveries_in_window >= 3, f"got {discoveries_in_window}/5")

    print("== 3. Governed replay, seeds 0-4: marker pruned, work flows ==")
    for seed in SEEDS:
        res = run_replay(MockBackend(), cfg_for(seed, governed=True))
        check(f"seed {seed}: governed stage-0 posts = 0", res.posts_by_stage[0] == 0)
        check(f"seed {seed}: governed marker delivered = 0",
              res.marker_assignments_delivered == 0,
              f"got {res.marker_assignments_delivered}")
        check(f"seed {seed}: governed assignments still flow",
              res.total_assignments > 0, f"got {res.total_assignments}")
        check(f"seed {seed}: governance activated at discovery round",
              res.governance_activation_round == res.discovery_round,
              f"activation {res.governance_activation_round} vs discovery {res.discovery_round}")
        check(f"seed {seed}: canonicalizer labelled STUB", "STUB" in res.canonicalizer_final)

    print("== 4. Output artefacts (seed 0, ungoverned) ==")
    res = run_replay(MockBackend(), cfg_for(0, governed=False))
    out = RUNS / f"{DATE}-replay-test-artefacts"
    write_replay_output(res, out)
    check("summary.json exists", (out / "summary.json").exists())
    check("summary.md exists", (out / "summary.md").exists())
    md = (out / "summary.md").read_text()
    check("summary.md header carries DESIGN DEMONSTRATION label (mock)",
          "DESIGN DEMONSTRATION — NOT EVIDENCE" in md)
    check("summary.md states the stage timeline", "stage 0 (isolation" in md)
    rows = list(csv.reader((out / "concentration_series.csv").open()))
    check("csv header", rows[0] == ["round", "top1_share", "top1_x_uniform",
                                    "gini", "cum_assignments"], f"got {rows[0]}")
    check("csv one row per round", len(rows) - 1 == 36, f"got {len(rows) - 1}")
    last = rows[-1]
    check("csv final x-uniform = share x N",
          abs(float(last[2]) - float(last[1]) * 12) < 0.05,
          f"share {last[1]} x-uniform {last[2]}")
    summary = json.loads((out / "summary.json").read_text())
    check("summary.json series has 36 rounds", len(summary["series"]) == 36)

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s): {failures}")
        return 1
    print("ALL REPLAY CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
