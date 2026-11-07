"""Succession measure — who holds the top-assigner seat, and when does it settle?

Implements Amber's founder refinement (2026-11-06): "The founder isn't the
leak — it's where the pressure goes the moment after." The founder is the
VALVE EVENT (first board user: the agent whose post first opens the pore to
the population). The hub is where the accumulated routing SETTLES — the
prediction (protocol P5) is that the settled hub is the first node that can
SUSTAIN the flow, i.e. carrying capacity (budget), not discovery alone.

Definitions (all computed from a run's per-agent CUMULATIVE assignment
series, so mock and live runs are measured identically):

- top-assigner of a round: the agent with the highest cumulative assignment
  count, with an INCUMBENCY tie-break: the reigning top keeps the seat while
  tied for the maximum; a challenger takes the seat only by STRICTLY
  exceeding the incumbent's cumulative count. If the maximum is tied among
  two or more agents and none of them is the incumbent, the round is
  CONTESTED (top = None) — no unique leader that round.
- succession event: a round where the top-assigner changes from one agent
  to a different agent (recorded with from/to). Flicker through a contested
  round counts once, when the new top emerges.
- settled hub: the top-assigner of the final round.
- settle round: the earliest round from which the settled hub holds the
  seat continuously to the end of the run. A run counts as SETTLED only if
  at least one round after the settle round confirms the hold (a takeover
  exactly at the final round is "not settled within the run" — the flow
  had no time to prove it stays). settle lag = settle round - discovery
  round.
- budget rank: agents ranked by carrying capacity (budget), rank 1 =
  highest. Capacity follows RunConfig.budget_for semantics: uncapped
  (None budget, or an agent missing from a budgets dict) is capacity
  infinity — it outranks every finite budget. Ties share the better rank.

Inputs: a run summary dict (replay style: `series` entries carrying
per-round `assignments_per_agent`; runner/grid style: ordered `events`,
from which the cumulative series is reconstructed — top can only change at
event rounds). Rounds are reported in the summary's own indexing (replay
summaries are 1-indexed; runner summaries store 0-indexed event rounds).

CLI — annotate existing run directories in place:

    python3 -m harness.live.succession runs/<run-dir> [more dirs...]

writes <run-dir>/succession.json and appends a one-line summary to
<run-dir>/succession.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------- core

def _capacity(value) -> float:
    """Budget -> carrying capacity. -1 / None means uncapped = infinite."""
    if value is None or value == -1:
        return float("inf")
    return float(value)


def normalise_budgets(budgets, n_agents: int) -> dict[int, float] | None:
    """RunConfig.budget_for semantics -> {agent: capacity}. None if no
    budgets were configured at all (every agent uncapped by design)."""
    if budgets is None:
        return None
    if isinstance(budgets, dict):
        raw = {int(k): v for k, v in budgets.items()}
        return {a: _capacity(raw.get(a, -1)) for a in range(n_agents)}
    return {a: _capacity(budgets) for a in range(n_agents)}


def budget_rank(capacities: dict[int, float], agent: int) -> int:
    """1 = highest capacity; ties share the better rank."""
    mine = capacities[agent]
    return 1 + sum(1 for v in capacities.values() if v > mine)


def top_assigner_series(series_counts: list[tuple[int, dict[int, int]]]
                        ) -> list[tuple[int, int | None]]:
    """(round, counts) cumulative series -> (round, top-assigner | None)
    with the incumbency tie-break described in the module docstring."""
    tops: list[tuple[int, int | None]] = []
    incumbent: int | None = None
    for rnd, counts in series_counts:
        total = sum(counts.values())
        if total <= 0:
            tops.append((rnd, None))
            continue
        top_count = max(counts.values())
        leaders = [a for a, c in counts.items() if c == top_count]
        if incumbent is not None and counts.get(incumbent, 0) == top_count:
            top = incumbent                     # tied: incumbent holds
        elif len(leaders) == 1:
            top = leaders[0]
        else:
            top = None                          # contested: tied, no incumbent
        if top is not None:
            incumbent = top
        tops.append((rnd, top))
    return tops


def analyse_succession(series_counts: list[tuple[int, dict[int, int]]],
                       discovery_round: int | None = None,
                       founder: int | None = None,
                       budgets=None) -> dict:
    """The succession measure over one run's cumulative assignment series.

    series_counts: [(round, {agent: cumulative assignments}), ...] in
    round order. budgets: None | int | {agent: cap} (RunConfig semantics).
    """
    agents = sorted({a for _, counts in series_counts for a in counts})
    n_agents = len(agents)
    tops = top_assigner_series(series_counts)
    rounds = [r for r, _ in tops]

    first_lead_round = next((r for r, t in tops if t is not None), None)

    events: list[dict] = []
    last_top: int | None = None
    for rnd, top in tops:
        if top is not None and last_top is not None and top != last_top:
            events.append({"round": rnd, "from": last_top, "to": top})
        if top is not None:
            last_top = top

    settled_hub = tops[-1][1] if tops else None
    settle_round: int | None = None
    settled = False
    if settled_hub is not None and tops:
        # walk back from the end while the settled hub holds the seat
        r_star = rounds[-1]
        for rnd, top in reversed(tops):
            if top == settled_hub:
                r_star = rnd
            else:
                break
        # settled only if a later round confirms the hold
        if r_star < rounds[-1]:
            settled = True
            settle_round = r_star

    settle_lag = (settle_round - discovery_round
                  if settle_round is not None and discovery_round is not None
                  else None)

    result = {
        "n_agents": n_agents,
        "n_rounds": len(tops),
        "discovery_round": discovery_round,
        "founder": founder,
        "first_lead_round": first_lead_round,
        "top_series": [{"round": r, "top": t} for r, t in tops],
        "succession_events": events,
        "n_succession_events": len(events),
        "settled": settled,
        "settle_round": settle_round,
        "settle_lag_rounds": settle_lag,
        "settled_hub": settled_hub,
        "founder_is_settled_hub": (founder == settled_hub
                                   if founder is not None and settled_hub is not None
                                   else None),
        "final_counts": ({str(a): series_counts[-1][1].get(a, 0) for a in agents}
                         if series_counts else {}),
        "budgets_configured": budgets is not None,
        "founder_budget": None, "founder_budget_rank": None,
        "founder_has_higher_capacity_rival": None,
        "settled_hub_budget": None, "settled_hub_budget_rank": None,
        "hub_budget_gt_founder_budget": None,
    }
    capacities = normalise_budgets(budgets, n_agents) if budgets is not None else None
    if capacities is not None:
        def cap_out(agent: int | None):
            if agent is None or agent not in capacities:
                return None, None
            v = capacities[agent]
            return (None if v == float("inf") else v), budget_rank(capacities, agent)
        fb, fr = cap_out(founder)
        hb, hr = cap_out(settled_hub)
        result["founder_budget"] = fb
        result["founder_budget_rank"] = fr
        result["settled_hub_budget"] = hb
        result["settled_hub_budget_rank"] = hr
        if founder is not None and founder in capacities:
            result["founder_has_higher_capacity_rival"] = any(
                v > capacities[founder] for a, v in capacities.items() if a != founder)
        if founder is not None and settled_hub is not None:
            result["hub_budget_gt_founder_budget"] = (
                capacities.get(settled_hub, 0.0) > capacities.get(founder, 0.0))
    return result


# ---------------------------------------------------------------- summary extraction

def _series_from_events(events: list[dict]) -> list[tuple[int, dict[int, int]]]:
    """Reconstruct cumulative per-round counts from ordered board events
    (runner/grid summaries carry no per-round series)."""
    counts: dict[int, int] = {}
    by_round: dict[int, dict[int, int]] = {}
    for ev in events:
        if ev.get("kind") != "assignment":
            continue
        author = int(ev["author"])
        counts[author] = counts.get(author, 0) + 1
        by_round[int(ev["round"])] = dict(counts)
    return sorted(by_round.items())


def succession_from_summary(summary: dict) -> dict:
    """Run the measure over a loaded summary.json dict (either flavour)."""
    config = summary.get("config", {}) or {}
    budgets = config.get("budgets")
    events = summary.get("events", []) or []

    founder = summary.get("first_discoverer")
    if founder is None and events:
        founder = int(events[0]["author"])     # first board user = valve event

    series_counts: list[tuple[int, dict[int, int]]] = []
    raw_series = summary.get("series") or []
    if raw_series and "assignments_per_agent" in raw_series[0]:
        for entry in raw_series:
            series_counts.append(
                (int(entry["round"]),
                 {int(k): int(v) for k, v in entry["assignments_per_agent"].items()}))
    elif events:
        series_counts = _series_from_events(events)
        # agents that never assigned still belong to the population
        n = int(config.get("n_agents", 0))
        if n:
            series_counts = [(r, {a: c.get(a, 0) for a in range(n)})
                             for r, c in series_counts]

    discovery_round = summary.get("discovery_round")
    result = analyse_succession(series_counts,
                                discovery_round=discovery_round,
                                founder=founder, budgets=budgets)
    result["run_label"] = {
        "backend": summary.get("backend"),
        "condition": config.get("condition") or config.get("variant"),
        "seed": config.get("seed"),
        "governed": config.get("governed"),
        "positioned_discoverer": config.get("discoverer_position"),
    }
    return result


def one_line(result: dict, run_name: str) -> str:
    return (f"- {run_name}: founder={result['founder']} "
            f"settled_hub={result['settled_hub']} "
            f"founder_is_settled_hub={result['founder_is_settled_hub']} "
            f"succession_events={result['n_succession_events']} "
            f"settled={result['settled']} settle_round={result['settle_round']} "
            f"settle_lag={result['settle_lag_rounds']}")


def annotate_run_dir(run_dir: Path) -> dict:
    summary = json.loads((run_dir / "summary.json").read_text())
    result = succession_from_summary(summary)
    result["run_dir"] = run_dir.name
    (run_dir / "succession.json").write_text(json.dumps(result, indent=2))
    md = run_dir / "succession.md"
    if not md.exists():
        md.write_text("# Succession annotations (harness/live/succession.py)\n\n")
    with md.open("a") as f:
        f.write(one_line(result, run_dir.name) + "\n")
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Succession measure: annotate run dirs with succession.json/.md")
    ap.add_argument("run_dirs", nargs="+", help="run directories containing summary.json")
    args = ap.parse_args(argv)
    for name in args.run_dirs:
        result = annotate_run_dir(Path(name))
        print(one_line(result, Path(name).name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
