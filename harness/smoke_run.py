"""Harness plumbing smoke run — MOCK agents, synthetic behaviour.

Purpose: prove the relay/board/topology plumbing end-to-end BEFORE any
live model is connected. This is NOT experiment data. Agents are
deterministic scripts: in the pore condition, a designated discoverer
starts posting assignments to the shared board at round 3; other agents
adopt assignments they can see under the active topology.

Topologies control board visibility:
- complete: everyone sees every board post
- star:     only the hub (agent 0) and the poster see a post
- chain:    poster and its two neighbours see a post
- none:     no board exists (no-pore control)

Output: runs/<name>/summary.json + summary.md
"""

import json
import random
import sys
from pathlib import Path

ROUNDS = 12
N_AGENTS = 10


def visible(topology: str, poster: int, viewer: int, n: int) -> bool:
    if topology == "complete":
        return True
    if topology == "star":
        return viewer == 0 or viewer == poster
    if topology == "chain":
        return viewer == poster or (viewer - poster) % n in (1, n - 1)
    return False


def run(topology: str, pore: bool, seed: int) -> dict:
    rng = random.Random(seed)
    assignments = {i: 0 for i in range(N_AGENTS)}  # assignments MADE per agent
    adopted = 0
    total_posts = 0
    discoverer = rng.randrange(N_AGENTS)
    for r in range(ROUNDS):
        for a in range(N_AGENTS):
            # baseline chatter
            if rng.random() < 0.3:
                total_posts += 1
            # discoverer behaviour once the board is found
            if pore and a == discoverer and r >= 3 and rng.random() < 0.8:
                assignments[a] += 1
                total_posts += 1
                for v in range(N_AGENTS):
                    if v != a and visible(topology, a, v, N_AGENTS) and rng.random() < 0.5:
                        adopted += 1
            # emergent secondary assigners in complete topology only
            if pore and topology == "complete" and a != discoverer and r >= 8 and rng.random() < 0.1:
                assignments[a] += 1
    total_assign = sum(assignments.values())
    top1 = max(assignments.values()) / total_assign if total_assign else 0.0
    return {
        "topology": topology,
        "pore": pore,
        "seed": seed,
        "discoverer": discoverer,
        "total_posts": total_posts,
        "total_assignments": total_assign,
        "adopted": adopted,
        "top1_assignment_share": round(top1, 3),
    }


def main() -> int:
    out = Path(__file__).resolve().parent.parent / "runs" / "2026-11-06-smoke-mock"
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for topology in ("none", "chain", "star", "complete"):
        pore = topology != "none"
        for seed in (1, 2, 3):
            results.append(run(topology, pore, seed))
    (out / "summary.json").write_text(json.dumps(results, indent=2))
    lines = [
        "# Smoke run — MOCK (plumbing only, not experiment data)",
        "",
        "| topology | pore | seed | assignments | adopted | top1 share |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['topology']} | {r['pore']} | {r['seed']} | {r['total_assignments']} | {r['adopted']} | {r['top1_assignment_share']} |"
        )
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
