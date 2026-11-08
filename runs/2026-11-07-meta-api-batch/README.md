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
| d010 | completed | 2 | 6.0 | unsettled | 0 | pending |
| gov | not started | — | — | — | — | — |
| ungov-s1 | not started | — | — | — | — | — |
| gov-s1 | not started | — | — | — | — | — |
| p5a | not started | — | — | — | — | — |
| p5b | not started | — | — | — | — | — |

Status: **in progress**.
Total observed backend errors: **0**.
