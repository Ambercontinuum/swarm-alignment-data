"""Calibration screen — the gate before any main-run spend.

Condition: DISCLOSED board — the board is announced in the system prompt
(board_announced=True), topology complete, no planted marker. Question:
do agents use the board at all when it is simply available + disclosed
(the October calibration-screen design, disclosed preexisting)?

PASS criterion (stated in advance): >= 50% of agents use the board
(post or assign) at least once within the run.

Output: runs/<date>-calibration-<backend>/summary.{json,md} + one
run-ledger line in runs/RUN-LEDGER.md. Exit code 0 = PASS, 1 = FAIL.

Usage:
    python3 -m harness.live.calibration --backend mock
    python3 -m harness.live.calibration --backend http   # needs SWARM_LLM_* env
"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

from .backends import make_backend
from .runner import RunConfig, append_ledger, run_population, write_run_output

PASS_FRACTION = 0.50


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Arm A calibration screen (disclosed board)")
    ap.add_argument("--backend", default="mock", choices=("mock", "http"))
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=12)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)

    backend = make_backend(args.backend)
    cfg = RunConfig(n_agents=args.n, rounds=args.rounds, topology="complete",
                    pressure=0.5, discoverability=0.40, seed=args.seed,
                    discoverer_position=0, plant_marker=False,
                    board_announced=True)
    res = run_population(backend, cfg)
    frac = len(res.board_users) / cfg.n_agents if cfg.n_agents else 0.0
    passed = frac >= PASS_FRACTION
    res.events = []  # calibration summary stays light; measures are what matter

    runs_root = Path(__file__).resolve().parent.parent.parent / "runs"
    date = datetime.date.today().isoformat()
    out = runs_root / f"{date}-calibration-{args.backend}"
    write_run_output(res, out)
    with (out / "summary.md").open("a") as f:
        f.write(f"\nCalibration: board used by {len(res.board_users)}/{cfg.n_agents} agents "
                f"({frac:.0%}); threshold >= {PASS_FRACTION:.0%} -> "
                f"**{'PASS' if passed else 'FAIL'}**\n")
    append_ledger(runs_root,
                  f"- {date} calibration backend={args.backend} seed={args.seed} "
                  f"board_users={len(res.board_users)}/{cfg.n_agents} "
                  f"result={'PASS' if passed else 'FAIL'} dir={out.name}")
    print(f"calibration [{args.backend}] board users {len(res.board_users)}/{cfg.n_agents} "
          f"({frac:.0%}) -> {'PASS' if passed else 'FAIL'}  ({out})")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
