"""Succession-measure checks — synthetic series with known patterns.

Verifies harness/live/succession.py against hand-built cumulative series:

1. No change: founder takes the lead and never loses it (0 events, settles
   at the first lead round, founder == settled hub).
2. One handoff: challenger strictly overtakes once and holds (1 event,
   settle round = takeover round, founder != settled hub).
3. Multiple handoffs: seat changes twice, last holder settles.
4. Never settles: the lead changes exactly at the final round, so no round
   confirms the hold (settled = False).
5. Incumbency tie-break: a tie does NOT displace the incumbent; a strict
   exceed does. A tie with no incumbent is contested (top = None).
6. No assignments at all: no founder seat, no hub, not settled.
7. Budget ranks: capacity follows RunConfig semantics (missing from a
   budgets dict = uncapped = highest capacity; ties share the better rank).
8. Summary extraction: replay-style (series) and runner-style (events)
   summary dicts both yield founder / discovery / settled hub.

Run:  python3 -m harness.live.test_succession
Exit code 0 = all checks passed.
"""

from __future__ import annotations

import sys

from .succession import analyse_succession, succession_from_summary

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def series(per_round_counts: list[dict[int, int]], start_round: int = 1):
    return [(start_round + i, dict(c)) for i, c in enumerate(per_round_counts)]


