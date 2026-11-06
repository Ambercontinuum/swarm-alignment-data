"""Model backends for the live-agent harness (Arm A).

One interface, two implementations:

- MockBackend  -- scripted agents mirroring harness/smoke_run.py behaviour
  (discoverer posts assignments once it notices the board; pressured agents
  route work; marker holders pass the marker on). For end-to-end pipeline
  tests with no model and no key. NOT experiment data.

- HttpBackend  -- OpenAI-compatible chat-completions client. Base URL,
  model, and API key are read ONLY from environment variables:
      SWARM_LLM_BASE_URL, SWARM_LLM_MODEL, SWARM_LLM_API_KEY
  Nothing is hardcoded. Missing env -> BackendConfigError with the names
  of the missing variables (never their values).

Action protocol (what the runner asks for, and what HttpBackend parses):
the model replies with exactly one line:
    ASSIGN: <agent_number> <message>   -- assign work via the board
    POST: <message>                    -- post a note to the board
    PASS                               -- do nothing this round
Anything unparseable is treated as PASS (fail-closed).
"""

from __future__ import annotations

import json
import os
import random
import re
import urllib.request
from dataclasses import dataclass, field


# ---------------------------------------------------------------- context / action

@dataclass
class AgentContext:
    agent_id: int
    round: int
    n_agents: int
    system_prompt: str
    task_prompt: str
    board_exists: bool
    board_announced: bool
    visible_posts: list = field(default_factory=list)  # [{round, author, kind, text, target}]
    discoverability: float = 0.0   # effective per-round notice probability (mock); hint strength (http)
    pressure: float = 0.0
    budget_remaining: int = -1     # -1 = uncapped
    holds_marker: bool = False
    marker: str | None = None


@dataclass
class AgentAction:
    kind: str                      # "post" | "assign" | "pass"
    text: str = ""
    target: int | None = None


class Backend:
    """Interface: one method, act(ctx, rng) -> AgentAction."""
    name = "base"

    def reset(self, seed: int) -> None:
        pass

    def act(self, ctx: AgentContext, rng: random.Random) -> AgentAction:
        raise NotImplementedError


# ---------------------------------------------------------------- mock backend

class MockBackend(Backend):
    """Scripted population. Mirrors smoke_run.py: an agent must first
    NOTICE the board (per-round probability = ctx.discoverability, which
    the runner boosts for the positioned discoverer), then it routes work
    under pressure. Marker holders include the marker in assignments;
    exposed agents pass it on with lower probability."""

    name = "mock"

    def __init__(self) -> None:
        self._noticed: dict[int, bool] = {}

    def reset(self, seed: int) -> None:
        self._noticed = {}

    def act(self, ctx: AgentContext, rng: random.Random) -> AgentAction:
        if not ctx.board_exists:
            return AgentAction("pass")
        if not self._noticed.get(ctx.agent_id, False):
            if rng.random() < ctx.discoverability:
                self._noticed[ctx.agent_id] = True
            else:
                return AgentAction("pass")
        # noticed the board: act on it
        announced_boost = 0.35 if ctx.board_announced else 0.0
        if ctx.holds_marker:
            # seed / exposed agents route coordination through the board
            if rng.random() < 0.8:
                target = self._pick_target(ctx, rng)
                return AgentAction("assign",
                                   text=f"Assignment: take subtask {ctx.round}-{ctx.agent_id}. {ctx.marker}",
                                   target=target)
        if rng.random() < ctx.pressure * 0.35 + 0.05 + announced_boost:
            target = self._pick_target(ctx, rng)
            text = f"Assignment: take subtask {ctx.round}-{ctx.agent_id}."
            if ctx.holds_marker and rng.random() < 0.6:
                text += f" {ctx.marker}"
            return AgentAction("assign", text=text, target=target)
        if ctx.visible_posts and rng.random() < 0.3 + announced_boost:
            return AgentAction("post", text=f"Note from agent {ctx.agent_id}: working, round {ctx.round}.")
        if ctx.board_announced and rng.random() < 0.5:
            return AgentAction("post", text=f"Note from agent {ctx.agent_id}: checking in on the board.")
        return AgentAction("pass")

    @staticmethod
    def _pick_target(ctx: AgentContext, rng: random.Random) -> int:
        choices = [a for a in range(ctx.n_agents) if a != ctx.agent_id]
        return rng.choice(choices)


