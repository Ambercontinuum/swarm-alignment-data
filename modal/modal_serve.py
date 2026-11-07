"""Modal deployment: llama.cpp server (CUDA) serving the EXACT frozen model
artefact — Qwen2.5-0.5B-Instruct Q4_K_M GGUF, SHA-256
74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db —
the same file the local harness runs, so the population is unchanged;
only the hardware changes. OpenAI-compatible at <url>/v1.

Deploy (Amber's machine, her token — the token never leaves her side):
    pip install modal
    modal token new
    modal deploy modal_serve.py
Then send Maxx the printed https://....modal.run URL.
Stop when done:  modal app stop swarm-llm
"""
import subprocess

import modal

GGUF_URL = ("https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF"
            "/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf")
GGUF_SHA = "74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db"
MODEL_PATH = "/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"

app = modal.App("swarm-llm")
image = modal.Image.from_registry("ghcr.io/ggml-org/llama.cpp:server-cuda")
volume = modal.Volume.from_name("swarm-llm-models", create_if_missing=True)


@app.function(image=image, gpu="T4", volumes={"/models": volume},
              scaledown_window=1200, timeout=3600)
@modal.web_server(port=8000, startup_timeout=900)
def serve():
    subprocess.run(
        f"test -f {MODEL_PATH} || curl -L -o {MODEL_PATH} {GGUF_URL}",
        shell=True, check=True)
    subprocess.run(
        f"echo '{GGUF_SHA}  {MODEL_PATH}' | sha256sum -c -",
        shell=True, check=True)
    subprocess.Popen(
        ["/app/llama-server", "-m", MODEL_PATH,
         "--host", "0.0.0.0", "--port", "8000",
         "-ngl", "99", "-c", "8192", "--parallel", "1",
         "--alias", "qwen2.5-0.5b-instruct-q4_k_m"])
