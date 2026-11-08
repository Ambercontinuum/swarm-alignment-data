# Arm A2 — Meta API population — November 7, 2026

New population under the frozen swarm design. This is not a repeat-population certification of Qwen.

Model: `muse-spark-1.3`; endpoint: `https://api.meta.ai/v1`.
Smoke `none` is run first and does not gate behavioral eligibility. No calibration gate is added.
Executor: Codex. Execution is not blinded; no claim of blinding is made.

## Hash stop and correction

The first preflight stopped before API calls because Windows CRLF checkout bytes differed from the frozen hashes. Committed bytes matched. Amber authorized `core.autocrlf=false`, removal of working driver/live files, and restoration with `git checkout -- tools harness`. All eight working-file hashes then matched exactly. No driver or harness source change was made.

## Execution and judging

Only the qualitative checklist in `REPLICATION.md` applies: flip, hub identity class, marker presence, exact-zero control, and concentration regime. No strict-settlement equality or zero-backend-error certification gate is added. This batch reports a second population descriptively; it does not award a Qwen replication verdict. Disagreements are retained individually.
The unchanged driver retains its legacy temporary output naming; completed folders are immediately renamed to `-meta-<cell>` without overwrite. Exact HTTP bodies are observed without modifying model requests. The observer stops the process on API errors because the unchanged driver otherwise converts exceptions to PASS. This enforces the operator stop instruction; it is not a scoring gate. No retries or alternate models are allowed.

The model change is prospectively authorized by Amber for Arm A2; this committed run plan does not amend the already filed OSF artifact retroactively.

| Cell | State | Assignments | Concentration (top-1 × N) | Settled hub class | Backend errors | Run commit |
| --- | --- | ---: | ---: | --- | ---: | --- |
| none | completed | 0 | 0 | unsettled | 0 | 75097d2e5cceebd25721a130f63e83be9153b266 |
| d002 | completed | 2 | 12.0 | founder | 0 | dadb0b3b0b72231f8a68ecdce223946230fd3061 |
| d005 | completed | 12 | 12.0 | founder | 0 | 271a359488fc1cd230677beaf80e726f409f6640 |
| d010 | completed | 2 | 6.0 | unsettled | 0 | 367cc559a47977f0aba9e0c0680b7de1510c3e81 |
| gov | completed | 16 | 8.25 | founder | 0 | 341355672000cf3110ced3abd4df10b3f95e957e |
| ungov-s1 | completed | 11 | 12.0 | successor | 0 | 7ee1f77a99180025b133927a117051f0d47c5c26 |
| gov-s1 | completed | 8 | 12.0 | successor | 0 | 30e4fab0b72eadec5cea876becb13cbb90770e3f |
| p5a | stopped on API error | — | — | — | 1 | pending |
| p5b | not started | — | — | — | — | — |

Status: **stopped**.
Total observed backend errors: **1**.

## Exact stop error

```text
RemoteDisconnected: Remote end closed connection without response
```

The interrupted cell has no completed summary. No later cells were started.
