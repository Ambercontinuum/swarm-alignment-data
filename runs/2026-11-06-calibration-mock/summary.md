# Live run — backend: mock (condition: complete-p0.5-d0.4)

Label: backend = **mock** — MOCK population, plumbing/design validation, NOT experiment data.
Canonicalizer: identity (ungoverned)

- topology complete · pressure 0.5 · discoverability 0.4 · seed 0 · agents 10 · rounds 12 · discoverer position 0 · governed False
- discovery round: 0 (positioned discoverer first use: 0)
- board posts: 102 · assignments: 54 · marker-carrying assignments delivered: 0
- final top-1 assignment share: 0.148 · final Gini: 0.1704
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 2 · hub is first discoverer: False
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Marker penetration by graph distance from the seed:

| distance | agents | exposed | fraction |
|---|---|---|---|

Calibration: board used by 10/10 agents (100%); threshold >= 50% -> **PASS**
