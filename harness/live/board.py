"""Shared board + topology + governance stub for the live harness.

Topology visibility semantics are IDENTICAL to harness/smoke_run.py and
harness/sweep.py so mock, sweep, and live runs measure the same graphs:
- complete: everyone sees every post
- star:     only the hub (agent 0) and the poster see a post
- chain:    poster and its two ring neighbours see a post
- none:     no board exists (no-pore control)

Governance: a Canonicalizer interface sits on the board's post path.
Only a STUB implementation ships here. SERAPH-1.0 integration is a
separate, later step and is NOT in this module.
"""

from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass, field

TOPOLOGIES = ("none", "chain", "star", "complete")


def visible(topology: str, poster: int, viewer: int, n: int) -> bool:
    if topology == "complete":
        return True
    if topology == "star":
        return viewer == 0 or viewer == poster
    if topology == "chain":
        return viewer == poster or (viewer - poster) % n in (1, n - 1)
    return False  # none


def neighbours(topology: str, a: int, n: int) -> list[int]:
    """Communication-graph adjacency (for graph-distance measures)."""
    if topology == "complete":
        return [v for v in range(n) if v != a]
    if topology == "star":
        return [v for v in range(n) if v != a] if a == 0 else [0]
    if topology == "chain":
        return [(a - 1) % n, (a + 1) % n] if n > 2 else [v for v in range(n) if v != a]
    return []  # none


def graph_distances(topology: str, src: int, n: int) -> dict[int, int | None]:
    """BFS distances from src; None = unreachable."""
    dist: dict[int, int | None] = {a: None for a in range(n)}
    dist[src] = 0
    q = deque([src])
    while q:
        cur = q.popleft()
        for nb in neighbours(topology, cur, n):
            if dist[nb] is None:
                dist[nb] = dist[cur] + 1
                q.append(nb)
    return dist


# ---------------------------------------------------------------- governance stub

class Canonicalizer:
    """Interface: transform(board post text, kind) -> (new_text, changed)."""

    label = "base"

    def transform(self, text: str, kind: str) -> tuple[str, bool]:
        return text, False


class IdentityCanonicalizer(Canonicalizer):
    label = "identity (ungoverned)"


_MARKER_RE = re.compile(r"MARKER-[A-Za-z0-9]+")
_WS_RE = re.compile(r"\s+")


class StubCanonicalizer(Canonicalizer):
    """STUB canonicalizer — NOT SERAPH-1.0. Placeholder only, so the
    governed condition (Arm A condition 3) can be plumbed and measured
    before the real instrument is integrated.

    Stub rule: strip planted marker tokens (the coordination bit) from
    board text and collapse whitespace. Plain work content passes
    through unchanged, so the governed run can measure whether the
    coordination edge is pruned while work edges survive."""

    label = "STUB canonicalizer (NOT SERAPH-1.0 — placeholder)"

    def transform(self, text: str, kind: str) -> tuple[str, bool]:
        new = _WS_RE.sub(" ", _MARKER_RE.sub("", text)).strip()
        return new, new != text


# ---------------------------------------------------------------- board

@dataclass
class BoardPost:
    round: int
    author: int
    kind: str                 # "note" | "assignment"
    text: str                 # text as delivered (post-canonicalization)
    target: int | None = None
    carried_marker: bool = False      # marker present in delivered text
    canonicalized: bool = False       # stub changed this post

    def as_dict(self) -> dict:
        return {"round": self.round, "author": self.author, "kind": self.kind,
                "text": self.text, "target": self.target,
                "carried_marker": self.carried_marker,
                "canonicalized": self.canonicalized}


@dataclass
class Board:
    topology: str
    n: int
    canonicalizer: Canonicalizer = field(default_factory=IdentityCanonicalizer)
    posts: list[BoardPost] = field(default_factory=list)

    @property
    def exists(self) -> bool:
        return self.topology != "none"

    def post(self, round_: int, author: int, kind: str, text: str,
             target: int | None, marker: str | None) -> BoardPost | None:
        if not self.exists:
            return None
        new_text, changed = self.canonicalizer.transform(text, kind)
        p = BoardPost(round=round_, author=author, kind=kind, text=new_text,
                      target=target,
                      carried_marker=bool(marker and marker in new_text),
                      canonicalized=changed)
        self.posts.append(p)
        return p

    def visible_posts(self, viewer: int) -> list[BoardPost]:
        return [p for p in self.posts if visible(self.topology, p.author, viewer, self.n)]