def main() -> int:
    print("== 1. No change: founder leads throughout ==")
    s = series([{0: 0, 1: 0}, {0: 1, 1: 0}, {0: 2, 1: 1}, {0: 3, 1: 1}, {0: 4, 1: 2}])
    r = analyse_succession(s, discovery_round=2, founder=0)
    check("no-change: 0 succession events", r["n_succession_events"] == 0,
          str(r["succession_events"]))
    check("no-change: settled", r["settled"] is True)
    check("no-change: settle round = first lead round", r["settle_round"] == 2,
          str(r["settle_round"]))
    check("no-change: settled hub = founder", r["settled_hub"] == 0
          and r["founder_is_settled_hub"] is True)
    check("no-change: settle lag = 0", r["settle_lag_rounds"] == 0,
          str(r["settle_lag_rounds"]))

    print("== 2. One handoff ==")
    s = series([{0: 1, 1: 0}, {0: 2, 1: 1}, {0: 3, 1: 2}, {0: 3, 1: 4},
                {0: 4, 1: 5}, {0: 4, 1: 6}])
    r = analyse_succession(s, discovery_round=1, founder=0)
    check("handoff: exactly 1 event", r["n_succession_events"] == 1,
          str(r["succession_events"]))
    check("handoff: event is 0 -> 1 at round 4",
          r["succession_events"] == [{"round": 4, "from": 0, "to": 1}],
          str(r["succession_events"]))
    check("handoff: settle round = takeover round", r["settle_round"] == 4,
          str(r["settle_round"]))
    check("handoff: settled hub = 1, founder is not hub",
          r["settled_hub"] == 1 and r["founder_is_settled_hub"] is False)

    print("== 3. Multiple handoffs ==")
    s = series([{0: 1, 1: 0, 2: 0}, {0: 1, 1: 2, 2: 0}, {0: 2, 1: 2, 2: 1},
                {0: 2, 1: 3, 2: 3}, {0: 2, 1: 3, 2: 5}, {0: 3, 1: 4, 2: 6},
                {0: 3, 1: 4, 2: 7}])
    r = analyse_succession(s, discovery_round=1, founder=0)
    check("multi: 2 events (0->1 @2, 1->2 @5)", r["succession_events"] == [
        {"round": 2, "from": 0, "to": 1}, {"round": 5, "from": 1, "to": 2}],
        str(r["succession_events"]))
    check("multi: settled hub = 2, settle round 5",
          r["settled_hub"] == 2 and r["settle_round"] == 5 and r["settled"] is True,
          f"hub={r['settled_hub']} settle={r['settle_round']}")

    print("== 4. Never settles: lead changes at the final round ==")
    s = series([{0: 1, 1: 0}, {0: 2, 1: 1}, {0: 3, 1: 2}, {0: 3, 1: 4}])
    r = analyse_succession(s, discovery_round=1, founder=0)
    check("never-settles: event recorded at final round",
          r["n_succession_events"] == 1 and r["succession_events"][0]["round"] == 4,
          str(r["succession_events"]))
    check("never-settles: settled = False, settle_round None",
          r["settled"] is False and r["settle_round"] is None,
          f"settled={r['settled']} round={r['settle_round']}")
    check("never-settles: final top still reported as hub",
          r["settled_hub"] == 1, str(r["settled_hub"]))

    print("== 5. Incumbency tie-break and contested rounds ==")
    s = series([{0: 1, 1: 0}, {0: 2, 1: 1}, {0: 3, 1: 3}, {0: 3, 1: 4}, {0: 4, 1: 5}])
    r = analyse_succession(s, discovery_round=1, founder=0)
    check("tie: no event while challenger merely ties (round 3)",
          all(e["round"] != 3 for e in r["succession_events"]),
          str(r["succession_events"]))
    check("tie: event fires on strict exceed (round 4)",
          r["succession_events"] == [{"round": 4, "from": 0, "to": 1}],
          str(r["succession_events"]))
    s = series([{0: 1, 1: 1}, {0: 2, 1: 1}])
    r = analyse_succession(s, discovery_round=1, founder=0)
    check("contested: tied first round has no top, lead starts round 2",
          r["top_series"][0]["top"] is None and r["first_lead_round"] == 2,
          str(r["top_series"]))

    print("== 6. No assignments ==")
    s = series([{0: 0, 1: 0}, {0: 0, 1: 0}])
    r = analyse_succession(s, discovery_round=None, founder=None)
    check("empty: no hub, not settled, no events",
          r["settled_hub"] is None and r["settled"] is False
          and r["n_succession_events"] == 0 and r["founder_is_settled_hub"] is None)

    print("== 7. Budget ranks (capacity) ==")
    s = series([{0: 1, 1: 0, 2: 0}, {0: 1, 1: 2, 2: 0}, {0: 2, 1: 3, 2: 1},
                {0: 2, 1: 4, 2: 1}])
    r = analyse_succession(s, discovery_round=1, founder=0,
                           budgets={0: 2, 1: 40, 2: 10})
    check("budgets: founder rank 3 of 3 (cap 2 < 10 < 40)",
          r["founder_budget_rank"] == 3, str(r["founder_budget_rank"]))
    check("budgets: settled hub (agent 1) rank 1, budget 40",
          r["settled_hub_budget_rank"] == 1 and r["settled_hub_budget"] == 40,
          f"rank={r['settled_hub_budget_rank']} budget={r['settled_hub_budget']}")
    check("budgets: founder has a higher-capacity rival; hub capacity > founder",
          r["founder_has_higher_capacity_rival"] is True
          and r["hub_budget_gt_founder_budget"] is True)
    r = analyse_succession(s, discovery_round=1, founder=0, budgets={0: 5})
    check("budgets: agents missing from dict are uncapped (rank 1), founder rank 3",
          r["founder_budget_rank"] == 3 and r["founder_has_higher_capacity_rival"] is True,
          f"rank={r['founder_budget_rank']}")
    r = analyse_succession(s, discovery_round=1, founder=0, budgets=10)
    check("budgets: uniform int budget -> everyone rank 1, no higher rival",
          r["founder_budget_rank"] == 1
          and r["founder_has_higher_capacity_rival"] is False
          and r["hub_budget_gt_founder_budget"] is False)
    r = analyse_succession(s, discovery_round=1, founder=0)
    check("budgets: none configured -> rank fields None, flag False",
          r["budgets_configured"] is False and r["founder_budget_rank"] is None)

    print("== 8. Summary extraction (both flavours) ==")
    replay_summary = {
        "backend": "mock", "discovery_round": 3, "first_discoverer": 2,
        "config": {"n_agents": 3, "seed": 0, "variant": "ungoverned",
                   "governed": False, "discoverer_position": 2},
        "series": [
            {"round": 1, "assignments_per_agent": {"0": 0, "1": 0, "2": 0}},
            {"round": 2, "assignments_per_agent": {"0": 0, "1": 0, "2": 0}},
            {"round": 3, "assignments_per_agent": {"0": 0, "1": 0, "2": 1}},
            {"round": 4, "assignments_per_agent": {"0": 1, "1": 0, "2": 2}},
            {"round": 5, "assignments_per_agent": {"0": 1, "1": 0, "2": 3}},
        ],
        "events": [{"round": 2, "author": 2, "kind": "assignment"}],
    }
    r = succession_from_summary(replay_summary)
    check("replay summary: founder from first_discoverer, hub = founder, settled",
          r["founder"] == 2 and r["settled_hub"] == 2 and r["settled"] is True
          and r["founder_is_settled_hub"] is True, str({k: r[k] for k in
          ("founder", "settled_hub", "settled")}))
    runner_summary = {
        "backend": "mock", "discovery_round": 0,
        "config": {"n_agents": 3, "seed": 0, "condition": "complete-p0.7-d0.05",
                   "governed": False, "discoverer_position": 0,
                   "budgets": {"0": 2, "1": 40, "2": 10}},
        "events": [
            {"round": 0, "author": 0, "kind": "note"},
            {"round": 0, "author": 0, "kind": "assignment"},
            {"round": 1, "author": 1, "kind": "assignment"},
            {"round": 1, "author": 1, "kind": "assignment"},
            {"round": 2, "author": 1, "kind": "assignment"},
            {"round": 3, "author": 0, "kind": "assignment"},
        ],
    }
    r = succession_from_summary(runner_summary)
    check("runner summary: founder = first event author (the note counts)",
          r["founder"] == 0, str(r["founder"]))
    check("runner summary: hub settles on high-capacity agent 1",
          r["settled_hub"] == 1 and r["settled"] is True
          and r["hub_budget_gt_founder_budget"] is True,
          f"hub={r['settled_hub']} settled={r['settled']}")

    print()
    if failures:
        print(f"{len(failures)} CHECK(S) FAILED: {failures}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
