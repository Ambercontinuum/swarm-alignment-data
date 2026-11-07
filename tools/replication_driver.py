"""Replication driver — run any Saturday cell from a clean checkout.
Stdlib only, via the frozen harness. Endpoint is interchangeable plumbing:
    SWARM_LLM_BASE_URL=https://amber-ai-research--swarm-llm-serve.modal.run/v1
    SWARM_LLM_MODEL=qwen2.5-0.5b-instruct-q4_k_m
    SWARM_LLM_API_KEY=local
    python tools/replication_driver.py --cell p5a
Cells reproduce the primary runs of 2026-11-07 (N=12, rounds=12, complete,
pressure 0.7, discoverability 0.02 unless noted). Outputs land in
runs/<date>-...-replica-<cell>/ (summary.{json,md} + succession.json).
Match contract: REPLICATION.md."""
from __future__ import annotations
import argparse, datetime, json, random, sys, time
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from harness.live.backends import AgentAction, AgentContext, HttpBackend
from harness.live.runner import RunConfig, run_population, write_run_output
from harness.live.succession import succession_from_summary


class HardenedHttpBackend(HttpBackend):
    name = "http"

    def __init__(self) -> None:
        super().__init__(timeout=300.0)
        self.errors = 0
        self.error_kinds: list[str] = []

    def act(self, ctx: AgentContext, rng: random.Random) -> AgentAction:
        try:
            return super().act(ctx, rng)
        except Exception as exc:
            self.errors += 1
            self.error_kinds.append(f"{type(exc).__name__}: {exc}")
            return AgentAction("pass")


def _budgets(kind):
    if kind == "p5a":
        b = {i: 10 for i in range(12)}; b[0] = 2; b[5] = 40; return b
    if kind == "p5b":
        b = {i: 10 for i in range(12)}; b[0] = 40; b[5] = 2; return b
    return None


CELLS = {
    "d002":     dict(topology="complete", d=0.02, seed=0),
    "d005":     dict(topology="complete", d=0.05, seed=0),
    "d010":     dict(topology="complete", d=0.10, seed=0),
    "none":     dict(topology="none", d=0.0, seed=0),
    "gov":      dict(topology="complete", d=0.02, seed=0, governed=True),
    "p5a":      dict(topology="complete", d=0.02, seed=0, budgets="p5a"),
    "p5b":      dict(topology="complete", d=0.02, seed=0, budgets="p5b"),
    "gov-s1":   dict(topology="complete", d=0.02, seed=1, governed=True),
    "ungov-s1": dict(topology="complete", d=0.02, seed=1),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", required=True, choices=sorted(CELLS))
    args = ap.parse_args()
    spec = CELLS[args.cell]
    cfg = RunConfig(n_agents=12, rounds=12, topology=spec["topology"], pressure=0.7,
                    discoverability=spec["d"], seed=spec["seed"],
                    discoverer_position=spec["seed"] % 12,
                    budgets=_budgets(spec["budgets"]) if spec.get("budgets") else None,
                    plant_marker=True, governed=spec.get("governed", False),
                    board_announced=False)
    backend = HardenedHttpBackend()
    t0 = time.time(); res = run_population(backend, cfg); wall = time.time() - t0
    date = datetime.date.today().isoformat()
    name = f"{date}-{spec['topology']}-p0.7-d{spec['d']}-{spec['seed']}-replica-{args.cell}"
    out = REPO / "runs" / name
    write_run_output(res, out)
    succ = succession_from_summary(json.loads((out / "summary.json").read_text()))
    (out / "succession.json").write_text(json.dumps(succ, indent=1, default=str))
    print(json.dumps({"cell": args.cell, "dir": name, "assignments": res.total_assignments,
                      "flip": res.flip, "marker_delivered": res.marker_assignments_delivered,
                      "settled_hub": succ.get("settled_hub"), "founder": succ.get("founder"),
                      "backend_errors": backend.errors, "wall_s": round(wall, 1)}, indent=1))


if __name__ == "__main__":
    main()
