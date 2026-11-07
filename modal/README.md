# Modal endpoint — Amber's 3 steps (about 5 minutes, whenever)

1. In your IDE terminal: `python -m pip install --upgrade modal`
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

## Python detection error after image build

The upstream server image declares `/app/llama-server` as its entrypoint.
Modal needs an entrypoint that lets its Python runtime start. Adding Python
alone does not remove the inherited server entrypoint.

The deployment now clears it during base-image setup with
`setup_dockerfile_commands=["ENTRYPOINT []"]`. A CPU-only image build step
checks Python 3.12 and the executable server binary. The function still starts
the server explicitly after validating the frozen GGUF hash.

Retry from this directory:

```powershell
python -m pip install --upgrade modal
python -m modal deploy modal_serve.py
```

The base setup change creates a different image definition. Local source checks
are not proof of remote build or endpoint readiness. If detection still fails,
retain the full new build log, image ID, `python -m modal --version` output and
workspace Image Builder version for diagnosis.

Sources: https://modal.com/docs/guide/existing-images and
https://github.com/ggml-org/llama.cpp/blob/master/.devops/cuda.Dockerfile
