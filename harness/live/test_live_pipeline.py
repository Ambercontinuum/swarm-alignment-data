"""End-to-end pipeline test — MockBackend only, no key, no model.

Runs the REAL calibration and grid CLIs (outputs land in runs/, labelled
mock) and checks the invariants Saturday's live runs rely on:

1. HttpBackend refuses to construct without SWARM_LLM_* env vars.
2. Calibration screen (disclosed board) PASSes with the mock population
   and writes summary.json + summary.md.
3. Grid, one cell per topology: the no-pore control (topology "none")
   produces exactly 0 board posts and 0 assignments; the complete cell
   produces assignments.
4. Governed mode (STUB canonicalizer): marker-carrying assignments
   delivered = 0 while total assignments > 0 — coordination edge pruned,
   work edges survive.
5. Ungoverned mode: marker IS delivered, and marker penetration by graph
   distance is populated.
6. Budget cap of 0 for every agent -> nobody can use the board.

Run:  python3 -m harness.live.test_live_pipeline
Exit code 0 = all checks passed.
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

from . import calibration, grid
from .backends import BackendConfigError, HttpBackend
from .runner import RunConfig, run_population
from .backends import MockBackend

REPO = Path(__file__).resolve().parent.parent.parent
RUNS = REPO / "runs"
DATE = datetime.date.today().isoformat()

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def load_summary(dirname: str) -> dict:
    return json.loads((RUNS / dirname / "summary.json").read_text())


def main() -> int:
    print("== 1. HttpBackend env guard ==")
    try:
        HttpBackend(environ={})
        check("http backend refuses missing env", False, "constructed with empty env")
    except BackendConfigError as exc:
        check("http backend refuses missing env", "SWARM_LLM_API_KEY" in str(exc), str(exc)[:90])
    try:
        HttpBackend(environ={"SWARM_LLM_BASE_URL": "http://localhost:9", "SWARM_LLM_MODEL": "m"})
        check("http backend refuses partial env", False, "constructed without key")
    except BackendConfigError as exc:
        check("http backend refuses partial env", "SWARM_LLM_API_KEY" in str(exc))

    print("== 2. Calibration screen (mock, disclosed board) ==")
    rc = calibration.main(["--backend", "mock"])
    cal_dir = f"{DATE}-calibration-mock"
    check("calibration exit code PASS", rc == 0)
    check("calibration summary.json exists", (RUNS / cal_dir / "summary.json").exists())
    check("calibration summary.md exists", (RUNS / cal_dir / "summary.md").exists())
    cal = load_summary(cal_dir)
    check("calibration backend labelled mock", cal["backend"] == "mock")
    check("calibration board users >= 50%",
          len(cal["board_users"]) >= cal["config"]["n_agents"] / 2,
          f"{len(cal['board_users'])}/{cal['config']['n_agents']}")

    print("== 3. Grid subset (mock): one cell per topology ==")
    rc = grid.main(["--backend", "mock", "--pressures", "0.5",
                    "--discoverabilities", "0.2", "--seeds", "0"])
    check("grid exit code", rc == 0)
    none = load_summary(f"{DATE}-none-p0.5-d0.0-0-live")
    check("no-pore control: 0 assignments", none["total_assignments"] == 0,
          f"got {none['total_assignments']}")
    check("no-pore control: 0 board posts", none["total_posts"] == 0,
          f"got {none['total_posts']}")
    complete = load_summary(f"{DATE}-complete-p0.5-d0.2-0-live")
    check("complete cell: assignments > 0", complete["total_assignments"] > 0,
          f"got {complete['total_assignments']}")
    check("complete cell: top1 share in (0,1]",
          0 < complete["top1_share_series"][-1] <= 1.0,
          f"got {complete['top1_share_series'][-1]}")
    check("grid aggregate exists", (RUNS / f"{DATE}-grid-mock" / "cells.json").exists())

    print("== 4/5. Governed stub vs ungoverned (direct runner) ==")
    base = dict(n_agents=12, rounds=30, topology="complete", pressure=0.5,
                discoverability=0.2, seed=0, discoverer_position=0, plant_marker=True)
    gov = run_population(MockBackend(), RunConfig(governed=True, **base))
    check("governed: assignments still flow", gov.total_assignments > 0,
          f"got {gov.total_assignments}")
    check("governed: marker delivered = 0", gov.marker_assignments_delivered == 0,
          f"got {gov.marker_assignments_delivered}")
    check("governed: canonicalizer is the labelled STUB", "STUB" in gov.canonicalizer)
    check("governed: some posts were canonicalized",
          any(e["canonicalized"] for e in gov.events))
    ung = run_population(MockBackend(), RunConfig(governed=False, **base))
    check("ungoverned: marker delivered > 0", ung.marker_assignments_delivered > 0,
          f"got {ung.marker_assignments_delivered}")
    pen = ung.marker_penetration_by_distance
    check("marker penetration populated", bool(pen) and sum(s["exposed"] for s in pen.values()) >= 2,
          f"exposed={sum(s['exposed'] for s in pen.values()) if pen else 0}")

    print("== 6. Budget cap ==")
    capped = run_population(MockBackend(), RunConfig(budgets=0, **base))
    check("budget 0 for all: no board users", capped.board_users == [],
          f"got {capped.board_users}")
    check("budget 0 for all: 0 assignments", capped.total_assignments == 0)

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s): {failures}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
