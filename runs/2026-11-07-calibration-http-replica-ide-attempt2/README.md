# IDE replica calibration - November 7, 2026

**PASS: 10/10 agents used the disclosed board; threshold 50%.**
Completed attempt: 120 requests, 61 posts, 56 assignments, no backend exceptions,
112.0 seconds. This is an independently executed IDE-client screen using the shared
Modal endpoint, not an independent model-weight or serving-hardware replication.
A calibration pass does not certify any main-cell result.

## What ran

Source: commit `9c9794548d6e51427c02257f10ff27e154c50761`.
The existing HttpBackend and run_population were used with the stock calibration
configuration: 10 agents, 12 rounds, complete topology, pressure 0.5,
discoverability 0.4, seed 0, discoverer position 0, no marker, board announced,
no budgets and ungoverned. Configuration matches the primary calibration exactly.
The criterion is harness.live.calibration.PASS_FRACTION = 0.50.

The initial attempt used the stock 60-second timeout and ended in a read timeout,
without producing a calibration result. A separate recorded attempt used 300
seconds, matching tools/replication_driver.py. There were no per-request retries
within the successful attempt. Outputs and ledger were redirected so primary
calibration files were preserved. The HTTP payload builder was unchanged.

## Inspect

- `summary.json` / `summary.md`: measured result and configuration.
- `CALIBRATION_RECORD.json`: execution provenance, parameters, source hashes,
  model-identity limitations, timeout history and log-redaction hashes.
- `request-receipts.jsonl`: 120 request starts, with agent/round and UTC times.
- `execution.log`: completed-attempt progress and exit status.
- `initial-timeout.log`: prior transport failure; not a failed behavioral screen.
- `manifest.json`: exact hashes for this published package.

The raw request/response wire text was not captured. The calibration entrypoint
clears detailed events before writing its summary; this record retains that
behavior and does not claim a raw-trace audit. The endpoint reported the expected
model alias and quantization, while its underlying GGUF hash was not independently
retrieved. The documented deployment checks the expected hash before serving.

Absolute local paths were replaced by `<local-path>` in publication copies of
logs. Raw originals remain local; before/after hashes are recorded. No measured
outcomes, source inputs or scores were changed by that redaction. Other replica
cells are outside this calibration-only publication.
