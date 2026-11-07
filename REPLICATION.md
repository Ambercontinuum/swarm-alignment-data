# Replication — how a second environment certifies these results

Tandem semantics: the primary environment's outputs are **preliminary**
until an independent run in the operator's IDE reproduces them. This file
is the whole contract; the driver is `tools/replication_driver.py`.

## Setup (5 minutes, stdlib only — no pip installs beyond a model server)

1. Clone this repo.
2. Point the harness at any OpenAI-compatible endpoint serving the frozen
   model artefact (Qwen2.5-0.5B-Instruct Q4_K_M GGUF, SHA-256
   `74a4da8c…a9db`):
   - the shared Modal endpoint (fast; same serving stack as the Saturday
     Modal wave), or
   - a local `llama-server` with the identical GGUF (tests the stack too).
3. Export:
   `SWARM_LLM_BASE_URL=<endpoint>/v1`,
   `SWARM_LLM_MODEL=qwen2.5-0.5b-instruct-q4_k_m`,
   `SWARM_LLM_API_KEY=local` (dummy for local/Modal; never a real key here).

## Run

`python tools/replication_driver.py --cell <name>` — cells: `d002 d005
d010 none gov p5a p5b gov-s1 ungov-s1`. Each writes
`runs/<date>-...-replica-<cell>/summary.{json,md}` + `succession.json`
and prints a one-line result. A cell takes ~4–5 min on the Modal endpoint,
~40–110 min on a CPU-local server (grown-board regime).

## What "match" means

- **Mock layers** (sweeps, replay demos): byte-identical outputs expected.
- **Live layers**: sampling is stochastic and serving stacks differ
  (llama.cpp build/CUDA vs CPU), so exact counts are NOT the target. A
  cell **certifies** when the qualitative outcomes match the primary run —
  flip yes/no, hub identity class (founder vs successor), marker delivered
  0 vs >0, control cells exactly 0/0 — and concentration (top-1 share ×N)
  lands in the same regime (order of magnitude, same side of the 4.2×
  flip criterion).
- **Calibration**: the screen itself (`harness.live.calibration`,
  PASS = ≥50% board users on the disclosed board) must PASS in the
  replica environment before its live cells certify anything.

Disagreements are reported, not averaged away: if a replica cell flips a
qualitative outcome, both records stay in the repo and the report says so.