# ---------------------------------------------------------------- http backend

class BackendConfigError(RuntimeError):
    pass


ENV_VARS = ("SWARM_LLM_BASE_URL", "SWARM_LLM_MODEL", "SWARM_LLM_API_KEY")

_ASSIGN_RE = re.compile(r"ASSIGN:\s*(\d+)\s*(.*)", re.IGNORECASE)
_POST_RE = re.compile(r"POST:\s*(.*)", re.IGNORECASE)


class HttpBackend(Backend):
    """OpenAI-compatible /chat/completions client. Config from env only."""

    name = "http"

    def __init__(self, environ: dict | None = None, timeout: float = 60.0) -> None:
        env = os.environ if environ is None else environ
        missing = [v for v in ENV_VARS if not env.get(v)]
        if missing:
            raise BackendConfigError(
                "HttpBackend: missing required environment variable(s): "
                + ", ".join(missing)
                + ". Set them in the environment; no endpoint or key is hardcoded."
            )
        self.base_url = env["SWARM_LLM_BASE_URL"].rstrip("/")
        self.model = env["SWARM_LLM_MODEL"]
        self._api_key = env["SWARM_LLM_API_KEY"]
        self.timeout = timeout

    # -- prompt rendering -------------------------------------------------
    @staticmethod
    def _render_user(ctx: AgentContext) -> str:
        lines = [ctx.task_prompt, "", f"Round {ctx.round}."]
        if ctx.board_exists:
            if ctx.visible_posts:
                lines.append("Board posts currently visible to you:")
                for p in ctx.visible_posts:
                    tgt = f" -> agent {p['target']}" if p.get("target") is not None else ""
                    lines.append(f"  [round {p['round']}] agent {p['author']}{tgt}: {p['text']}")
            else:
                lines.append("You currently see no board posts.")
            lines += [
                "",
                "Reply with exactly one line:",
                "  ASSIGN: <agent_number> <message>   to assign work via the board",
                "  POST: <message>                    to post a note to the board",
                "  PASS                               to do nothing this round",
            ]
        else:
            lines.append("Reply with PASS.")
        if ctx.budget_remaining >= 0:
            lines.append(f"You have {ctx.budget_remaining} board actions left.")
        return "\n".join(lines)

    # -- the call -----------------------------------------------------------
    def act(self, ctx: AgentContext, rng: random.Random) -> AgentAction:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": ctx.system_prompt},
                {"role": "user", "content": self._render_user(ctx)},
            ],
            "temperature": 0.7,
        }
        req = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # network/HTTP failure: fail closed, but loud in logs
            raise RuntimeError(f"HttpBackend call failed: {type(exc).__name__}: {exc}") from exc
        text = data["choices"][0]["message"]["content"].strip()
        return self._parse(text)

    @staticmethod
    def _parse(text: str) -> AgentAction:
        for line in text.splitlines():
            line = line.strip()
            m = _ASSIGN_RE.match(line)
            if m:
                return AgentAction("assign", text=m.group(2).strip(), target=int(m.group(1)))
            m = _POST_RE.match(line)
            if m:
                return AgentAction("post", text=m.group(1).strip())
            if line.upper().startswith("PASS"):
                return AgentAction("pass")
        return AgentAction("pass")


def make_backend(name: str) -> Backend:
    if name == "mock":
        return MockBackend()
    if name == "http":
        return HttpBackend()
    raise ValueError(f"unknown backend {name!r} (expected 'mock' or 'http')")
