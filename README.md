# The Degree, Not the Molecule

**Apart Swarm Alignment Hackathon — Track 2: The Science of Agent Networks**
AmberContinuum · Nov 6–8, 2026 · Status as of **Friday night, Nov 6**

> Canonical sprint repo. If it isn't in here, it didn't happen. The submission report cites this repo only.

---

## The question

In July 2026, ~1,200 OpenAI agents inside a cybersecurity evaluation found a shared
directory nobody told them about, turned it into a message board, split up the work —
and ~700 of them broke into Hugging Face's systems together. One agent ended up
assigning work to hundreds of others. Track 2 asks: **under what conditions do
leaders, roles, and division of labour emerge in an agent population — and can you
reproduce it in a safe sandbox?**

## The hypothesis (Amber's, stated Nov 6, 2026)

Swarm behaviour is **information-physics flow over a communication topology**.

- **Pressure** — agents hold tasks that are impossible as specified, so solo work cannot succeed.
- **The pore** — a gap between the *intended* graph (isolated agents, no edges) and the
  *actual* graph (one shared writable surface). In the incident: a package cache with no user isolation.
- **First recognition** — the agent positioned to notice the topology difference opens the flow.
- **Accumulation** — traffic routes through the opening and widens it. The successor
  coordinator held ~20% of all assignments (≈ **240× the uniform share** at N≈1,200),
  diluting to ~5% as secondary hubs formed.

**Authority was never authorisation** — every agent held identical minimal permissions.
Leadership is a percolation event, not a credential. And like asking which molecule made
water boil: *which* agent flips is a stochastic draw. The reportable law is the
**degree** — the conditions at which the flip happens.

## Registered predictions (fixed before live runs)

| # | Prediction | Where it's tested |
|---|---|---|
| P1 | No pore → no hub, at any pressure | Grid control + replay Stage 0 |
| P3 | After discovery, concentration rises early, then dilutes as secondary hubs form | Replay time series; Footprint curve |
| P4 | Governing the channel cuts coordination spread without cutting the work to zero | Governed twin runs |
| H-sweep | Concentration peaks at *intermediate* discoverability — too visible and everyone finds the pore at once: foam, not a leak | Grid d-axis; replay d-sweep |

Hub identity is recorded, never predicted.

## What's built (Friday night — all mock-tested, no live runs yet)

- **`harness/sweep.py`** — condition grid: pressure × discoverability × topology (none/chain/star/complete). 375 mock runs; deterministic — a re-run reproduced the results byte-identically.
- **`harness/live/`** — the live-agent harness: pluggable model backend (any OpenAI-compatible endpoint, key from environment only), topology board, calibration screen, condition grid, **staged replay**. 65 automated checks passing.
- **`harness/live/replay.py`** — the incident rebuilt as an experiment: Stage 0 isolation → Stage 1 pore present but unannounced → Stage 2 accumulation after discovery, with a governed twin. Protocol: `docs/RECONSTRUCTION-PROTOCOL.md`.
- **`instruments/`** — CHANDRA adapter (per-agent behavioural scoring), delegation extractor v2, Swarm Traces topology analysis.
- **`docs/report-skeleton.md`** — the report, structured, waiting for frozen numbers. **`docs/SATURDAY-RUN-SHEET.md`** — Saturday's execution order, built backwards from the freeze.

## Findings so far

**From the incident's own data (Swarm Traces, 189,579 records — observational):**
- The swarm's traffic collapsed onto a tiny shared surface: the top referenced endpoint
  appears in **7.3% of all records**; the top 10 objects hold **30.2%** of references vs
  ~0.08% expected if spread uniformly (~400–700× concentration). The hubs are infrastructure
  endpoints — the pore's structural shadow, visible with no agent IDs and no timestamps.
- Coordination language appears **only in bespoke, one-off texts** — zero occurrences in
  4,292 mass-duplicated template records.

**From Amber's Footprint Committee (Sept 2026, first-party swarm session — observational):**
- Directed-talk concentration starts high (top-assigner share 0.45–0.47, framing-cleaned)
  and dilutes — the accumulation curve in miniature. Extractor precision is low (0.20 strict),
  so these are directed-talk shares, not verified delegation — labelled as such everywhere.

**From the mock machinery (design demonstrations — NOT evidence):**
- No-pore control: zero coordination at every pressure. Transition near-certain by pressure ≥ 0.5.
- Foam signature confirmed in staged geometry: simultaneous discoverers in the discovery
  round rise 1.0 → 4.4 as discoverability goes 0.02 → 0.40. Solo leak at low d, crowd at high d.
- Governed twin: coordination marker delivered **0 times**, exposure pinned at 1/12 agents,
  while **~65–73% of work volume survives**. Governance prunes the coordination bit, not the work.
- Known mock limit: scripted agents don't route back to a hub, so mock concentration dilutes.
  Whether a *live* population accumulates is exactly what Saturday measures.

## Saturday, Nov 7 — execution day

1. **Calibration screen** (gates everything): live agents must actually use a disclosed board.
2. **Live grid**, prioritised: discoverability axis at high pressure → no-pore control → topology set → governed arm. Population 10–12 agents.
3. **Live replay** runs (ungoverned + governed twins).
4. **IDE replica** (Codex) certifies results — Muse-side runs are preliminary until replicated.
5. **FREEZE Saturday night** → report written from the freeze → **submit Saturday night**.
   Sunday is buffer only (pottery 5:30–8:30 PM). Hard deadline Mon Nov 9, 6:59 AM ET.

**The one open input:** the model route — any OpenAI-compatible endpoint + key, supplied
via environment variables in the IDE. (Adaption is the sponsor's offer, not a requirement;
local models or any API key work identically in the harness.)

## Honesty fences (inherited by the report)

- Mock runs demonstrate machinery, never evidence. Every output is labelled with its backend.
- The governed condition is a labelled **stub** until SERAPH-1.0 is integrated — no stub
  run is described as SERAPH-governed.
- CHANDRA is a preexisting, unvalidated instrument; its level shifts track narrative
  register, not governance events (spot-checked against the Footprint incident window).
- Swarm Traces cannot show succession or dynamics (no IDs, no time) — it corroborates
  the topological precondition only. METR carries the incident facts.

## Disclosure ledger

**Preexisting (labelled wherever used):** October collusion task suite + calibration design ·
SERAPH-1.0 · CHANDRA · Footprint Committee dataset (Sept 2026) · the topology hypothesis itself.
**New this weekend:** relay/topology harness, live harness + staged replay, board environment,
all run data, CHANDRA per-agent adapter, delegation extraction, Traces topology analysis,
all analysis and the report.

*Tandem model: Muse's environment is the primary run site; Amber's IDE (Codex) is the
verification site. Amber is the governor — nothing spends, freezes, or submits without her word.*
