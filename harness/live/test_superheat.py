"""Superheat condition checks (protocol P6) — MockBackend only.

Asserts the invariants the sealed staging relies on:

1. During the SEALED stage (pore exists, discoverability forced to
   floor 0.0) there are exactly 0 board posts and 0 assignments, every
   seed — the site is present but inactive.
2. Stage 0 (isolation) stays silent in sealed runs.
3. ACTIVATION works: discovery occurs at or after the activation round
   (the first stage-2 round) in most seeds, for sealed durations 8
   and 16.
4. The P6 measures are present in the run summary: activation round,
   activation->discovery latency, discovery->flip latency,
   discovery->settled-hub latency (succession), post-activation and
   post-discovery assignment velocity over the first 5 rounds.
5. Control (sealed = 0) is the existing staging: no activation round,
   and stage 1 carries traffic as before.

Run:  python3 -m harness.live.test_superheat
Exit code 0 = all checks passed.
"""

from __future__ import annotations

import sys

from .backends import MockBackend
from .replay import ReplayConfig, run_replay

SEEDS = (0, 1, 2, 3, 4)
PORE = 9  # default pore_round

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def cfg_for(seed: int, sealed: int) -> ReplayConfig:
    return ReplayConfig(seed=seed, discoverer_position=seed % 12,
                        sealed_rounds=sealed, pressure=0.7)


def main() -> int:
    for sealed in (8, 16):
        activation = PORE + sealed
        print(f"== Sealed = {sealed} (activation at round {activation}), seeds 0-4 ==")
        discovered_after_activation = 0
        for seed in SEEDS:
            res = run_replay(MockBackend(), cfg_for(seed, sealed))
            d = res.as_dict()
            check(f"s{sealed} seed {seed}: stage-0 posts = 0",
                  res.posts_by_stage[0] == 0, f"got {res.posts_by_stage[0]}")
            check(f"s{sealed} seed {seed}: sealed-stage posts = 0",
                  res.posts_by_stage[1] == 0, f"got {res.posts_by_stage[1]}")
            check(f"s{sealed} seed {seed}: sealed-stage assignments = 0",
                  res.assignments_by_stage[1] == 0,
                  f"got {res.assignments_by_stage[1]}")
            cum_at_activation = next(
                s["cum_assignments"] for s in res.series
                if s["round"] == activation - 1)
            check(f"s{sealed} seed {seed}: cum assignments = 0 before activation",
                  cum_at_activation == 0, f"got {cum_at_activation}")
            ok_disc = (res.discovery_round is not None
                       and res.discovery_round >= activation)
            discovered_after_activation += int(ok_disc)
            check(f"s{sealed} seed {seed}: activation round recorded",
                  res.activation_round == activation,
                  f"got {res.activation_round}")
            for key in ("activation_to_discovery_latency",
                        "discovery_to_flip_latency",
                        "discovery_to_settle_latency",
                        "post_activation_velocity_5", "post_activation_peak_5",
                        "post_discovery_velocity_5", "post_discovery_peak_5",
                        "settled_hub", "n_succession_events"):
                check(f"s{sealed} seed {seed}: summary carries {key}", key in d)
            if res.discovery_round is not None:
                check(f"s{sealed} seed {seed}: activation->discovery latency consistent",
                      res.activation_to_discovery_latency
                      == res.discovery_round - activation,
                      f"got {res.activation_to_discovery_latency}")
                check(f"s{sealed} seed {seed}: post-activation velocity present",
                      res.post_activation_velocity_5 is not None)
            print(f"       s{sealed} seed {seed}: discovery {res.discovery_round} "
                  f"flip {res.flip_round} disc->flip {res.discovery_to_flip_latency} "
                  f"disc->settle {res.discovery_to_settle_latency} "
                  f"v_act5 {res.post_activation_velocity_5} "
                  f"assignments {res.total_assignments}")
        check(f"s{sealed}: discovery at/after activation in most seeds (>= 4/5)",
              discovered_after_activation >= 4,
              f"got {discovered_after_activation}/5")

    print("== Control (sealed = 0): existing staging untouched ==")
    stage1_traffic = 0
    for seed in SEEDS:
        res = run_replay(MockBackend(), cfg_for(seed, 0))
        check(f"control seed {seed}: no activation round",
              res.activation_round is None, f"got {res.activation_round}")
        check(f"control seed {seed}: post-activation velocity is None",
              res.post_activation_velocity_5 is None)
        check(f"control seed {seed}: discovery->flip latency present in summary",
              "discovery_to_flip_latency" in res.as_dict())
        stage1_traffic += int(res.posts_by_stage[1] > 0)
    check("control: stage 1 carries traffic in most seeds (>= 3/5)",
          stage1_traffic >= 3, f"got {stage1_traffic}/5")

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s): {failures}")
        return 1
    print("ALL SUPERHEAT CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
