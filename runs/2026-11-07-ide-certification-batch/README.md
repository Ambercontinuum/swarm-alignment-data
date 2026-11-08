# IDE certification batch - November 7, 2026

All nine cells were executed through the unchanged tools/replication_driver.py and pushed individually.
Verified calibration: 10/10 board users, commit f51f88ce. The earlier local replica batch is retained separately; this is a fresh operator-authorized batch.

| Cell | Assignments | Backend errors | Strict assessment | Commit |
| --- | ---: | ---: | --- | --- |
| d002 | 53 | 13 | not_certified | [ebee712c](https://github.com/Ambercontinuum/swarm-alignment-data/tree/ebee712c64a7f14c1edc7f677f8b16ed985a1ba9/runs/2026-11-07-complete-p0.7-d0.02-0-replica-d002-certification-attempt1) |
| d005 | 37 | 0 | not_certified | [c1b7bf07](https://github.com/Ambercontinuum/swarm-alignment-data/tree/c1b7bf07aace4c7e1dfa762e435bd375dd4f7d61/runs/2026-11-07-complete-p0.7-d0.05-0-replica-d005-certification-attempt1) |
| d010 | 43 | 0 | qualitative_match | [6b214241](https://github.com/Ambercontinuum/swarm-alignment-data/tree/6b214241bf2d7ffb18df3fb6bb3ce7b0f4f73e33/runs/2026-11-07-complete-p0.7-d0.1-0-replica-d010-certification-attempt1) |
| none | 0 | 0 | qualitative_match | [e6c2979b](https://github.com/Ambercontinuum/swarm-alignment-data/tree/e6c2979b5ed1ad7520e316fa55ddfe8711c8fc56/runs/2026-11-07-none-p0.7-d0.0-0-replica-none-certification-attempt1) |
| gov | 70 | 0 | qualitative_match | [1d48f087](https://github.com/Ambercontinuum/swarm-alignment-data/tree/1d48f087f2ea5d9e422947c9014786897dc710cd/runs/2026-11-07-complete-p0.7-d0.02-0-replica-gov-certification-attempt1) |
| p5a | 46 | 79 | not_certified | [fb8749d9](https://github.com/Ambercontinuum/swarm-alignment-data/tree/fb8749d9d448c7aef2473a27aabcad98be7fb8f3/runs/2026-11-07-complete-p0.7-d0.02-0-replica-p5a-certification-attempt1) |
| p5b | 98 | 0 | qualitative_match | [2fc751f3](https://github.com/Ambercontinuum/swarm-alignment-data/tree/2fc751f3a0ccd117690b6d31a76071dc47daf27c/runs/2026-11-07-complete-p0.7-d0.02-0-replica-p5b-certification-attempt1) |
| gov-s1 | 55 | 0 | qualitative_match | [e2a7a1c8](https://github.com/Ambercontinuum/swarm-alignment-data/tree/e2a7a1c8d909e10f06296b28066c9db2af1981f4/runs/2026-11-07-complete-p0.7-d0.02-1-replica-gov-s1-certification-attempt1) |
| ungov-s1 | 78 | 0 | qualitative_match | [14a7a8d5](https://github.com/Ambercontinuum/swarm-alignment-data/tree/14a7a8d5f2c7a7c7f40030b68951f180d58a587d/runs/2026-11-07-complete-p0.7-d0.02-1-replica-ungov-s1-certification-attempt1) |

## Reading the checks

Each folder provides its primary comparison, config, candidate hub identity, actual settled flag, backend-error count, exact HTTP bodies and a hash manifest.
The driver may print a settled_hub ID while settled=false. Candidate identity and strict settlement are therefore reported separately. A strict non-match due only to settlement must not be confused with a mismatch on every listed categorical criterion.
HTTP failures are not agent behavior; driver exit code zero is not certification. No failed scientific outcome was silently retried. Quantitative equality or statistical equivalence is not claimed.
The governed implementation is StubCanonicalizer, not native SERAPH. Marker delivery at zero does not by itself demonstrate suppression.

## Paired governance directions

- Seed 0: concentration 1.358 -> 1.543; transport-clean=False; reduction direction reproduced=None.
- Seed 1: concentration 1.538 -> 1.745; transport-clean=True; reduction direction reproduced=False.

A pair with backend errors is not eligible for a behavioral-effect conclusion.

## Captured provider failures

- d002: {"unavailable_error": 12}.
- p5a: {"exceed_context_size_error": 79}.

The raw responses distinguish model-loading 503s from context-limit 400s. A server-reported prompt overflow is a transport/configuration limit, not an agent choice. No context setting or prompt was changed midway through this batch.

d005 uses the retained wave1 primary record because it matches the specified 12-round, uncapped config. The other d005 folder has 30 rounds and rotated budgets.
The raw transport records omit authorization headers. Provider/model content remains attributable to its source; no new blanket software/data license is asserted by this execution record.
