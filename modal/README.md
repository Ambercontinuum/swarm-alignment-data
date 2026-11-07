# Modal endpoint — Amber's 3 steps (about 5 minutes, whenever)

1. In your IDE terminal: `pip install modal`
2. `modal token new` — opens your browser, log in as you. The token stays
   on your machine; Maxx never sees it.
3. `modal deploy modal_serve.py` (from this folder) — it prints a URL like
   https://ambercontinuum--swarm-llm-serve.modal.run — send Maxx that URL.

Then Maxx health-checks it, runs a 5-call smoke, and points the wave
drivers at it with env vars only. Same GGUF file (hash-verified inside the
container before serving), so the frozen population is unchanged.

Cost: T4 ≈ $0.59/GPU-hour; the $80 credit covers ~130 hours. We need ~3.
When the sprint ends: `modal app stop swarm-llm`.

Fallback if the image tag fails to pull: change `server-cuda` to
`full-cuda` in modal_serve.py and redeploy.
